from tracepointdebug.broker.handler.response.response_handler import ResponseHandler
from tracepointdebug.probe.dynamicConfig.dynamic_config_manager import DynamicConfigManager
from tracepointdebug.probe.response.dynamicConfig.get_config_response import GetConfigResponse

import logging
logger = logging.getLogger(__name__)

class GetConfigResponseHandler(ResponseHandler):
    RESPONSE_NAME = "GetConfigResponse"


    @staticmethod
    def get_response_name():
        return GetConfigResponseHandler.RESPONSE_NAME

    
    @staticmethod
    def get_response_cls():
        return GetConfigResponse


    @staticmethod
    def handle_response(response):
        try:
            config = response.config
            dynamic_config_manager = DynamicConfigManager.instance()
            dynamic_config_manager.update_config(config)
        except Exception as e:
            logger.error("Error on connection, msg: {}".format(response.config))