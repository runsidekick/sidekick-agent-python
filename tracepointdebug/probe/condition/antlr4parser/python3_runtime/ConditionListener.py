# Generated from Condition.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ConditionParser import ConditionParser
else:
    from ConditionParser import ConditionParser

# This class defines a complete listener for a parse tree produced by ConditionParser.
class ConditionListener(ParseTreeListener):

    # Enter a parse tree produced by ConditionParser#parse.
    def enterParse(self, ctx:ConditionParser.ParseContext):
        pass

    # Exit a parse tree produced by ConditionParser#parse.
    def exitParse(self, ctx:ConditionParser.ParseContext):
        pass


    # Enter a parse tree produced by ConditionParser#binaryExpression.
    def enterBinaryExpression(self, ctx:ConditionParser.BinaryExpressionContext):
        pass

    # Exit a parse tree produced by ConditionParser#binaryExpression.
    def exitBinaryExpression(self, ctx:ConditionParser.BinaryExpressionContext):
        pass


    # Enter a parse tree produced by ConditionParser#parenExpression.
    def enterParenExpression(self, ctx:ConditionParser.ParenExpressionContext):
        pass

    # Exit a parse tree produced by ConditionParser#parenExpression.
    def exitParenExpression(self, ctx:ConditionParser.ParenExpressionContext):
        pass


    # Enter a parse tree produced by ConditionParser#comparatorExpression.
    def enterComparatorExpression(self, ctx:ConditionParser.ComparatorExpressionContext):
        pass

    # Exit a parse tree produced by ConditionParser#comparatorExpression.
    def exitComparatorExpression(self, ctx:ConditionParser.ComparatorExpressionContext):
        pass


    # Enter a parse tree produced by ConditionParser#comparator.
    def enterComparator(self, ctx:ConditionParser.ComparatorContext):
        pass

    # Exit a parse tree produced by ConditionParser#comparator.
    def exitComparator(self, ctx:ConditionParser.ComparatorContext):
        pass


    # Enter a parse tree produced by ConditionParser#binary.
    def enterBinary(self, ctx:ConditionParser.BinaryContext):
        pass

    # Exit a parse tree produced by ConditionParser#binary.
    def exitBinary(self, ctx:ConditionParser.BinaryContext):
        pass


    # Enter a parse tree produced by ConditionParser#operand.
    def enterOperand(self, ctx:ConditionParser.OperandContext):
        pass

    # Exit a parse tree produced by ConditionParser#operand.
    def exitOperand(self, ctx:ConditionParser.OperandContext):
        pass



del ConditionParser