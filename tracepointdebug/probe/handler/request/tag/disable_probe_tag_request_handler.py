from tracepointdebug.application.application import Application
from tracepointdebug.broker.handler.request.request_handler import RequestHandler
from tracepointdebug.probe.request.tag.disable_probe_tag_requests import DisableProbeTagRequest
from tracepointdebug.probe.response.tag.disable_probe_tag_response import DisableProbeTagResponse
from tracepointdebug.probe.tag_manager import TagManager


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
            tag = request.get_tag()
            client = request.get_client()
            tag_manager = TagManager().instance()
            tag_manager.disable_tag(tag, client)
            return DisableProbeTagResponse(request_id=request.get_id(), client=request.get_client(),
                                             application_instance_id=application_info.get('applicationInstanceId'))
        except Exception as e:
            tp = DisableProbeTagResponse(request_id=request.get_id(), client=request.get_client(),
                                           application_instance_id=application_info.get('applicationInstanceId'),
                                           erroneous=True)
            tp.set_error(e)
            return tp
