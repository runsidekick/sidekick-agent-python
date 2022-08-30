from tracepointdebug.broker.event.base_event import BaseEvent


class LogPointEvent(BaseEvent):
    EVENT_NAME = "LogPointEvent"

    def __init__(self, log_point_id, file, line_no, method_name, log_message, created_at):
        super(LogPointEvent, self).__init__()
        self.log_point_id = log_point_id
        self.file = file
        self.line_no = line_no
        self.method_name = method_name
        self.log_message = log_message
        self.created_at = created_at

    def to_json(self):
        return {
            "logPointId": self.log_point_id,
            "name": self.name,
            "type": self.get_type(),
            "id": self.id,
            "fileName": self.file,
            "lineNo": self.line_no,
            "methodName": self.method_name,
            "logMessage": self.log_message,
            "sendAck": self.send_ack,
            "applicationInstanceId": self.application_instance_id,
            "applicationName": self.application_name,
            "client": self.client,
            "time": self.time,
            "hostName": self.hostname,
            "createdAt": self.created_at
        }
