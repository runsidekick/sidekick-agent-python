from threading import RLock

from tracepointdebug.probe import errors
from tracepointdebug.probe.coded_exception import CodedException
from tracepointdebug.probe.trace_point import TracePoint
from tracepointdebug.probe.trace_point_config import TracePointConfig


class TracePointManager(object):
    __instance = None

    def __init__(self, broker_manager):
        self._lock = RLock()
        self._trace_points = {}
        self.broker_manager = broker_manager
        TracePointManager.__instance = self

    @staticmethod
    def instance(*args, **kwargs):
        return TracePointManager(*args,
                                 **kwargs) if TracePointManager.__instance is None else TracePointManager.__instance

    def list_trace_points(self, client):
        trace_points = []
        for trace_point_id in self._trace_points:
            tp = self._trace_points.get(trace_point_id)
            if client is None or tp.config.client == client:
                trace_points.append(tp.config)
        return trace_points

    def update_trace_point(self, trace_point_id, client, expire_duration, expire_count, enable_tracing,
                           condition, disable):
        with self._lock:
            if trace_point_id not in self._trace_points:
                raise CodedException(errors.NO_TRACEPOINT_EXIST_WITH_ID, (trace_point_id, client))
            trace_point = self._trace_points.pop(trace_point_id)
            trace_point.remove_trace_point()
            trace_point_config = TracePointConfig(trace_point_id, trace_point.config.file, trace_point.config.file_ref, trace_point.config.line,
                                                  client, condition, expire_duration, expire_count,
                                                  tracing_enabled=enable_tracing, disabled=disable)
            trace_point = TracePoint(self, trace_point_config)
            self._trace_points[trace_point_id] = trace_point

    def put_trace_point(self, trace_point_id, file, file_hash, line, client, expire_duration, expire_count,
                        enable_tracing, condition):
        with self._lock:
            if trace_point_id in self._trace_points:
                raise CodedException(errors.TRACEPOINT_ALREADY_EXIST, (file, line, client))
            file, file_ref = file.split("?ref=") # Commit id has been added to fileName. To get actual path, remove commit id.
            trace_point_config = TracePointConfig(trace_point_id, file, file_ref, line, client, condition, expire_duration,
                                                  expire_count,
                                                  file_hash=file_hash,
                                                  tracing_enabled=enable_tracing)
            trace_point = TracePoint(self, trace_point_config)
            self._trace_points[trace_point_id] = trace_point

    def remove_trace_point(self, trace_point_id, client):
        with self._lock:
            if trace_point_id in self._trace_points:
                self._trace_points.pop(trace_point_id).remove_trace_point()
            else:
                raise CodedException(errors.NO_TRACEPOINT_EXIST_WITH_ID, (trace_point_id, client))

    def remove_all_trace_points(self):
        with self._lock:
            for trace_point_id in self._trace_points:
                self._trace_points.get(trace_point_id).remove_trace_point()
            self._trace_points = {}

    def enable_trace_point(self, trace_point_id, client):
        with self._lock:
            if trace_point_id in self._trace_points:
                self._trace_points[trace_point_id].config.disabled = False
            else:
                raise CodedException(errors.NO_TRACEPOINT_EXIST_WITH_ID, (trace_point_id, client))

    def disable_trace_point(self, trace_point_id, client):
        with self._lock:
            if trace_point_id in self._trace_points:
                self._trace_points[trace_point_id].config.disabled = True
            else:
                raise CodedException(errors.NO_TRACEPOINT_EXIST_WITH_ID, (trace_point_id, client))

    def expire_trace_point(self, trace_point):
        with self._lock:
            if trace_point.timer is not None:
                trace_point.timer.cancel()
            trace_point_id = trace_point.config.trace_point_id
            if trace_point_id in self._trace_points:
                self._trace_points.pop(trace_point_id).remove_trace_point()

    def publish_event(self, event):
        self.broker_manager.publish_event(event)

    def publish_application_status(self, client=None):
        self.broker_manager.publish_application_status(client=client)
