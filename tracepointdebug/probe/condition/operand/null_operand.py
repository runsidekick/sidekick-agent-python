from tracepointdebug.probe.condition.operand.operand import Operand


class NullOperand(Operand):

    def get_value(self, condition_context):
        return None

    def eq(self, operand, condition_context):
        return operand.get_value(condition_context) is None

    def ne(self, operand, condition_context):
        return operand.get_value(condition_context) is not None

    def lt(self, operand, condition_context):
        return False

    def le(self, operand, condition_context):
        return False

    def gt(self, operand, condition_context):
        return False

    def ge(self, operand, condition_context):
        return False
