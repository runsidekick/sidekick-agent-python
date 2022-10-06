import atexit

from . import cdbg_native
from .broker.broker_manager import BrokerManager
from .probe.trace_point_manager import TracePointManager
from .probe.log_point_manager import LogPointManager
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
    _broker_manager.initialize(tracepoint_data_redaction_callback, log_data_redaction_callback)
    tpm = TracePointManager(broker_manager=_broker_manager)
    lpm = LogPointManager(broker_manager=_broker_manager)
    esm = ErrorStackManager(broker_manager=_broker_manager)
    esm.start()
    atexit.register(tpm.remove_all_trace_points)
    atexit.register(lpm.remove_all_log_points)
    atexit.register(esm.shutdown)