import abc

ABC = abc.ABCMeta('ABC', (object,), {})


class Response(ABC):

    @abc.abstractmethod
    def get_request_id(self):
        pass

    @abc.abstractmethod
    def get_name(self):
        pass

    @abc.abstractmethod
    def get_client(self):
        pass
    
    @staticmethod
    def get_type():
        return "Response"

    @staticmethod
    def get_source():
        return "Agent"

    @abc.abstractmethod
    def is_erroneous(self):
        pass

    @abc.abstractmethod
    def get_error_code(self):
        pass

    @abc.abstractmethod
    def get_error_type(self):
        pass
