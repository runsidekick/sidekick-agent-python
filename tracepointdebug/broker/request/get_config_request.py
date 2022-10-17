from tracepointdebug.broker.request.base_request import BaseRequest

from uuid import uuid4
from tracepointdebug.broker.application.application_filter import ApplicationFilter

class GetConfigRequest(BaseRequest):
    

    def __init__(self, name, version, stage, customTags):
        super(GetConfigRequest, self).__init__(str(uuid4()))
        self._application_filter = ApplicationFilter()
        self._application_filter.name = name
        self._application_filter.version = version
        self._application_filter.stage = stage
        self._application_filter.custom_tags = customTags

    def get_id(self):
        return self.id


    def get_name(self):
        return self.__class__.__name__

    
    @property
    def application_filter(self):
        return self._application_filter

    
    @application_filter.setter
    def application_filter(self, application_filter):
        self._application_filter = application_filter


    def to_json(self):
        return { 
                "type": self.get_type(),
                "name": self.get_name(),
                "id": self.id,
                "applicationFilter": self.application_filter,
                "applicationFilterName": self.application_filter.name,
                "applicationFilterStage": self.application_filter.stage,
                "applicationFilterVersion": self.application_filter.version,
                "applicationFilterCustomTags": self.application_filter.custom_tags,
            }