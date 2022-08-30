import logging
import os
import time
from threading import Lock, Timer


from tracepointdebug import cdbg_native
from tracepointdebug.external.googleclouddebugger import imphook2, module_search2, module_utils2
from tracepointdebug.external.googleclouddebugger.module_explorer import GetCodeObjectAtLine
from tracepointdebug.probe.coded_exception import CodedException
from tracepointdebug.probe.condition.condition_context import ConditionContext
from tracepointdebug.probe.condition.condition_factory import ConditionFactory
from tracepointdebug.probe.errors import CONDITION_CHECK_FAILED, SOURCE_CODE_MISMATCH_DETECTED, \
    LINE_NO_IS_NOT_AVAILABLE, LINE_NO_IS_NOT_AVAILABLE_2, LINE_NO_IS_NOT_AVAILABLE_3, PUT_TRACEPOINT_FAILED
from tracepointdebug.probe.event.put_tracepoint_failed_event import PutTracePointFailedEvent
from tracepointdebug.probe.event.trace_point_rate_limit_event import TracePointRateLimitEvent
from tracepointdebug.probe.event.trace_point_snapshot_event import TracePointSnapshotEvent
from tracepointdebug.probe.event.tracepoint_snapshot_failed_event import TracePointSnapshotFailedEvent
from tracepointdebug.probe.ratelimit.rate_limit_result import RateLimitResult
from tracepointdebug.probe.ratelimit.rate_limiter import RateLimiter
from tracepointdebug.probe.snapshot_collector import SnapshotCollector
from tracepointdebug.probe.source_code_helper import get_source_code_hash
from tracepointdebug.trace import TraceSupport

logger = logging.getLogger(__name__)

_MAX_SNAPSHOT_SIZE = 32768
_MAX_FRAMES = 10
_MAX_EXPAND_FRAMES = 2


