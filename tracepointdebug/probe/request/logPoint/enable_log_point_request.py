from tracepointdebug.broker.request.base_request import BaseRequest


class EnableLogPointRequest(BaseRequest):

    def __init__(self, request):
        super(EnableLogPointRequest, self).__init__(id=request.get("id"), client=request.get("client"))
        self.log_point_id = request.get("logPointId")

    def get_id(self):
        return self.id

    def get_log_point_id(self):
        return self.log_point_id

    def get_name(self):
        return self.__class__.__name__

    def get_client(self):
        return self.client
