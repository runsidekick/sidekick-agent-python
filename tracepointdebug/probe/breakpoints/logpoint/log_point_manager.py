from threading import RLock

from tracepointdebug.probe import errors
from tracepointdebug.probe.coded_exception import CodedException
from .log_point import LogPoint
from .log_point_config import LogPointConfig
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class LogPointManager(object):
    __instance = None

    def __init__(self, broker_manager, data_redaction_callback=None):
        self._lock = RLock()
        self._log_points = {}
        self._tagged_log_points = defaultdict(set)
        self.broker_manager = broker_manager
        self._data_redaction_callback = None
        if callable(data_redaction_callback):
            self._data_redaction_callback = data_redaction_callback
        LogPointManager.__instance = self

    @staticmethod
    def instance(*args, **kwargs):
        return LogPointManager(*args,
                                 **kwargs) if LogPointManager.__instance is None else LogPointManager.__instance

    def list_log_points(self, client):
        with self._lock:
            log_points = []
            for log_point_id in self._log_points:
                tp = self._log_points.get(log_point_id)
                if client is None or tp.config.client == client:
                    log_points.append(tp.config)
            return log_points

    def update_log_point(self, log_point_id, client, expire_duration, expire_count, log_expression,
                           condition, disabled, log_level, stdout_enabled, tags):
        with self._lock:
            if log_point_id not in self._log_points:
                raise CodedException(errors.NO_LOGPOINT_EXIST_WITH_ID, (log_point_id, client))
            self._delete_log_point_tags(log_point_id)
            log_point = self._log_points.pop(log_point_id)
            log_point.remove_log_point()
            log_point_config = LogPointConfig(log_point_id, log_point.config.file, log_point.config.file_ref, log_point.config.line,
                                                  client, log_expression, condition, expire_duration, expire_count, disabled=disabled,
                                                  log_level=log_level, stdout_enabled=stdout_enabled, tags=tags)
            log_point = LogPoint(self, log_point_config)
            self._log_points[log_point_id] = log_point
            if tags:
                self._add_log_point_tags(log_point_id, tags)

    def put_log_point(self, log_point_id, file, file_hash, line, client, expire_duration, expire_count,
                        disabled, log_expression, condition, log_level, stdout_enabled, tags):
        with self._lock:
            if log_point_id in self._log_points:
                raise CodedException(errors.LOGPOINT_ALREADY_EXIST, (file, line, client))
            file, file_ref = file.split("?ref=") # Commit id has been added to fileName. To get actual path, remove commit id.
            log_point_config = LogPointConfig(log_point_id, file, file_ref, line, client, log_expression, condition, expire_duration,
                                                  expire_count,
                                                  file_hash=file_hash,
                                                  disabled=disabled,
                                                  log_level=log_level,
                                                  stdout_enabled=stdout_enabled,
                                                  tags=tags)
            log_point = LogPoint(self, log_point_config)
            self._log_points[log_point_id] = log_point
            if tags:
                self._add_log_point_tags(log_point_id, tags)

    def remove_log_point(self, log_point_id, client):
        with self._lock:
            if log_point_id in self._log_points:
                self._delete_log_point_tags(log_point_id)
                self._log_points.pop(log_point_id).remove_log_point()
            else:
                raise CodedException(errors.NO_LOGPOINT_EXIST_WITH_ID, (log_point_id, client))

    def remove_all_log_points(self):
        with self._lock:
            for log_point_id in self._log_points:
                self._log_points.get(log_point_id).remove_log_point()
            self._log_points = {}
            self._tagged_log_points = defaultdict(set)

    def enable_log_point(self, log_point_id, client):
        with self._lock:
            if log_point_id in self._log_points:
                self._log_points[log_point_id].config.disabled = False
            else:
                raise CodedException(errors.NO_LOGPOINT_EXIST_WITH_ID, (log_point_id, client))

    def disable_log_point(self, log_point_id, client):
        with self._lock:
            if log_point_id in self._log_points:
                self._log_points[log_point_id].config.disabled = True
            else:
                raise CodedException(errors.NO_LOGPOINT_EXIST_WITH_ID, (log_point_id, client))

    def enable_tag(self, tags, client):
        with self._lock:
            for tag in tags:
                if tag in self._tagged_log_points:
                    log_point_ids = self._tagged_log_points.get(tag, set())
                    for log_point_id in log_point_ids:
                        self.enable_log_point(log_point_id, client)

    def disable_tag(self, tags, client):
        with self._lock:
            for tag in tags:
                if tag in self._tagged_log_points:
                    log_point_ids = self._tagged_log_points.get(tag, set())
                    for log_point_id in log_point_ids:
                        self.disable_log_point(log_point_id, client)

    def expire_log_point(self, log_point):
        with self._lock:
            if log_point.timer is not None:
                log_point.timer.cancel()
            log_point_id = log_point.config.log_point_id
            if log_point_id in self._log_points:
                self._log_points.pop(log_point_id).remove_log_point()

    def publish_event(self, event):
        self.broker_manager.publish_event(event)

    def publish_application_status(self, client=None):
        self.broker_manager.publish_application_status(client=client)


    def _delete_log_point_tags(self, log_point_id):
        try:
            log_point_tags = self._log_points[log_point_id].config.tags
            deleted_tags = set()
            for log_point_tag in log_point_tags:
                self._tagged_log_points[log_point_tag].discard(log_point_id)
                if not self._tagged_log_points[log_point_tag]:
                    deleted_tags.add(log_point_tag)
            for deleted_tag in deleted_tags:
                del self._tagged_log_points[deleted_tag]
        except Exception as e:
            logger.error("Error while cleaning logpoints tags %s " % e)

    def _add_log_point_tags(self, log_point_id, tags=set()):
        try:
            for tag in tags:
                self._tagged_log_points[tag].add(log_point_id)
        except Exception as e:
            logger.error("Error while putting logpoints tags %s " % e)
