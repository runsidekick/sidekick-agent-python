from tracepointdebug.application.application import Application
from tracepointdebug.broker.handler.request.request_handler import RequestHandler
from tracepointdebug.probe.request.logPoint.enable_log_point_request import EnableLogPointRequest
from tracepointdebug.probe.response.logPoint.enable_log_point_response import EnableLogPointResponse
from tracepointdebug.probe.breakpoints.logpoint import LogPointManager


class EnableLogPointRequestHandler(RequestHandler):
    REQUEST_NAME = "EnableLogPointRequest"

    @staticmethod
    def get_request_name():
        return EnableLogPointRequestHandler.REQUEST_NAME

    @staticmethod
    def get_request_cls():
        return EnableLogPointRequest

    @staticmethod
    def handle_request(request):
        application_info = Application.get_application_info()
        try:
            log_point_manager = LogPointManager.instance()
            log_point_manager.enable_log_point(request.log_point_id, request.get_client())

            log_point_manager.publish_application_status()
            if request.get_client() is not None:
                log_point_manager.publish_application_status(request.get_client())

            return EnableLogPointResponse(request_id=request.get_id(), client=request.get_client(),
                                            application_instance_id=application_info.get('applicationInstanceId'))
        except Exception as e:
            tp = EnableLogPointResponse(request_id=request.get_id(), client=request.get_client(),
                                          application_instance_id=application_info.get('applicationInstanceId'),
                                          erroneous=True)
            tp.set_error(e)
            return tp
