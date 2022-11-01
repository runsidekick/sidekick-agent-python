from tracepointdebug.application.application import Application
from tracepointdebug.broker.handler.request.request_handler import RequestHandler
from tracepointdebug.probe.request.tracePoint.disable_trace_point_request import DisableTracePointRequest
from tracepointdebug.probe.response.tracePoint.disable_trace_point_response import DisableTracePointResponse
from tracepointdebug.probe.breakpoints.tracepoint import TracePointManager


class DisableTracePointRequestHandler(RequestHandler):
    REQUEST_NAME = "DisableTracePointRequest"

    @staticmethod
    def get_request_name():
        return DisableTracePointRequestHandler.REQUEST_NAME

    @staticmethod
    def get_request_cls():
        return DisableTracePointRequest

    @staticmethod
    def handle_request(request):
        application_info = Application.get_application_info()
        try:
            trace_point_manager = TracePointManager.instance()
            trace_point_manager.disable_trace_point(request.trace_point_id, request.get_client())

            trace_point_manager.publish_application_status()
            if request.get_client() is not None:
                trace_point_manager.publish_application_status(request.get_client())

            return DisableTracePointResponse(request_id=request.get_id(), client=request.get_client(),
                                             application_instance_id=application_info.get('applicationInstanceId'))
        except Exception as e:
            tp = DisableTracePointResponse(request_id=request.get_id(), client=request.get_client(),
                                           application_instance_id=application_info.get('applicationInstanceId'),
                                           erroneous=True)
            tp.set_error(e)
            return tp
