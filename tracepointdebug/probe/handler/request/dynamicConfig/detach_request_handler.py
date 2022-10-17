from tracepointdebug.application.application import Application
from tracepointdebug.broker.handler.request.request_handler import RequestHandler
from tracepointdebug.probe.dynamicConfig.dynamic_config_manager import DynamicConfigManager
from tracepointdebug.probe.request.dynamicConfig.detach_request import DetachRequest
from tracepointdebug.probe.response.dynamicConfig.detach_response import DetachResponse


class DetachRequestHandler(RequestHandler):
    REQUEST_NAME = "DetachRequest"

    @staticmethod
    def get_request_name():
        return DetachRequestHandler.REQUEST_NAME

    @staticmethod
    def get_request_cls():
        return DetachRequest

    @staticmethod
    def handle_request(request):
        application_info = Application.get_application_info()
        try:
            dynamic_config_manager = DynamicConfigManager.instance()

            dynamic_config_manager.handle_detach()

            dynamic_config_manager.publish_application_status()
            if request.get_client() is not None:
                dynamic_config_manager.publish_application_status(request.get_client())

            return DetachResponse(request_id=request.get_id(), client=request.get_client(),
                                             application_instance_id=application_info.get('applicationInstanceId'))
        except Exception as e:
            dr = DetachResponse(request_id=request.get_id(), client=request.get_client(),
                                           application_instance_id=application_info.get('applicationInstanceId'),
                                           erroneous=True)
            dr.set_error(e)
            return dr
