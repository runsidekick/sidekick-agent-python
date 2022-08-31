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
import tracepointdebug.probe.errors as errors
from tracepointdebug.probe.event.logpoint.log_point_event import LogPointEvent
from tracepointdebug.probe.event.logpoint.log_point_failed_event import LogPointFailedEvent
from tracepointdebug.probe.event.logpoint.put_logpoint_failed_event import PutLogPointFailedEvent
from tracepointdebug.probe.ratelimit.rate_limit_result import RateLimitResult
from tracepointdebug.probe.ratelimit.rate_limiter import RateLimiter
from tracepointdebug.probe.snapshot_collector import SnapshotCollector
from tracepointdebug.probe.source_code_helper import get_source_code_hash
import pystache
from datetime import datetime
from tracepointdebug.utils.log.logger import print_log_event_message

logger = logging.getLogger(__name__)

_MAX_SNAPSHOT_SIZE = 32768
_MAX_FRAMES = 10
_MAX_EXPAND_FRAMES = 2

class LogPoint(object):

    def __init__(self, log_point_manager, log_point_config):
        self.config = log_point_config
        self.id = log_point_config.log_point_id
        self.hit_count = 0
        self._lock = Lock()
        self._completed = False
        self._cookie = None
        self.log_point_manager = log_point_manager
        self._import_hook_cleanup = None
        self.condition = None
        self.timer = None
        self.rate_limiter = RateLimiter()

        if os.path.splitext(self.config.file)[1] != '.py':
            raise CodedException(errors.PUT_LOGPOINT_FAILED, (
                self.config.get_file_name(), self.config.line, self.config.client, 'Only .py file extension is supported'))

        if log_point_config.expire_duration != -1:
            self.timer = Timer(log_point_config.expire_duration, self.log_point_manager.expire_log_point,
                               args=(self,)).start()

        # Check if file really exist
        source_path = module_search2.Search(self.config.file)
        loaded_module = module_utils2.GetLoadedModuleBySuffix(source_path)

        # Module has been loaded, set log point
        if loaded_module:
            self.set_active_log_point(loaded_module)
        # Add an import hook to later set the log point
        else:
            self._import_hook_cleanup = imphook2.AddImportCallbackBySuffix(
                source_path,
                self.set_active_log_point)

    @staticmethod
    def get_id(file, line, client):
        return '{}:{}:{}'.format(file, line, client)

    def set_active_log_point(self, module):
        try:
            self.remove_import_hook()
            file_path = os.path.splitext(module.__file__)[0] + '.py'

            # Check if source code matches with the source in client (IDE or web)
            if self.config.file_hash:
                source_hash = get_source_code_hash(file_path)
                if source_hash and source_hash != self.config.file_hash:
                    raise CodedException(errors.SOURCE_CODE_MISMATCH_DETECTED, ( "logpoint",
                        self.config.get_file_name(), self.config.line, self.config.client))

            status, code_object = GetCodeObjectAtLine(module, self.config.line)
            if not status:
                args = [str(self.config.line), file_path]
                alt_lines = [str(line) for line in code_object if line is not None]
                args = args + alt_lines

                if len(args) == 4:
                    err = errors.LINE_NO_IS_NOT_AVAILABLE_3
                elif len(args) == 3:
                    err = errors.LINE_NO_IS_NOT_AVAILABLE_2
                else:
                    err = errors.LINE_NO_IS_NOT_AVAILABLE

                raise CodedException(err, tuple(args))

            # Create condition from expression
            if self.config.cond:
                try:
                    # Create the condition from expression using antlr parser and listeners
                    self.condition = ConditionFactory.create_condition_from_expression(self.config.cond)
                except Exception as e:
                    raise CodedException(errors.CONDITION_CHECK_FAILED, (self.config.cond, str(e)))

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
            event = PutLogPointFailedEvent(self.config.get_file_name(), self.config.line, code, str(exc))
            event.client = self.config.client
            self.log_point_manager.publish_event(event)
            self.complete_log_point()

    def breakpoint_callback(self, event, frame):
        try:
            f_variables = {}
            f_variables.update(frame.f_locals)
            f_variables.update(frame.f_globals)
            if self.config.disabled:
                return
            if self.condition:
                try:
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
                self.log_point_manager.expire_log_point(self)

            rate_limit_result = self.rate_limiter.check_rate_limit(time.time())

            if rate_limit_result == RateLimitResult.HIT:
                event = LogPointFailedEvent(self.config.get_file_name(), self.config.line)
                event.client = self.config.client
                self.log_point_manager.publish_event(event)

            if rate_limit_result == RateLimitResult.EXCEEDED:
                return
            snapshot_collector = SnapshotCollector(_MAX_SNAPSHOT_SIZE, _MAX_FRAMES, _MAX_EXPAND_FRAMES)
            snapshot = snapshot_collector.collect(frame)
            log_message = pystache.render(self.config.log_expression, f_variables)
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            event = LogPointEvent(log_point_id = self.id, 
                file=self.config.get_file_name(), 
                line_no = self.config.line, 
                method_name=snapshot.method_name, 
                log_message=log_message,
                created_at=created_at)
            
            if self.config.stdout_enabled:
                print_log_event_message(created_at, self.config.log_level, log_message)

            event.client = self.config.client
            self.log_point_manager.publish_event(event)
        except Exception as exc:
            logger.warning('Error on log point snapshot %s' % exc)
            code = 0
            if isinstance(exc, CodedException):
                code = exc.code
            event = LogPointFailedEvent(self.config.get_file_name(), self.config.line, code, str(exc))
            event.client = self.config.client
            self.log_point_manager.publish_event(event)

    def remove_log_point(self):
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

    def complete_log_point(self):
        self._completed = True
        if self.timer is not None:
            self.timer.cancel()
        self.remove_log_point()
