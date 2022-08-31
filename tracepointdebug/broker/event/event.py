import abc

ABC = abc.ABCMeta('ABC', (object,), {})


class Event(ABC):

    def get_type(self):
        return "Event"

    @property
    @abc.abstractmethod
    def name(self):
        pass

    @property
    @abc.abstractmethod
    def id(self):
        pass

    @property
    @abc.abstractmethod
    def send_ack(self):
        pass

    @property
    @abc.abstractmethod
    def client(self):
        pass

    @property
    @abc.abstractmethod
    def time(self):
        pass

    @property
    @abc.abstractmethod
    def hostname(self):
        pass

    @property
    @abc.abstractmethod
    def application_name(self):
        pass

    @property
    @abc.abstractmethod
    def application_instance_id(self):
        pass
