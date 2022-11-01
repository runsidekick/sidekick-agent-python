from tracepointdebug.application.application import Application
from tracepointdebug.broker.handler.request.request_handler import RequestHandler
from tracepointdebug.probe.request.tracePoint.put_trace_point_request import PutTracePointRequest
from tracepointdebug.probe.response.tracePoint.put_trace_point_response import PutTracePointResponse
from tracepointdebug.probe.breakpoints.tracepoint import TracePointManager
from tracepointdebug.utils.validation import validate_file_name_and_line_no


class PutTracePointRequestHandler(RequestHandler):
    REQUEST_NAME = "PutTracePointRequest"

    @staticmethod
    def get_request_name():
        return PutTracePointRequestHandler.REQUEST_NAME

    @staticmethod
    def get_request_cls():
        return PutTracePointRequest

    @staticmethod
    def handle_request(request):
        application_info = Application.get_application_info()
        try:
            validate_file_name_and_line_no(request.file, request.line_no)
            trace_point_manager = TracePointManager.instance()
            trace_point_manager.put_trace_point(request.trace_point_id, request.file, request.file_hash,
                                                request.line_no,
                                                request.get_client(), request.expire_secs,
                                                request.expire_count, request.enable_tracing, request.condition,
                                                request.tags)

            trace_point_manager.publish_application_status()
            if request.get_client() is not None:
                trace_point_manager.publish_application_status(request.get_client())

            return PutTracePointResponse(request_id=request.get_id(), client=request.get_client(),
                                         application_instance_id=application_info.get('applicationInstanceId'))
        except Exception as e:
            tp = PutTracePointResponse(request_id=request.get_id(), client=request.get_client(),
                                       application_instance_id=application_info.get('applicationInstanceId'),
                                       erroneous=True)
            tp.set_error(e)
            return tp
