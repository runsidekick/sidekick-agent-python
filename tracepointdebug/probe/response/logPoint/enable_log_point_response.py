from tracepointdebug.broker.response.base_response import BaseResponse


class EnableLogPointResponse(BaseResponse):

    def __init__(self, request_id=None, client=None, application_instance_id=None, erroneous=False, error_code=None,
                 error_type=None, error_message=None):
        super(EnableLogPointResponse, self).__init__(request_id, client, application_instance_id, erroneous,
                                                       error_code, error_type, error_message)
