from tracepointdebug.probe.coded_exception import CodedException
from tracepointdebug.probe.coded_exception import CodedException
from tracepointdebug.probe.event.errorstack.error_stack_rate_limit_event import ErrorStackRateLimitEvent
from tracepointdebug.probe.event.errorstack.error_stack_snapshot_event import ErrorStackSnapshotEvent
from tracepointdebug.probe.event.errorstack.error_stack_snapshot_failed_event import ErrorStackSnapshotFailedEvent
from tracepointdebug.probe.ratelimit.rate_limit_result import RateLimitResult
from tracepointdebug.probe.ratelimit.rate_limiter import RateLimiter
from tracepointdebug.probe.snapshot_collector import SnapshotCollector
import logging, sys, threading
from tracepointdebug.config import config_names
from tracepointdebug.config.config_provider import ConfigProvider

from datetime import datetime as dt
from cachetools import TTLCache

logger = logging.getLogger(__name__)

_MAX_SNAPSHOT_SIZE = 32768
_MAX_FRAMES = 10
_MAX_EXPAND_FRAMES = 2
_MAX_TIME_TO_ALIVE = 3 * 60

class ErrorStackManager(object):
    __instance = None

    def __init__(self, broker_manager):
        self.broker_manager = broker_manager
        self.old_settrace = sys.gettrace()
        self.old_threading = threading._trace_hook
        self._lock = threading.Lock()
        self.condition = None
        self.timer = None
        self.rate_limiter = RateLimiter()
        self.ttl_cache = TTLCache(maxsize=128, ttl=_MAX_TIME_TO_ALIVE)
        ErrorStackManager.__instance = self

    @staticmethod
    def instance(*args, **kwargs):
        return ErrorStackManager(*args,
                                 **kwargs) if ErrorStackManager.__instance is None else ErrorStackManager.__instance

    @staticmethod
    def get_id(file, line, client):
        return '{}:{}:{}:{}'.format(file, line, client, str(dt.now()))

    def _get_point_cache_id(self, frame):
        return frame.f_code.co_filename + ":::" + str(frame.f_lineno)

    def _check_point_rate_limit(self, frame):
        with self._lock:
            error_point_id = self._get_point_cache_id(frame)
            if error_point_id not in self.ttl_cache:
                self.ttl_cache[error_point_id] = RateLimiter() 
            return self.ttl_cache[error_point_id].check_rate_limit(time.time())

    def trace_hook(self, frame, event, arg):
        frame.f_trace = self._frame_hook

    def _frame_hook(self, frame, event, arg):
        try:
            if event != "exception": 
                return
            frame_file_name = frame.f_code.co_filename
            frame_line_no = frame.f_lineno
            rate_limit_result_for_frame_call = self.rate_limiter.check_rate_limit(time.time())
            rate_limit_result_for_point = self._check_point_rate_limit(frame)

            if (rate_limit_result_for_frame_call == RateLimitResult.HIT or 
                    rate_limit_result_for_frame_call == RateLimitResult.HIT):
                event = ErrorStackRateLimitEvent(frame_file_name, frame_line_no)
                self.error_stack_manager.publish_event(event)

            if (rate_limit_result_for_frame_call == RateLimitResult.EXCEEDED or 
                    rate_limit_result_for_point == RateLimitResult.EXCEEDED):
                return
            snapshot_collector = SnapshotCollector(_MAX_SNAPSHOT_SIZE, _MAX_FRAMES, _MAX_EXPAND_FRAMES)
            snapshot = snapshot_collector.collect(frame)
            error_stack_id = self.get_id()
            event = ErrorStackSnapshotEvent(error_stack_id, frame_file_name, frame_line_no, method_name=snapshot.method_name,
                                            frames=snapshot.frames)

            self.error_stack_manager.publish_event(event)
        except Exception as exc:
            logger.warning('Error on error stack snapshot %s' % exc)
            code = 0
            if isinstance(exc, CodedException):
                code = exc.code
            event = ErrorStackSnapshotFailedEvent(frame.f_code.co_filename, frame.f_lineno, code, str(exc))
            self._publish_event(event)

    def start(self):
        if ConfigProvider.get(config_names.SIDEKICK_ERROR_STACK_ENABLE):
            sys.settrace(self.trace_hook)
            threading.settrace(self.trace_hook)

    def shutdown(self):
        if ConfigProvider.get(config_names.SIDEKICK_ERROR_STACK_ENABLE):
            sys.settrace(self.old_settrace)
            threading.settrace(self.old_threading)

    def _publish_event(self, event):
        self.broker_manager.publish_event(event)
