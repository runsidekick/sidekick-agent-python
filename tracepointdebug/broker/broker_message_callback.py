import json

from tracepointdebug.probe.encoder import to_json
from tracepointdebug.probe.handler import ( DisableTracePointRequestHandler, 
    EnableTracePointRequestHandler, PutTracePointRequestHandler, RemoveTracePointRequestHandler, 
    UpdateTracePointRequestHandler, FilterTracePointsResponseHandler )
from tracepointdebug.probe.handler.request.logPoint.disable_log_point_request_handler import DisableLogPointRequestHandler
from tracepointdebug.probe.handler.request.logPoint.enable_log_point_request_handler import EnableLogPointRequestHandler
from tracepointdebug.probe.handler.request.logPoint.put_log_point_request_handler import PutLogPointRequestHandler
from tracepointdebug.probe.handler.request.logPoint.remove_log_point_request_handler import RemoveLogPointRequestHandler
from tracepointdebug.probe.handler.request.logPoint.update_log_point_request_handler import UpdateLogPointRequestHandler
from tracepointdebug.probe.handler.response.filter_logpoints_response_handler import FilterLogPointsResponseHandler

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
    "UpdateLogPointRequest": UpdateLogPointRequestHandler
}

RESPONSE_HANDLER_MAP = {
    "FilterTracePointsResponse": FilterTracePointsResponseHandler,
    "FilterLogPointsResponse": FilterLogPointsResponseHandler
}


class BrokerMessageCallback(object):

    def on_message(self, broker_client, message):
        try:
            message = json.loads(message)

            message_type = message.get("type", None)

            if message_type == MESSAGE_REQUEST_TYPE:
                handler = REQUEST_HANDLER_MAP.get(message.get("name"))
                if handler is not None:
                    request = handler.get_request_cls()(message)
                    response = handler.handle_request(request)
                    serialized = to_json(response)
                    broker_client.send(serialized)
                else:
                    print("No request handler could be found for message with name {}: {}".format(message.get("name"),
                                                                                              message))
            elif message_type == MESSAGE_RESPONSE_TYPE:
                handler = RESPONSE_HANDLER_MAP.get(message.get("name"))
                if handler is not None:
                    response = handler.get_response_cls()(**message)
                    handler.handle_response(response)
                else:
                    print("No response handler could be found for message with name {}: {}".format(message.get("name"),
                                                                                              message))

        except Exception as e:
            print(e)
