from tracepointdebug.application.application import Application
from tracepointdebug.broker.handler.request.request_handler import RequestHandler
from tracepointdebug.probe.dynamicConfig.dynamic_config_manager import DynamicConfigManager
from tracepointdebug.probe.request.dynamicConfig.update_config_request import UpdateConfigRequest
from tracepointdebug.probe.response.dynamicConfig.update_config_response import UpdateConfigResponse


class UpdateConfigRequestHandler(RequestHandler):
    REQUEST_NAME = "UpdateConfigRequest"

    @staticmethod
    def get_request_name():
        return UpdateConfigRequestHandler.REQUEST_NAME

    @staticmethod
    def get_request_cls():
        return UpdateConfigRequest

    @staticmethod
    def handle_request(request):
        application_info = Application.get_application_info()
        try:
            dynamic_config_manager = DynamicConfigManager.instance()

            dynamic_config_manager.update_config(request.config)

            dynamic_config_manager.publish_application_status()
            if request.get_client() is not None:
                dynamic_config_manager.publish_application_status(request.get_client())

            return UpdateConfigResponse(request_id=request.get_id(), client=request.get_client(),
                                             application_instance_id=application_info.get('applicationInstanceId'))
        except Exception as e:
            ucr = UpdateConfigResponse(request_id=request.get_id(), client=request.get_client(),
                                           application_instance_id=application_info.get('applicationInstanceId'),
                                           erroneous=True)
            ucr.set_error(e)
            return ucr
