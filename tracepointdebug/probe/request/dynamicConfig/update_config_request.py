from tracepointdebug.broker.request.base_request import BaseRequest


class UpdateConfigRequest(BaseRequest):

    def __init__(self, request):
        super(UpdateConfigRequest, self).__init__(id=request.get("id"), client=request.get("client"))
        self.config = request.get("config", {})

    def get_id(self):
        return self.id

    def get_config(self):
        return self.config

    def get_name(self):
        return self.__class__.__name__

    def get_client(self):
        return self.client
