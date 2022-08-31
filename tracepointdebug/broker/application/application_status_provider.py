import abc

ABC = abc.ABCMeta('ABC', (object,), {})


class ApplicationStatusProvider(ABC):

    @abc.abstractmethod
    def provide(self, application_status, client):
        pass
