import atexit

from . import cdbg_native
from .broker.broker_manager import BrokerManager
from .probe.trace_point_manager import TracePointManager
from .probe.log_point_manager import LogPointManager
'''
    After importing ConfigProvider for the first time, the __init__.py has been run by interpreter and
    whole configuration is reflected to configs.
'''
from .config.config_provider import ConfigProvider


import logging
logger = logging.getLogger(__name__)

def start():
    cdbg_native.InitializeModule(None)
    _broker_manager = BrokerManager().instance()
    tpm = TracePointManager(broker_manager=_broker_manager)
    lpm = LogPointManager(broker_manager=_broker_manager)
    _broker_manager.initialize()
    atexit.register(tpm.remove_all_trace_points)
    atexit.register(lpm.remove_all_log_points)
