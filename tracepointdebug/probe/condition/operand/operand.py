import abc

ABC = abc.ABCMeta('ABC', (object,), {})


class Operand(ABC):

    @abc.abstractmethod
    def get_value(self, condition_context):
        pass

    @abc.abstractmethod
    def eq(self, operand, condition_context):
        return False

    @abc.abstractmethod
    def ne(self, operand, condition_context):
        return False

    @abc.abstractmethod
    def lt(self, operand, condition_context):
        return False

    @abc.abstractmethod
    def le(self, operand, condition_context):
        return False

    @abc.abstractmethod
    def gt(self, operand, condition_context):
        return False

    @abc.abstractmethod
    def ge(self, operand, condition_context):
        return False
