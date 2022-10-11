from tracepointdebug.broker.event.base_event import BaseEvent


class ErrorStackSnapshotEvent(BaseEvent):
    EVENT_NAME = "ErrorStackSnapshotEvent"

    def __init__(self, error_stack_id, file, line_no, method_name, error, frames):
        super(ErrorStackSnapshotEvent, self).__init__()
        self.error_stack_id = error_stack_id
        self.file = file
        self.line_no = line_no
        self.method_name = method_name
        self.error = error
        self.frames = frames

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "sendAck": self.send_ack,
            "fileName": self.file,
            "className": self.file,
            "lineNo": self.line_no,
            "type": self.get_type(),
            "methodName": self.method_name,
            "errorStackId": self.error_stack_id,
            "applicationInstanceId": self.application_instance_id,
            "applicationName": self.application_name,
            "time": self.time,
            "hostName": self.hostname,
            "frames": self.frames,
            "error": self.error
        }
