from tracepointdebug.broker.request.base_request import BaseRequest


class RemoveTracePointRequest(BaseRequest):

    def __init__(self, request):
        super(RemoveTracePointRequest, self).__init__(id=request.get("id"), client=request.get("client"))
        self.trace_point_id = request.get("tracePointId")

    def get_id(self):
        return self.id

    def get_trace_point_id(self):
        return self.trace_point_id

    def get_name(self):
        return self.__class__.__name__

    def get_client(self):
        return self.client
