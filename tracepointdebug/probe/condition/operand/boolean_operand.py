from tracepointdebug.probe.condition.operand.typed_operand import TypedOperand


class BooleanOperand(TypedOperand):

    def __init__(self, value_provider):
        super(BooleanOperand, self).__init__(bool, value_provider)

    def is_eq(self, value, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val == value

    def is_ne(self, value, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val != value


