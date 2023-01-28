import json
from tracepointdebug.probe.dynamicConfig.dynamic_config_manager import DynamicConfigManager

from tracepointdebug.probe.encoder import to_json
from tracepointdebug.probe.handler import ( DisableTracePointRequestHandler, 
    EnableTracePointRequestHandler, PutTracePointRequestHandler, RemoveTracePointRequestHandler, 
    UpdateTracePointRequestHandler, FilterTracePointsResponseHandler, DisableLogPointRequestHandler, 
    EnableLogPointRequestHandler, PutLogPointRequestHandler, RemoveLogPointRequestHandler, UpdateLogPointRequestHandler,
    FilterLogPointsResponseHandler, EnableProbeTagRequestHandler, DisableProbeTagRequestHandler, GetConfigResponseHandler, 
    AttachRequestHandler, DetachRequestHandler, UpdateConfigRequestHandler, RemoveProbeTagRequestHandler)
from tracepointdebug.utils import debug_logger

MESSAGE_REQUEST_TYPE = "Request"
MESSAGE_RESPONSE_TYPE = "Response"

REQUEST_HANDLER_MAP = {
    "DisableTracePointRequest": DisableTracePointRequestHandler,
    "EnableTracePointRequest": EnableTracePointRequestHandler,
    "PutTracePointRequest": PutTracePointRequestHandler,
    "RemoveTracePointRequest": RemoveTracePointRequestHandler,
    "UpdateTracePointRequest": UpdateTracePointRequestHandler,

    "DisableLogPointRequest": DisableLogPointRequestHandler,
    "EnableLogPointRequest": EnableLogPointRequestHandler,
    "PutLogPointRequest": PutLogPointRequestHandler,
    "RemoveLogPointRequest": RemoveLogPointRequestHandler,
    "UpdateLogPointRequest": UpdateLogPointRequestHandler,

    "EnableProbeTagRequest": EnableProbeTagRequestHandler,
    "DisableProbeTagRequest": DisableProbeTagRequestHandler,
    "RemoveProveTagRequest": RemoveProbeTagRequestHandler,

    "UpdateConfigRequest": UpdateConfigRequestHandler,
    "AttachRequest": AttachRequestHandler,
    "DetachRequest": DetachRequestHandler
}

RESPONSE_HANDLER_MAP = {
    "FilterTracePointsResponse": FilterTracePointsResponseHandler,
    "FilterLogPointsResponse": FilterLogPointsResponseHandler,
    "GetConfigResponse": GetConfigResponseHandler
}


class BrokerMessageCallback(object):

    def on_message(self, broker_client, message):
        try:
            dynamic_config_manager = DynamicConfigManager.instance()
            attached = dynamic_config_manager.attached
            message = json.loads(message)

            message_type = message.get("type", None)
            if attached:
                if message_type == MESSAGE_REQUEST_TYPE and message.get("name") != "AttachRequest":
                    self._handle_requests(message, broker_client)
                elif message_type == MESSAGE_RESPONSE_TYPE:
                    self._handle_responses(message)
            else:
                if message_type == MESSAGE_REQUEST_TYPE and message.get("name") == "AttachRequest":
                    self._handle_requests(message, broker_client)
                else:
                    return
        except Exception as e:
            debug_logger(e)

    def _handle_requests(self, message, broker_client):
        handler = REQUEST_HANDLER_MAP.get(message.get("name"))
        if handler is not None:
            request = handler.get_request_cls()(message)
            response = handler.handle_request(request)
            serialized = to_json(response)
            broker_client.send(serialized)
        else:
            debug_logger("No request handler could be found for message with name {}: {}".format(message.get("name"),
                                                                                    message))

    def _handle_responses(self, message):
        handler = RESPONSE_HANDLER_MAP.get(message.get("name"))
        if handler is not None:
            response = handler.get_response_cls()(**message)
            handler.handle_response(response)
        else:
            debug_logger("No response handler could be found for message with name {}: {}".format(message.get("name"),
                                                                                              message))