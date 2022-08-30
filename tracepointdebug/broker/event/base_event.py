from tracepointdebug.broker.event.event import Event


class BaseEvent(Event):

    def __init__(self, send_ack=False, client=None, time=None, hostname=None,
                 application_name=None, application_instance_id=None):
        self._name = self.__class__.__name__
        self._id = None
        self._send_ack = send_ack
        self._client = client
        self._time = time
        self._hostname = hostname
        self._application_name = application_name
        self._application_instance_id = application_instance_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, _name):
        self._name = _name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, _id):
        self._id = _id

    @property
    def send_ack(self):
        return self._send_ack

    @send_ack.setter
    def send_ack(self, value):
        self._send_ack = value

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, value):
        self._hostname = value

    @property
    def application_name(self):
        return self._application_name

    @application_name.setter
    def application_name(self, value):
        self._application_name = value

    @property
    def application_instance_id(self):
        return self._application_instance_id

    @application_instance_id.setter
    def application_instance_id(self, value):
        self._application_instance_id = value

    def get_type(self):
        return "Event"

    def get_name(self):
        return self.__class__.__name__
