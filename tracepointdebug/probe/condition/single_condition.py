from tracepointdebug.probe.condition.comparison_operator import ComparisonOperator
from tracepointdebug.probe.condition.condition import Condition


class SingleCondition(Condition):

    def __init__(self, left_operand, right_operand, comparison_operator):
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.comparison_operator = comparison_operator

    def evaluate(self, condition_context):
        if self.comparison_operator == ComparisonOperator.EQ:
            return self.left_operand.eq(self.right_operand, condition_context=condition_context)
        if self.comparison_operator == ComparisonOperator.NE:
            return self.left_operand.ne(self.right_operand, condition_context=condition_context)
        if self.comparison_operator == ComparisonOperator.GE:
            return self.left_operand.ge(None, self.right_operand)
        if self.comparison_operator == ComparisonOperator.LE:
            return self.left_operand.le(self.right_operand, condition_context=condition_context)
        if self.comparison_operator == ComparisonOperator.GT:
            return self.left_operand.gt(self.right_operand, condition_context=condition_context)
        if self.comparison_operator == ComparisonOperator.LT:
            return self.left_operand.lt(self.right_operand, condition_context=condition_context)
        return False
