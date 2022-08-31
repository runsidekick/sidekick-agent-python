from tracepointdebug.application.config_aware_application_info_provider import ConfigAwareApplicationInfoProvider


class Application(object):
    application_info_provider = ConfigAwareApplicationInfoProvider()

    @staticmethod
    def get_application_info():
        return Application.application_info_provider.get_application_info()

    @staticmethod
    def get_application_info_provider():
        return Application.application_info_provider

    @staticmethod
    def set_application_info_provider(application_info_provider):
        Application.application_info_provider = application_info_provider
