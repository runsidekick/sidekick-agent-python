from tracepointdebug.probe.condition.operand.operand import Operand


class ObjectOperand(Operand):

    def __init__(self, value_provider):
        self.value_provider = value_provider

    def get_value(self, condition_context):
        return self.value_provider.get_value(condition_context)

    def eq(self, operand, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val == operand.get_value(condition_context)

    def ne(self, operand, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val != operand.get_value(condition_context)

    def lt(self, operand, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val < operand.get_value(condition_context)

    def le(self, operand, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val <= operand.get_value(condition_context)

    def gt(self, operand, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val > operand.get_value(condition_context)

    def ge(self, operand, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val >= operand.get_value(condition_context)
