from tracepointdebug.application.application import Application
from tracepointdebug.broker.handler.request.request_handler import RequestHandler
from tracepointdebug.probe.request.logPoint.put_log_point_request import PutLogPointRequest
from tracepointdebug.probe.response.logPoint.put_log_point_response import PutLogPointResponse
from tracepointdebug.probe.breakpoints.logpoint import LogPointManager
from tracepointdebug.utils.validation import validate_file_name_and_line_no


class PutLogPointRequestHandler(RequestHandler):
    REQUEST_NAME = "PutLogPointRequest"

    @staticmethod
    def get_request_name():
        return PutLogPointRequestHandler.REQUEST_NAME

    @staticmethod
    def get_request_cls():
        return PutLogPointRequest

    @staticmethod
    def handle_request(request):
        application_info = Application.get_application_info()
        try:
            validate_file_name_and_line_no(request.file, request.line_no)
            log_point_manager = LogPointManager.instance()
            log_point_manager.put_log_point(request.log_point_id, request.file, request.file_hash,
                                                request.line_no,
                                                request.get_client(), request.expire_secs,
                                                request.expire_count, False, 
                                                request.log_expression, request.condition,
                                                request.log_level, request.stdout_enabled, request.tags)

            log_point_manager.publish_application_status()
            if request.get_client() is not None:
                log_point_manager.publish_application_status(request.get_client())

            return PutLogPointResponse(request_id=request.get_id(), client=request.get_client(),
                                         application_instance_id=application_info.get('applicationInstanceId'))
        except Exception as e:
            tp = PutLogPointResponse(request_id=request.get_id(), client=request.get_client(),
                                       application_instance_id=application_info.get('applicationInstanceId'),
                                       erroneous=True)
            tp.set_error(e)
            return tp
