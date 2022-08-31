import socket
import sys
import uuid

from tracepointdebug.application.application_info_provider import ApplicationInfoProvider
from tracepointdebug.config import config_names
from tracepointdebug.config.config_provider import ConfigProvider


class ConfigAwareApplicationInfoProvider(ApplicationInfoProvider):
    def __init__(self):
        self.application_info = ConfigAwareApplicationInfoProvider.get_application_info_from_config()
        if self.application_info.get('applicationId') is None:
            self.application_info['applicationId'] = ConfigAwareApplicationInfoProvider.get_default_application_id(
                self.application_info['applicationName'])
        if self.application_info.get('applicationInstanceId') is None:
            self.application_info[
                'applicationInstanceId'] = ConfigAwareApplicationInfoProvider.get_default_application_instance_id(
                self.application_info['applicationName'])

    def get_application_info(self):
        return self.application_info

    @staticmethod
    def get_application_info_from_config():
        return {
            'applicationId': ConfigProvider.get(config_names.SIDEKICK_APPLICATION_ID),
            'applicationInstanceId': ConfigProvider.get(config_names.SIDEKICK_APPLICATION_INSTANCE_ID),
            'applicationDomainName': ConfigProvider.get(config_names.SIDEKICK_APPLICATION_DOMAIN_NAME, ''),
            'applicationClassName': ConfigProvider.get(config_names.SIDEKICK_APPLICATION_CLASS_NAME, ''),
            'applicationName': ConfigProvider.get(config_names.SIDEKICK_APPLICATION_NAME, ''),
            'applicationVersion': ConfigProvider.get(config_names.SIDEKICK_APPLICATION_VERSION, ''),
            'applicationStage': ConfigProvider.get(config_names.SIDEKICK_APPLICATION_STAGE, ''),
            'applicationRegion': ConfigProvider.get(config_names.SIDEKICK_APPLICATION_REGION, ''),
            'applicationRuntime': 'python',
            'applicationRuntimeVersion': str(sys.version_info[0]),
            'applicationTags': ApplicationInfoProvider.parse_application_tags()
        }

    @staticmethod
    def get_default_application_id(app_name):
        return "python:" + app_name

    @staticmethod
    def get_default_application_instance_id(app_name):
        hostname = socket.gethostname()
        return '{app_name}:{id}@{hostname}'.format(app_name=app_name, id=str(uuid.uuid4()), hostname=hostname)