class TracePoint(object):

    def __init__(self, trace_point_manager, trace_point_config):
        self.config = trace_point_config
        self.id = trace_point_config.trace_point_id
        self.hit_count = 0
        self._lock = Lock()
        self._completed = False
        self._cookie = None
        self.trace_point_manager = trace_point_manager
        self._import_hook_cleanup = None
        self.condition = None
        self.timer = None
        self.rate_limiter = RateLimiter()
        self.thundra_agent = True

        if os.path.splitext(self.config.file)[1] != '.py':
            raise CodedException(PUT_TRACEPOINT_FAILED, (
                self.config.get_file_name(), self.config.line, self.config.client, 'Only .py file extension is supported'))

        if trace_point_config.expire_duration != -1:
            self.timer = Timer(trace_point_config.expire_duration, self.trace_point_manager.expire_trace_point,
                               args=(self,)).start()

        # Check if file really exist
        source_path = module_search2.Search(self.config.file)
        loaded_module = module_utils2.GetLoadedModuleBySuffix(source_path)

        # Module has been loaded, set trace point
        if loaded_module:
            self.set_active_trace_point(loaded_module)
        # Add an import hook to later set the trace point
        else:
            self._import_hook_cleanup = imphook2.AddImportCallbackBySuffix(
                source_path,
                self.set_active_trace_point)

    @staticmethod
    def get_id(file, line, client):
        return '{}:{}:{}'.format(file, line, client)

    def set_active_trace_point(self, module):
        try:
            self.remove_import_hook()
            file_path = os.path.splitext(module.__file__)[0] + '.py'

            # Check if source code matches with the source in client (IDE or web)
            if self.config.file_hash:
                source_hash = get_source_code_hash(file_path)
                if source_hash and source_hash != self.config.file_hash:
                    raise CodedException(SOURCE_CODE_MISMATCH_DETECTED, ( "tracepoint",
                        self.config.get_file_name(), self.config.line, self.config.client))

            status, code_object = GetCodeObjectAtLine(module, self.config.line)
            if not status:
                args = [str(self.config.line), file_path]
                alt_lines = [str(line) for line in code_object if line is not None]
                args = args + alt_lines

                if len(args) == 4:
                    err = LINE_NO_IS_NOT_AVAILABLE_3
                elif len(args) == 3:
                    err = LINE_NO_IS_NOT_AVAILABLE_2
                else:
                    err = LINE_NO_IS_NOT_AVAILABLE

                raise CodedException(err, tuple(args))

            # Create condition from expression
            if self.config.cond:
                try:
                    # Create the condition from expression using antlr parser and listeners
                    self.condition = ConditionFactory.create_condition_from_expression(self.config.cond)
                except Exception as e:
                    raise CodedException(CONDITION_CHECK_FAILED, (self.config.cond, str(e)))

            logger.info('Creating new Python breakpoint %s in %s, line %d' % (self.id, code_object, self.config.line))

            # Set the breakpoint callback to line and
            # store the identifier cookie to use later when removing
            self._cookie = cdbg_native.SetConditionalBreakpoint(
                code_object,
                self.config.line,
                None,
                self.breakpoint_callback)
        except Exception as exc:
            code = 0
            if isinstance(exc, CodedException):
                code = exc.code
            event = PutTracePointFailedEvent(self.config.get_file_name(), self.config.line, code, str(exc))
            event.client = self.config.client
            self.trace_point_manager.publish_event(event)
            self.complete_trace_point()

    def breakpoint_callback(self, event, frame):
        try:
            if self.config.disabled:
                return
            if self.condition:
                try:
                    f_variables = {}
                    f_variables.update(frame.f_locals)
                    f_variables.update(frame.f_globals)
                    result = self.condition.evaluate(ConditionContext(f_variables))
                    # Condition failed, do not send snapshot
                    if not result:
                        return
                except Exception as e:
                    logger.warning(e)
                    # TODO: report error to broker here
                    pass
            self.hit_count += 1
            if self.config.expire_hit_count != -1 and self.hit_count >= self.config.expire_hit_count:
                self.trace_point_manager.expire_trace_point(self)

            rate_limit_result = self.rate_limiter.check_rate_limit(time.time())

            if rate_limit_result == RateLimitResult.HIT:
                event = TracePointRateLimitEvent(self.config.get_file_name(), self.config.line)
                event.client = self.config.client
                self.trace_point_manager.publish_event(event)

            if rate_limit_result == RateLimitResult.EXCEEDED:
                return
            snapshot_collector = SnapshotCollector(_MAX_SNAPSHOT_SIZE, _MAX_FRAMES, _MAX_EXPAND_FRAMES)
            snapshot = snapshot_collector.collect(frame)

            trace_context = TraceSupport.get_trace_context()

            trace_id = None if not trace_context else trace_context.get_trace_id()
            transaction_id = None if not trace_context else trace_context.get_transaction_id()
            span_id = None if not trace_context else trace_context.get_span_id()

            event = TracePointSnapshotEvent(self.id, self.config.get_file_name(), self.config.line, method_name=snapshot.method_name,
                                            frames=snapshot.frames, transaction_id=transaction_id, trace_id=trace_id,
                                            span_id=span_id)

            event.client = self.config.client
            self.trace_point_manager.publish_event(event)
        except Exception as exc:
            logger.warning('Error on trace point snapshot %s' % exc)
            code = 0
            if isinstance(exc, CodedException):
                code = exc.code
            event = TracePointSnapshotFailedEvent(self.config.get_file_name(), self.config.line, code, str(exc))
            event.client = self.config.client
            self.trace_point_manager.publish_event(event)

    def remove_trace_point(self):
        self.remove_import_hook()
        if self._cookie is not None:
            logger.info('Clearing breakpoint %s' % self.id)
            if self.timer is not None:
                self.timer.cancel()
            cdbg_native.ClearConditionalBreakpoint(self._cookie)
            self._cookie = None
        self._completed = True

    def remove_import_hook(self):
        if self._import_hook_cleanup:
            self._import_hook_cleanup()
            self._import_hook_cleanup = None

    def complete_trace_point(self):
        self._completed = True
        if self.timer is not None:
            self.timer.cancel()
        self.remove_trace_point()
