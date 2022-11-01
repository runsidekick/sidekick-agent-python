from tracepointdebug.broker.request.base_request import BaseRequest
from tracepointdebug.probe import constants


class PutLogPointRequest(BaseRequest):

    def __init__(self, request):
        super(PutLogPointRequest, self).__init__(id=request.get("id"), client=request.get("client"))
        self.log_point_id = request.get("logPointId")
        self.file = request.get("fileName", None)
        self.file_hash = request.get("fileHash")
        self.line_no = request.get("lineNo", -1)
        self.condition = request.get("conditionExpression")
        self.log_expression = request.get("logExpression")
        self.tags = request.get("tags", set())
        self.expire_secs = min(int(request.get("expireSecs", constants.LOGPOINT_DEFAULT_EXPIRY_SECS)),
                               constants.LOGPOINT_MAX_EXPIRY_SECS)
        self.expire_count = min(int(request.get("expireCount", constants.LOGPOINT_DEFAULT_EXPIRY_COUNT)),
                                constants.LOGPOINT_MAX_EXPIRY_COUNT)

        self.log_level = request.get("logLevel", "INFO")
        self.stdout_enabled = request.get("stdoutEnabled", False)

    def get_id(self):
        return self.id

    def get_log_point_id(self):
        return self.log_point_id

    def get_name(self):
        return self.__class__.__name__

    def get_client(self):
        return self.client
