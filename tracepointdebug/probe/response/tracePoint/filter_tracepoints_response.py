from tracepointdebug.broker.response.base_response import BaseResponse

from typing import List

class FilterTracePointsResponse(BaseResponse):

    def __init__(self, tracePoints=None, requestId=None, 
                source=None, applicationInstanceId=None, 
                erroneous=False, errorCode=None,
                errorType=None, errorMessage=None, **opts):
        super(FilterTracePointsResponse, self).__init__(request_id=requestId, 
                client=source, application_instance_id=applicationInstanceId, 
                erroneous=erroneous, error_code=errorCode,
                error_type=errorType, error_message=errorMessage)
        
        self._trace_points = tracePoints


    @property
    def trace_points(self):
        return self._trace_points

    
    @trace_points.setter
    def trace_points(self, trace_points):
        self._trace_points = trace_points