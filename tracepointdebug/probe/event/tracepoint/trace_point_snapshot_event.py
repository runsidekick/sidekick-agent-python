from tracepointdebug.broker.event.base_event import BaseEvent


class TracePointSnapshotEvent(BaseEvent):
    EVENT_NAME = "TracePointSnapshotEvent"

    def __init__(self, tracepoint_id, file, line_no, method_name, frames, trace_id=None, transaction_id=None, span_id=None):
        super(TracePointSnapshotEvent, self).__init__()
        self.tracepoint_id = tracepoint_id
        self.file = file
        self.line_no = line_no
        self.method_name = method_name
        self.frames = frames
        self.trace_id = trace_id
        self.transaction_id = transaction_id
        self.span_id = span_id

    def to_json(self):
        return {
            "name": self.name,
            "tracePointId": self.tracepoint_id,
            "type": self.get_type(),
            "id": self.id,
            "fileName": self.file,
            "lineNo": self.line_no,
            "methodName": self.method_name,
            "frames": self.frames,
            "traceId": self.trace_id,
            "transactionId": self.transaction_id,
            "spanId": self.span_id,
            "sendAck": self.send_ack,
            "applicationInstanceId": self.application_instance_id,
            "applicationName": self.application_name,
            "client": self.client,
            "time": self.time,
            "hostName": self.hostname
        }
