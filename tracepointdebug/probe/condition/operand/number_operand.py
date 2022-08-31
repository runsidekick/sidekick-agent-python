from tracepointdebug.probe.condition.operand.typed_operand import TypedOperand


class NumberOperand(TypedOperand):

    def __init__(self, value_provider):
        super(NumberOperand, self).__init__((float, int), value_provider)

    def is_eq(self, value, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val == value

    def is_ne(self, value, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val != value

    def is_lt(self, value, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val < value

    def is_le(self, value, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val <= value

    def is_gt(self, value, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val > value

    def is_ge(self, value, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val >= value
