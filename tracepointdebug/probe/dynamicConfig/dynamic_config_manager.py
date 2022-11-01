from tracepointdebug.probe.breakpoints.tracepoint import TracePointManager
from tracepointdebug.probe.breakpoints.logpoint import LogPointManager
from tracepointdebug.probe.error_stack_manager import ErrorStackManager
from tracepointdebug.probe.snapshot import SnapshotCollectorConfigManager
from tracepointdebug.config import config_names
from tracepointdebug.config.config_provider import ConfigProvider

_ERROR_COLLECTION_ENABLE_KEY = "errorCollectionEnable"
_ERROR_COLLECTION_ENABLE_CAPTURE_FRAME = "errorCollectionEnableCaptureFrame"

class DynamicConfigManager():
    __instance = None

    def __init__(self, broker_manager):
        self.attached = True
        self.trace_point_manager = TracePointManager.instance()
        self.log_point_manager = LogPointManager.instance()
        self.error_stack_manager = ErrorStackManager.instance()
        self.broker_manager = broker_manager
        DynamicConfigManager.__instance = self

    @staticmethod
    def instance(*args, **kwargs):
        return DynamicConfigManager(*args,
                                 **kwargs) if DynamicConfigManager.__instance is None else DynamicConfigManager.__instance

    def handle_attach(self):
        self.attached = True
        self.broker_manager.publish_request()
        self.broker_manager.send_get_config()

    
    def handle_detach(self):
        self.attached = False
        self.trace_point_manager.remove_all_trace_points()
        self.log_point_manager.remove_all_log_points()
        self.error_stack_manager.shutdown()

    def update_config(self, config):
        SnapshotCollectorConfigManager.update_snapshot_config(config)
        ConfigProvider.set(config_names.SIDEKICK_ERROR_STACK_ENABLE, config.get(_ERROR_COLLECTION_ENABLE_KEY, False))
        self._update_set_trace_hooks(ConfigProvider.get(config_names.SIDEKICK_ERROR_STACK_ENABLE, False))
        ConfigProvider.set(config_names.SIDEKICK_ERROR_COLLECTION_ENABLE_CAPTURE_FRAME, config.get(_ERROR_COLLECTION_ENABLE_CAPTURE_FRAME, False))

    def publish_application_status(self, client=None):
        self.broker_manager.publish_application_status(client=client)

    def _update_set_trace_hooks(self, error_stack_enable):
        if error_stack_enable:
            self.error_stack_manager.start()
        else:
            self.error_stack_manager.shutdown()