from tracepointdebug.application.application import Application
from tracepointdebug.broker.handler.request.request_handler import RequestHandler
from tracepointdebug.probe.request.logPoint.update_log_point_request import UpdateLogPointRequest
from tracepointdebug.probe.response.logPoint.update_log_point_response import UpdateLogPointResponse
from tracepointdebug.probe.breakpoints.logpoint import LogPointManager


class UpdateLogPointRequestHandler(RequestHandler):
    REQUEST_NAME = "UpdateLogPointRequest"

    @staticmethod
    def get_request_name():
        return UpdateLogPointRequestHandler.REQUEST_NAME

    @staticmethod
    def get_request_cls():
        return UpdateLogPointRequest

    @staticmethod
    def handle_request(request):
        application_info = Application.get_application_info()
        try:
            log_point_manager = LogPointManager.instance()
            log_point_manager.update_log_point(request.log_point_id,
                                                   request.get_client(), request.expire_secs,
                                                   request.expire_count, request.log_expression, request.condition,
                                                   disabled=request.disable, log_level=request.log_level, 
                                                   stdout_enabled=request.stdout_enabled, tags=request.tags)

            log_point_manager.publish_application_status()
            if request.get_client() is not None:
                log_point_manager.publish_application_status(request.get_client())

            return UpdateLogPointResponse(request_id=request.get_id(), client=request.get_client(),
                                            application_instance_id=application_info.get('applicationInstanceId'))
        except Exception as e:
            tp = UpdateLogPointResponse(request_id=request.get_id(), client=request.get_client(),
                                          application_instance_id=application_info.get('applicationInstanceId'),
                                          erroneous=True)
            tp.set_error(e)
            return tp
