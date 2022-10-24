from tracepointdebug.probe.breakpoints.tracepoint import TracePointManager
from tracepointdebug.probe.breakpoints.logpoint import LogPointManager
import logging

logger = logging.getLogger(__name__)

class TagManager(object):
    __instance = None

    def __init__(self):
        self.trace_point_manager = TracePointManager.instance()
        self.log_point_manager = LogPointManager.instance()
        TagManager.__instance = self

    @staticmethod
    def instance(*args, **kwargs):
        return TagManager(*args,**kwargs) if TagManager.__instance is None else TagManager.__instance

    def enable_tag(self, tag, client):
        self.trace_point_manager.enable_tag(tag, client)
        self.log_point_manager.enable_tag(tag, client)
        self._publish_status(client)

    def disable_tag(self, tag, client):
        self.trace_point_manager.disable_tag(tag, client)
        self.log_point_manager.disable_tag(tag, client)
        self._publish_status(client)

    def _publish_status(self, client):
        self.trace_point_manager.publish_application_status()
        self.log_point_manager.publish_application_status()
        if client:
            self.trace_point_manager.publish_application_status(client)
            self.log_point_manager.publish_application_status(client)
