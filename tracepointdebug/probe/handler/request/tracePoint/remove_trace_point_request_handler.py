from tracepointdebug.application.application import Application
from tracepointdebug.broker.handler.request.request_handler import RequestHandler
from tracepointdebug.probe.request.tracePoint.remove_trace_point_request import RemoveTracePointRequest
from tracepointdebug.probe.response.tracePoint.remove_trace_point_response import RemoveTracePointResponse
from tracepointdebug.probe.breakpoints.tracepoint import TracePointManager


class RemoveTracePointRequestHandler(RequestHandler):
    REQUEST_NAME = "RemoveTracePointRequest"

    @staticmethod
    def get_request_name():
        return RemoveTracePointRequestHandler.REQUEST_NAME

    @staticmethod
    def get_request_cls():
        return RemoveTracePointRequest

    @staticmethod
    def handle_request(request):
        application_info = Application.get_application_info()
        try:
            trace_point_manager = TracePointManager.instance()
            trace_point_manager.remove_trace_point(request.trace_point_id, request.get_client())

            trace_point_manager.publish_application_status()
            if request.get_client() is not None:
                trace_point_manager.publish_application_status(request.get_client())

            return RemoveTracePointResponse(request_id=request.get_id(), client=request.get_client(),
                                            application_instance_id=application_info.get('applicationInstanceId'))
        except Exception as e:
            tp = RemoveTracePointResponse(request_id=request.get_id(), client=request.get_client(),
                                          application_instance_id=application_info.get('applicationInstanceId'),
                                          erroneous=True)
            tp.set_error(e)
            return tp
