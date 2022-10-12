from tracepointdebug.application.application import Application
from tracepointdebug.broker.handler.request.request_handler import RequestHandler
from tracepointdebug.probe.log_point_manager import LogPointManager
from tracepointdebug.probe.trace_point_manager import TracePointManager
from tracepointdebug.probe.request.tag.disable_probe_tag_requests import DisableProbeTagRequest
from tracepointdebug.probe.response.tag.disable_tag_response import DisableTagResponse


class DisableProbeTagRequestHandler(RequestHandler):
    REQUEST_NAME = "DisableProbeTagRequest"

    @staticmethod
    def get_request_name():
        return DisableProbeTagRequestHandler.REQUEST_NAME

    @staticmethod
    def get_request_cls():
        return DisableProbeTagRequest

    @staticmethod
    def handle_request(request):
        application_info = Application.get_application_info()
        try:
            trace_point_manager = TracePointManager.instance()
            log_point_manager = LogPointManager.instance()
            trace_point_manager.disable_tag(request.get_tag(), request.get_client())
            log_point_manager.disable_tag(request.get_tag(), request.get_client())
            log_point_manager.publish_application_status()
            trace_point_manager.publish_application_status()
            if request.get_client() is not None:
                log_point_manager.publish_application_status(request.get_client())
                trace_point_manager.publish_application_status(request.get_client())

            return DisableTagResponse(request_id=request.get_id(), client=request.get_client(),
                                             application_instance_id=application_info.get('applicationInstanceId'))
        except Exception as e:
            tp = DisableTagResponse(request_id=request.get_id(), client=request.get_client(),
                                           application_instance_id=application_info.get('applicationInstanceId'),
                                           erroneous=True)
            tp.set_error(e)
            return tp
