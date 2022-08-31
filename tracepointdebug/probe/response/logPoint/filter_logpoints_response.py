from tracepointdebug.broker.response.base_response import BaseResponse

from typing import List

class FilterLogPointsResponse(BaseResponse):

    def __init__(self, logPoints=None, requestId=None, 
                source=None, applicationInstanceId=None, 
                erroneous=False, errorCode=None,
                errorType=None, errorMessage=None, **opts):
        super(FilterLogPointsResponse, self).__init__(request_id=requestId, 
                client=source, application_instance_id=applicationInstanceId, 
                erroneous=erroneous, error_code=errorCode,
                error_type=errorType, error_message=errorMessage)
        
        self._log_points = logPoints


    @property
    def log_points(self):
        return self._log_points

    
    @log_points.setter
    def log_points(self, log_points):
        self._log_points = log_points