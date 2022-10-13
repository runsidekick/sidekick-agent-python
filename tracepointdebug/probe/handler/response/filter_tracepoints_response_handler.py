from tracepointdebug.probe.coded_exception import CodedException
from tracepointdebug.probe.errors import TRACEPOINT_ALREADY_EXIST
from tracepointdebug.probe.breakpoints.tracepoint import TracePointManager
from tracepointdebug.broker.handler.response.response_handler import ResponseHandler
from tracepointdebug.probe.response.tracePoint.filter_tracepoints_response import FilterTracePointsResponse

from tracepointdebug.utils.validation import validate_file_name_and_line_no

import logging
logger = logging.getLogger(__name__)

def _applyTracePoint(trace_point):
    try:
        validate_file_name_and_line_no(trace_point.get("fileName"), trace_point.get("lineNo"))
        condition = trace_point.get("condition", None)
        client = trace_point.get("client", None)
        file_name = trace_point.get("fileName", None)
        trace_point_manager = TracePointManager.instance()
        trace_point_manager.put_trace_point(trace_point.get("id", None), file_name, 
                                            trace_point.get("fileHash", None), trace_point.get("lineNo",None),
                                            client, trace_point.get("expireDuration", None), trace_point.get("expireCount", None),
                                            trace_point.get("disabled", None), condition = condition,
                                            tags=trace_point.get("tags", set()))
        
        trace_point_manager.publish_application_status()
        if client is not None:
            trace_point_manager.publish_application_status(client)

    except Exception as e:
        skip_logging = False
        if isinstance(e, CodedException):
            skip_logging = True if e.code == TRACEPOINT_ALREADY_EXIST.code else False
        if not skip_logging:
            logger.error("Unable to apply tracepoint %s" % e)

class FilterTracePointsResponseHandler(ResponseHandler):
    RESPONSE_NAME = "FilterTracePointsResponse"


    @staticmethod
    def get_response_name():
        return FilterTracePointsResponseHandler.RESPONSE_NAME

    
    @staticmethod
    def get_response_cls():
        return FilterTracePointsResponse


    @staticmethod
    def handle_response(response):
        trace_points = response.trace_points
        for trace_point in trace_points:
            _applyTracePoint(trace_point)
    