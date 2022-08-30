from tracepointdebug.broker.event.base_event import BaseEvent


class ApplicationStatusEvent(BaseEvent):
    EVENT_NAME = "ApplicationStatusEvent"

    def __init__(self, client=None, application=None):
        super(ApplicationStatusEvent, self).__init__(client=client)
        self._application = application

    @property
    def application(self):
        return self._application

    @application.setter
    def application(self, value):
        self._application = value

    def to_json(self):
        return {
            "name": self.name,
            "type": self.get_type(),
            "application": self.application,
            "id": self.id,
            "sendAck": self.send_ack,
            "applicationInstanceId": self.application.instance_id,
            "applicationName": self.application.name,
            "client": self.client,
            "time": self.time,
            "hostName": self.application.hostname,
            "runtime": self.application.runtime,
        }
