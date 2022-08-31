from tracepointdebug.probe.condition.operand.operand import Operand


class TypedOperand(Operand):

    def __init__(self, value_type, value_provider):
        self.value_type = value_type
        self.value_provider = value_provider

    def get_value(self, condition_context):
        value = self.value_provider.get_value(condition_context)
        if value is None or isinstance(value, self.value_type):
            return value
        return None

    def is_eq(self, value, condition_context):
        return False

    def eq(self, operand, condition_context):
        value = operand.get_value(condition_context)
        if value is None or isinstance(value, self.value_type):
            return self.is_eq(value, condition_context)
        return False

    def is_ne(self, value, condition_context):
        return False

    def ne(self, operand, condition_context):
        value = operand.get_value(condition_context)
        if value is None or isinstance(value, self.value_type):
            return self.is_ne(value, condition_context)
        return False

    def is_lt(self, value, condition_context):
        return False

    def lt(self, operand, condition_context):
        value = operand.get_value(condition_context)
        if value is None or isinstance(value, self.value_type):
            return self.is_lt(value, condition_context)
        return False

    def is_le(self, value, condition_context):
        return False

    def le(self, operand, condition_context):
        value = operand.get_value(condition_context)
        if value is None or isinstance(value, self.value_type):
            return self.is_le(value, condition_context)
        return False

    def is_gt(self, value, condition_context):
        return False

    def gt(self, operand, condition_context):
        value = operand.get_value(condition_context)
        if value is None or isinstance(value, self.value_type):
            return self.is_gt(value, condition_context)
        return False

    def is_ge(self, value, condition_context):
        return False

    def ge(self, operand, condition_context):
        value = operand.get_value(condition_context)
        if value is None or isinstance(value, self.value_type):
            return self.is_ge(value, condition_context)
        return False
