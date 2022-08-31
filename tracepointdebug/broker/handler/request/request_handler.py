import abc

ABC = abc.ABCMeta('ABC', (object,), {})


class RequestHandler(ABC):

    @staticmethod
    @abc.abstractmethod
    def get_request_name():
        pass

    @staticmethod
    @abc.abstractmethod
    def get_request_cls():
        pass

    @staticmethod
    @abc.abstractmethod
    def handle_request(request):
        pass
