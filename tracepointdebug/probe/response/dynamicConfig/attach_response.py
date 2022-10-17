from tracepointdebug.broker.response.base_response import BaseResponse

class AttachResponse(BaseResponse):

    def __init__(self, requestId=None, 
                source=None, applicationInstanceId=None, 
                erroneous=False, errorCode=None,
                errorType=None, errorMessage=None, **opts):
        super(AttachResponse, self).__init__(request_id=requestId, 
                client=source, application_instance_id=applicationInstanceId, 
                erroneous=erroneous, error_code=errorCode,
                error_type=errorType, error_message=errorMessage)