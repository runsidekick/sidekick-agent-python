from tracepointdebug.broker.request.base_request import BaseRequest
from tracepointdebug.probe import constants


class UpdateTracePointRequest(BaseRequest):

    def __init__(self, request):
        super(UpdateTracePointRequest, self).__init__(id=request.get("id"), client=request.get("client"))
        self.trace_point_id = request.get("tracePointId")
        self.enable_tracing = request.get("enableTracing")
        self.condition = request.get("conditionExpression")
        self.disable = request.get("disable")
        self.tags = request.get("tags", set())
        self.expire_secs = min(int(request.get("expireSecs", constants.TRACEPOINT_DEFAULT_EXPIRY_SECS)),
                               constants.TRACEPOINT_MAX_EXPIRY_SECS)
        self.expire_count = min(int(request.get("expireCount", constants.TRACEPOINT_DEFAULT_EXPIRY_COUNT)),
                                constants.TRACEPOINT_MAX_EXPIRY_COUNT)

    def get_id(self):
        return self.id

    def get_trace_point_id(self):
        return self.trace_point_id

    def get_name(self):
        return self.__class__.__name__

    def get_client(self):
        return self.client
