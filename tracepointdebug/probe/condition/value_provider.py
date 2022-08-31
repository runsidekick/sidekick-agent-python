import abc

ABC = abc.ABCMeta('ABC', (object,), {})


class ValueProvider(ABC):

    @abc.abstractmethod
    def get_value(self, condition_context):
        pass
