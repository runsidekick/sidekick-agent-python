from tracepointdebug.broker.event.base_event import BaseEvent


class PutTracePointFailedEvent(BaseEvent):
    EVENT_NAME = "PutTracePointFailedEvent"

    def __init__(self, file, line_no, error_code, error_message):
        super(PutTracePointFailedEvent, self).__init__()
        self.file = file
        self.line_no = line_no
        self.error_code = error_code
        self.error_message = error_message

    def to_json(self):
        return {
            "name": self.name,
            "type": self.get_type(),
            "id": self.id,
            "fileName": self.file,
            "lineNo": self.line_no,
            "sendAck": self.send_ack,
            "applicationInstanceId": self.application_instance_id,
            "applicationName": self.application_name,
            "client": self.client,
            "time": self.time,
            "hostName": self.hostname,
            "errorCode": self.error_code,
            "errorMessage": self.error_message
        }
