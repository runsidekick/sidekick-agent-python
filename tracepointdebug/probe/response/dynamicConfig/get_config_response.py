from tracepointdebug.broker.response.base_response import BaseResponse

class GetConfigResponse(BaseResponse):

    def __init__(self, config=None, requestId=None, 
                source=None, applicationInstanceId=None, 
                erroneous=False, errorCode=None,
                errorType=None, errorMessage=None, **opts):
        super(GetConfigResponse, self).__init__(request_id=requestId, 
                client=source, application_instance_id=applicationInstanceId, 
                erroneous=erroneous, error_code=errorCode,
                error_type=errorType, error_message=errorMessage)
        
        self._config = config


    @property
    def config(self):
        return self._config

    
    @config.setter
    def config(self, config):
        self._config = config