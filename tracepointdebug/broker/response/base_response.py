from tracepointdebug.broker.response.response import Response
from tracepointdebug.probe.coded_exception import CodedException


class BaseResponse(Response):

    def __init__(self, request_id=None, client=None, application_instance_id=None, erroneous=False, error_code=None,
                 error_type=None, error_message=None):
        self.request_id = request_id
        self.client = client
        self.application_instance_id = application_instance_id
        self.erroneous = erroneous
        self.error_code = error_code
        self.error_type = error_type
        self.name = self.__class__.__name__
        self.error_message = error_message

    def get_request_id(self):
        return self.request_id

    def get_name(self):
        return self.name

    def get_client(self):
        return self.client

    def get_application_instance_id(self):
        return self.application_instance_id

    def is_erroneous(self):
        return self.erroneous

    def get_error_code(self):
        return self.error_code

    def get_error_type(self):
        return self.error_type

    def set_error(self, exception):
        if isinstance(exception, CodedException):
            self.error_code = exception.code

        self.erroneous = True
        self.error_type = exception.__class__.__name__
        self.error_message = str(exception)

    def to_json(self):
        return {
            "name": self.get_name(),
            "requestId": self.request_id,
            "applicationInstanceId": self.application_instance_id,
            "client": self.client,
            "erroneous": self.erroneous,
            "errorCode": self.error_code,
            "errorMessage": self.error_message,
            "source": self.get_source(),
            "type": self.get_type()
        }
