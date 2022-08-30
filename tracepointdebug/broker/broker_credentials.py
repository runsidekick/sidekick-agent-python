class BrokerCredentials(object):
    def __init__(self, api_key=None, app_instance_id=None, app_name=None, app_stage=None, app_version=None,
                 hostname=None, runtime=None):
        self.api_key = api_key
        self.app_instance_id = app_instance_id
        self.app_name = app_name
        self.app_stage = app_stage
        self.app_version = app_version
        self.hostname = hostname
        self.runtime = runtime
