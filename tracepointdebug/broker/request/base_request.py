from tracepointdebug.broker.request.request import Request


class BaseRequest(Request):

    def __init__(self, id, client=None):
        self.id = id
        self.client = client

    def get_id(self):
        return self.id

    def get_name(self):
        return self.__class__.__name__

    def get_client(self):
        return self.client
