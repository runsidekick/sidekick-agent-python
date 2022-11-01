from tracepointdebug.application.application import Application
from tracepointdebug.broker.handler.request.request_handler import RequestHandler
from tracepointdebug.probe.dynamicConfig.dynamic_config_manager import DynamicConfigManager
from tracepointdebug.probe.request.dynamicConfig.attach_request import AttachRequest
from tracepointdebug.probe.response.dynamicConfig.attach_response import AttachResponse


class AttachRequestHandler(RequestHandler):
    REQUEST_NAME = "AttachRequest"

    @staticmethod
    def get_request_name():
        return AttachRequestHandler.REQUEST_NAME

    @staticmethod
    def get_request_cls():
        return AttachRequest

    @staticmethod
    def handle_request(request):
        application_info = Application.get_application_info()
        try:
            dynamic_config_manager = DynamicConfigManager.instance()

            dynamic_config_manager.handle_attach()

            dynamic_config_manager.publish_application_status()
            if request.get_client() is not None:
                dynamic_config_manager.publish_application_status(request.get_client())

            return AttachResponse(request_id=request.get_id(), client=request.get_client(),
                                             application_instance_id=application_info.get('applicationInstanceId'))
        except Exception as e:
            ar = AttachResponse(request_id=request.get_id(), client=request.get_client(),
                                           application_instance_id=application_info.get('applicationInstanceId'),
                                           erroneous=True)
            ar.set_error(e)
            return ar
