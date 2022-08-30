from tracepointdebug.probe.condition.binary_operator import BinaryOperator
from tracepointdebug.probe.condition.condition import Condition


class CompositeCondition(Condition):

    def __init__(self, conditions, operators):
        self.conditions = conditions
        self.operators = operators

    def evaluate(self, condition_context):
        result = None
        for i in range(len(self.conditions)):
            condition = self.conditions[i]
            evaluation_result = condition.evaluate(condition_context)
            if result is None:
                result = evaluation_result
            else:
                operator = self.operators[i-1]
                if operator == BinaryOperator.AND:
                    result = result and evaluation_result
                elif operator == BinaryOperator.OR:
                    result = result or evaluation_result

        if result is not None:
            return result
        return False
