import atexit

from tracepointdebug.probe.dynamicConfig.dynamic_config_manager import DynamicConfigManager

from . import cdbg_native
from .broker.broker_manager import BrokerManager
from .probe.breakpoints.tracepoint import TracePointManager
from .probe.breakpoints.logpoint import LogPointManager
from .probe.error_stack_manager import ErrorStackManager

'''
    After importing ConfigProvider for the first time, the __init__.py has been run by interpreter and
    whole configuration is reflected to configs.
'''


tracepoint_data_redaction_callback = None
log_data_redaction_callback = None

import logging
logger = logging.getLogger(__name__)

def start(tracepoint_data_redaction_callback=None, log_data_redaction_callback=None):
    cdbg_native.InitializeModule(None)
    _broker_manager = BrokerManager().instance()
    TracePointManager(broker_manager=_broker_manager, data_redaction_callback=tracepoint_data_redaction_callback)
    LogPointManager(broker_manager=_broker_manager, data_redaction_callback=log_data_redaction_callback)
    esm = ErrorStackManager(broker_manager=_broker_manager)
    dcm = DynamicConfigManager(broker_manager=_broker_manager)
    _broker_manager.initialize()
    esm.start()
    atexit.register(dcm.handle_detach)