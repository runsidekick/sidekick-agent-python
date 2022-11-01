from tracepointdebug.application.application import Application
from tracepointdebug.broker.handler.request.request_handler import RequestHandler
from tracepointdebug.probe.request.tracePoint.update_trace_point_request import UpdateTracePointRequest
from tracepointdebug.probe.response.tracePoint.update_trace_point_response import UpdateTracePointResponse
from tracepointdebug.probe.breakpoints.tracepoint import TracePointManager


class UpdateTracePointRequestHandler(RequestHandler):
    REQUEST_NAME = "UpdateTracePointRequest"

    @staticmethod
    def get_request_name():
        return UpdateTracePointRequestHandler.REQUEST_NAME

    @staticmethod
    def get_request_cls():
        return UpdateTracePointRequest

    @staticmethod
    def handle_request(request):
        application_info = Application.get_application_info()
        try:
            trace_point_manager = TracePointManager.instance()
            trace_point_manager.update_trace_point(request.trace_point_id,
                                                   request.get_client(), request.expire_secs,
                                                   request.expire_count, request.enable_tracing, request.condition,
                                                   disable=request.disable, tags=request.tags)

            trace_point_manager.publish_application_status()
            if request.get_client() is not None:
                trace_point_manager.publish_application_status(request.get_client())

            return UpdateTracePointResponse(request_id=request.get_id(), client=request.get_client(),
                                            application_instance_id=application_info.get('applicationInstanceId'))
        except Exception as e:
            tp = UpdateTracePointResponse(request_id=request.get_id(), client=request.get_client(),
                                          application_instance_id=application_info.get('applicationInstanceId'),
                                          erroneous=True)
            tp.set_error(e)
            return tp
