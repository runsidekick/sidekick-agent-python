import abc

ABC = abc.ABCMeta('ABC', (object,), {})


class ResponseHandler(ABC):

    @staticmethod
    @abc.abstractmethod
    def get_response_name():
        pass

    @staticmethod
    @abc.abstractmethod
    def get_response_cls():
        pass

    @staticmethod
    @abc.abstractmethod
    def handle_response(response):
        pass
