import time, traceback
from tracepointdebug.probe.coded_exception import CodedException
from tracepointdebug.probe.coded_exception import CodedException
from tracepointdebug.probe.event.errorstack.error_stack_rate_limit_event import ErrorStackRateLimitEvent
from tracepointdebug.probe.event.errorstack.error_stack_snapshot_event import ErrorStackSnapshotEvent
from tracepointdebug.probe.event.errorstack.error_stack_snapshot_failed_event import ErrorStackSnapshotFailedEvent
from tracepointdebug.probe.ratelimit.rate_limit_result import RateLimitResult
from tracepointdebug.probe.ratelimit.rate_limiter import RateLimiter
from tracepointdebug.probe.snapshot import SnapshotCollector
import logging, sys, threading
from tracepointdebug.config import config_names
from tracepointdebug.config.config_provider import ConfigProvider
from datetime import datetime as dt
from cachetools import TTLCache
import datetime, os

logger = logging.getLogger(__name__)

_MAX_TIME_TO_ALIVE_MIN = 5

class ErrorStackManager(object):
    __instance = None

    def __init__(self, broker_manager):
        self.broker_manager = broker_manager
        self.old_settrace = sys.gettrace()
        self.old_threading = threading._trace_hook
        self.condition = None
        self.timer = None
        self._started = False
        self.sidekick_exception = "sidekickException"
        self.rate_limiter = RateLimiter()
        self.ttl_cache = TTLCache(maxsize=2048, ttl=datetime.timedelta(minutes=_MAX_TIME_TO_ALIVE_MIN), timer=datetime.datetime.now)
        ErrorStackManager.__instance = self

    @staticmethod
    def instance(*args, **kwargs):
        return ErrorStackManager(*args,
                                 **kwargs) if ErrorStackManager.__instance is None else ErrorStackManager.__instance

    @staticmethod
    def get_id(file, line):
        return '{}:{}:{}'.format(file, line, str(dt.now()))

    def _get_point_cache_id(self, frame):
        return frame.f_code.co_filename + ":::" + str(frame.f_lineno)

    def _check_point_inserted(self, frame):
        error_point_id = self._get_point_cache_id(frame)
        item = self.ttl_cache.get(error_point_id, None)
        if item is None:
            self.ttl_cache[error_point_id] = True
            return False
        return True

    def _white_list_exceptions(self, frame):
        frame_file_path = os.path.abspath(frame.f_code.co_filename)
        blacklist = ["python", "site-packages", "importlib", "tracepointdebug"]
        for black in blacklist:
            if black in frame_file_path:
                return False
        return True

    def trace_hook(self, frame, event, arg):
        if not ConfigProvider.get(config_names.SIDEKICK_ERROR_STACK_ENABLE):
            return
        if not self._white_list_exceptions(frame):
            return
        frame.f_trace = self._frame_hook

    def _frame_hook(self, frame, event, arg):
        try:
            if event != "exception" or not ConfigProvider.get(config_names.SIDEKICK_ERROR_STACK_ENABLE):
                return
            frame_file_name = frame.f_code.co_filename
            frame_line_no = frame.f_lineno
            rate_limit_result_for_frame_call = self.rate_limiter.check_rate_limit(time.time())
            check_point_already_inserted = self._check_point_inserted(frame)

            if (check_point_already_inserted):
                return

            if (rate_limit_result_for_frame_call == RateLimitResult.HIT):
                event = ErrorStackRateLimitEvent(frame_file_name, frame_line_no)
                self._publish_event(event)

            if (rate_limit_result_for_frame_call == RateLimitResult.EXCEEDED):
                return

            frames = []
            if ConfigProvider.get(config_names.SIDEKICK_ERROR_COLLECTION_ENABLE_CAPTURE_FRAME, False):
                snapshot_collector = SnapshotCollector()
                snapshot = snapshot_collector.collect(frame)
                frames = snapshot.frames
            error_stack_id = self.get_id(frame_file_name, frame_line_no)
            error = {
                "name": str(arg[0]) or "Error",
                "message": str(arg[1]),
                "stack": str(traceback.extract_tb(arg[2]))
            }
            event = ErrorStackSnapshotEvent(error_stack_id, frame_file_name, frame_line_no, method_name=frame.f_code.co_name,
                                            error=error, frames=frames)
            self._publish_event(event)
        except Exception as exc:
            logger.warning('Error on error stack snapshot %s' % exc)
            code = 0
            if isinstance(exc, CodedException):
                code = exc.code
            event = ErrorStackSnapshotFailedEvent(frame.f_code.co_filename, frame.f_lineno, code, str(exc))
            self._publish_event(event)

    def start(self):
        if ConfigProvider.get(config_names.SIDEKICK_ERROR_STACK_ENABLE) and not self._started:
            self._started = True
            sys.settrace(self.trace_hook)
            threading.settrace(self.trace_hook)

    def shutdown(self):
        if self._started:
            self._started = False
            sys.settrace(self.old_settrace)
            threading.settrace(self.old_threading)

    def _publish_event(self, event):
        self.broker_manager.publish_event(event)
