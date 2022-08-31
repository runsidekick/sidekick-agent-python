from enum import Enum


class ComparisonOperator(Enum):
    EQ = "=="
    NE = "!="

    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="

    @staticmethod
    def from_expression(expression):
        for op in ComparisonOperator:
            if op == expression:
                return op
