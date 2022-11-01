from tracepointdebug.broker.event.base_event import BaseEvent


class TracePointRateLimitEvent(BaseEvent):
    EVENT_NAME = "TracePointRateLimitEvent"

    def __init__(self, file, line_no):
        super(TracePointRateLimitEvent, self).__init__()
        self.file = file
        self.line_no = line_no

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
            "hostName": self.hostname
        }
