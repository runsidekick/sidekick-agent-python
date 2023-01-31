from tracepointdebug.application.application import Application
from tracepointdebug.broker.handler.request.request_handler import RequestHandler
from tracepointdebug.probe.request.tag.remove_probe_tag_requests import RemoveProbeTagRequest
from tracepointdebug.probe.response.tag.remove_probe_tag_response import RemoveProbeTagResponse
from tracepointdebug.probe.tag_manager import TagManager


class RemoveProbeTagRequestHandler(RequestHandler):
    REQUEST_NAME = "RemoveProbeTagRequest"

    @staticmethod
    def get_request_name():
        return RemoveProbeTagRequestHandler.REQUEST_NAME

    @staticmethod
    def get_request_cls():
        return RemoveProbeTagRequest

    @staticmethod
    def handle_request(request):
        application_info = Application.get_application_info()
        try:
            tag = request.get_tag()
            client = request.get_client()
            tag_manager = TagManager().instance()
            tag_manager.remove_tag(tag, client)
            return RemoveProbeTagResponse(request_id=request.get_id(), client=request.get_client(),
                                             application_instance_id=application_info.get('applicationInstanceId'))
        except Exception as e:
            tp = RemoveProbeTagResponse(request_id=request.get_id(), client=request.get_client(),
                                           application_instance_id=application_info.get('applicationInstanceId'),
                                           erroneous=True)
            tp.set_error(e)
            return tp
