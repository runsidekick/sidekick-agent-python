from tracepointdebug.config import config_names

CONFIG_METADATA = {
    config_names.SIDEKICK_APIKEY: {
        'type': 'string',
    },
    config_names.SIDEKICK_DEBUG_ENABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.SIDEKICK_ERROR_STACK_ENABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.SIDEKICK_ERROR_COLLECTION_ENABLE_CAPTURE_FRAME: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.SIDEKICK_PRINT_CLOSED_SOCKET_DATA: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.SIDEKICK_APPLICATION_ID: {
        'type': 'string',
    },
    config_names.SIDEKICK_APPLICATION_INSTANCE_ID: {
        'type': 'string',
    },
    config_names.SIDEKICK_APPLICATION_NAME: {
        'type': 'string',
    },
    config_names.SIDEKICK_APPLICATION_STAGE: {
        'type': 'string',
    },
    config_names.SIDEKICK_APPLICATION_DOMAIN_NAME: {
        'type': 'string',
        'defaultValue': 'API',
    },
    config_names.SIDEKICK_APPLICATION_CLASS_NAME: {
        'type': 'string',
        'defaultValue': 'AWS-Lambda',
    },
    config_names.SIDEKICK_APPLICATION_VERSION: {
        'type': 'string',
    },
    config_names.SIDEKICK_APPLICATION_TAG_PREFIX: {
        'type': 'any',
    },
}
