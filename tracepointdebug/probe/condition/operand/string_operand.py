from tracepointdebug.probe.condition.operand.typed_operand import TypedOperand
import sys

class StringOperand(TypedOperand):

    def __init__(self, value_provider):
        if sys.version_info[0] >= 3:
            super(StringOperand, self).__init__(str, value_provider)
        else:
            super(StringOperand, self).__init__((str, unicode), value_provider)

    def is_eq(self, value, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val == value

    def is_ne(self, value, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val != value
