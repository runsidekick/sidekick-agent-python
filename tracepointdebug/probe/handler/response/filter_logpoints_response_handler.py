from tracepointdebug.probe.coded_exception import CodedException
from tracepointdebug.probe.errors import LOGPOINT_ALREADY_EXIST
from tracepointdebug.probe.breakpoints.logpoint import LogPointManager
from tracepointdebug.broker.handler.response.response_handler import ResponseHandler
from tracepointdebug.application.application import Application
from tracepointdebug.probe.response.logPoint.filter_logpoints_response import FilterLogPointsResponse
from tracepointdebug.utils.validation import validate_file_name_and_line_no

import logging
logger = logging.getLogger(__name__)

def _applyLogPoint(log_point):
    try:
        validate_file_name_and_line_no(log_point.get("fileName"), log_point.get("lineNo"))
        condition = log_point.get("condition", None)
        client = log_point.get("client", None)
        file_name = log_point.get("fileName", None)
        log_expression = log_point.get("logExpression", "")
        log_level = log_point.get("logLevel", "INFO")
        stdout_enabled = log_point.get("stdoutEnabled", True)
        log_point_manager = LogPointManager.instance()
        log_point_manager.put_log_point(log_point.get("id", None), file_name, 
                                            log_point.get("fileHash", None), log_point.get("lineNo",None),
                                            client, log_point.get("expireDuration", None), log_point.get("expireCount", None),
                                            log_point.get("disabled", False), log_expression=log_expression, condition=condition,
                                            log_level=log_level, stdout_enabled=stdout_enabled, tags=log_point.get("tags", set()))
        
        log_point_manager.publish_application_status()
        if client is not None:
            log_point_manager.publish_application_status(client)

    except Exception as e:
        skip_logging = False
        if isinstance(e, CodedException):
            skip_logging = True if e.code == LOGPOINT_ALREADY_EXIST.code else False
        if not skip_logging:
            logger.error("Unable to apply logpoint %s" % e)

class FilterLogPointsResponseHandler(ResponseHandler):
    RESPONSE_NAME = "FilterLogPointsResponse"


    @staticmethod
    def get_response_name():
        return FilterLogPointsResponseHandler.RESPONSE_NAME

    
    @staticmethod
    def get_response_cls():
        return FilterLogPointsResponse


    @staticmethod
    def handle_response(response):
        log_points = response.log_points
        for log_point in log_points:
            _applyLogPoint(log_point)
    