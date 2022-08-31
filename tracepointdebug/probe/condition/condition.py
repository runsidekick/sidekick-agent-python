import abc

ABC = abc.ABCMeta('ABC', (object,), {})


class Condition(ABC):

    @abc.abstractmethod
    def evaluate(self, condition_context):
        pass
