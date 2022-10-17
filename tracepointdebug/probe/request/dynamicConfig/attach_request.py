from tracepointdebug.broker.request.base_request import BaseRequest


class AttachRequest(BaseRequest):

    def __init__(self, request):
        super(AttachRequest, self).__init__(id=request.get("id"), client=request.get("client"))

    def get_id(self):
        return self.id

    def get_name(self):
        return self.__class__.__name__

    def get_client(self):
        return self.client
