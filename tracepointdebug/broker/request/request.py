import abc

ABC = abc.ABCMeta('ABC', (object,), {})


class Request(ABC):

    @staticmethod
    def get_type():
        return "Request"

    @abc.abstractmethod
    def get_id(self):
        pass

    @abc.abstractmethod
    def get_name(self):
        pass

    @abc.abstractmethod
    def get_client(self):
        pass
