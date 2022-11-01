from tracepointdebug.application.application import Application
from tracepointdebug.broker.handler.request.request_handler import RequestHandler
from tracepointdebug.probe.request.tag.enable_probe_tag_requests import EnableProbeTagRequest
from tracepointdebug.probe.response.tag.enable_probe_tag_response import EnableProbeTagResponse
from tracepointdebug.probe.tag_manager import TagManager

class EnableProbeTagRequestHandler(RequestHandler):
    REQUEST_NAME = "EnableProbeTagRequest"

    @staticmethod
    def get_request_name():
        return EnableProbeTagRequestHandler.REQUEST_NAME

    @staticmethod
    def get_request_cls():
        return EnableProbeTagRequest

    @staticmethod
    def handle_request(request):
        application_info = Application.get_application_info()
        try:
            tag = request.get_tag()
            client=request.get_client()
            tag_manager=TagManager().instance()
            tag_manager.enable_tag(tag, client)
            return EnableProbeTagResponse(request_id=request.get_id(), client=request.get_client(),
                                             application_instance_id=application_info.get('applicationInstanceId'))
        except Exception as e:
            tp = EnableProbeTagResponse(request_id=request.get_id(), client=request.get_client(),
                                           application_instance_id=application_info.get('applicationInstanceId'),
                                           erroneous=True)
            tp.set_error(e)
            return tp
