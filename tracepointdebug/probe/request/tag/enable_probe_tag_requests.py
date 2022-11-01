from tracepointdebug.broker.request.base_request import BaseRequest


class EnableProbeTagRequest(BaseRequest):

    def __init__(self, request):
        super(EnableProbeTagRequest, self).__init__(id=request.get("id"), client=request.get("client"))
        self.tag = request.get("tag")

    def get_id(self):
        return self.id

    def get_tag(self):
        return self.tag

    def get_name(self):
        return self.__class__.__name__

    def get_client(self):
        return self.client
