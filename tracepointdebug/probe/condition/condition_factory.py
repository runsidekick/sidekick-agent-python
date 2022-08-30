import abc

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, ParseTreeListener

import sys

if sys.version_info[0] < 3:
    from tracepointdebug.tracepoint.condition.antlr4parser.python2_runtime.ConditionLexer import ConditionLexer
    from tracepointdebug.tracepoint.condition.antlr4parser.python2_runtime.ConditionParser import ConditionParser
else:
    from tracepointdebug.probe.condition.antlr4parser.python3_runtime.ConditionLexer import ConditionLexer
    from tracepointdebug.probe.condition.antlr4parser.python3_runtime.ConditionParser import ConditionParser

from tracepointdebug.probe.condition.binary_operator import BinaryOperator
from tracepointdebug.probe.condition.comparison_operator import ComparisonOperator
from tracepointdebug.probe.condition.composite_condition import CompositeCondition
from tracepointdebug.probe.condition.constant_value_provider import ConstantValueProvider
from tracepointdebug.probe.condition.operand.boolean_operand import BooleanOperand
from tracepointdebug.probe.condition.operand.null_operand import NullOperand
from tracepointdebug.probe.condition.operand.number_operand import NumberOperand
from tracepointdebug.probe.condition.operand.string_operand import StringOperand
from tracepointdebug.probe.condition.operand.variable_operand import VariableOperand
from tracepointdebug.probe.condition.single_condition import SingleCondition

ABC = abc.ABCMeta('ABC', (object,), {})


class ConditionBuilder(ABC):

    @abc.abstractmethod
    def build(self):
        pass

    @abc.abstractmethod
    def add_builder(self, builder):
        pass

    @abc.abstractmethod
    def add_operator(self, builder):
        pass


class SingleConditionBuilder(ConditionBuilder):

    def __init__(self):
        self.left_operand = None
        self.right_operand = None
        self.comparison_operator = None

    def build(self):
        return SingleCondition(left_operand=self.left_operand,
                               right_operand=self.right_operand,
                               comparison_operator=self.comparison_operator)

    def add_builder(self, builder):
        raise Exception("Unsupported Operation")

    def add_operator(self, builder):
        raise Exception("Unsupported Operation")


class CompositeConditionBuilder(ConditionBuilder):

    def __init__(self):
        self.builders = []
        self.operators = []

    def build(self):
        if len(self.builders) == 1:
            return self.builders[0].build()

        conditions = []
        for builder in self.builders:
            conditions.append(builder.build())

        return CompositeCondition(conditions, self.operators)

    def add_builder(self, builder):
        self.builders.append(builder)

    def add_operator(self, builder):
        self.operators.append(builder)


class ConditionListener(ParseTreeListener):

    # Enter a parse tree produced by ConditionParser#parse.
    def __init__(self):
        self.condition_builder_stack = [CompositeConditionBuilder()]

    def enterParse(self, ctx):
        pass

    # Exit a parse tree produced by ConditionParser#parse.
    def exitParse(self, ctx):
        pass

    # Enter a parse tree produced by ConditionParser#binaryExpression.
    def enterBinaryExpression(self, ctx):
        pass

    # Exit a parse tree produced by ConditionParser#binaryExpression.
    def exitBinaryExpression(self, ctx):
        pass

    # Enter a parse tree produced by ConditionParser#parenExpression.
    def enterParenExpression(self, ctx):
        self.condition_builder_stack.append(CompositeConditionBuilder())

    # Exit a parse tree produced by ConditionParser#parenExpression.
    def exitParenExpression(self, ctx):
        condition_builder = self.condition_builder_stack.pop()
        if len(self.condition_builder_stack) > 0:
            parent_condition_builder = self.condition_builder_stack[-1]
            parent_condition_builder.add_builder(condition_builder)

    # Enter a parse tree produced by ConditionParser#comparatorExpression.
    def enterComparatorExpression(self, ctx):
        self.condition_builder_stack.append(SingleConditionBuilder())
        condition_builder = self.condition_builder_stack[-1]

        if ctx.op.EQ() is not None:
            condition_builder.comparison_operator = ComparisonOperator.EQ
        elif ctx.op.NE() is not None:
            condition_builder.comparison_operator = ComparisonOperator.NE
        elif ctx.op.LT() is not None:
            condition_builder.comparison_operator = ComparisonOperator.LT
        elif ctx.op.LE() is not None:
            condition_builder.comparison_operator = ComparisonOperator.LE
        elif ctx.op.GT() is not None:
            condition_builder.comparison_operator = ComparisonOperator.GT
        elif ctx.op.GE() is not None:
            condition_builder.comparison_operator = ComparisonOperator.GE
        else:
            raise Exception("Unsupported comparison operator: {}".format(ctx.getText()))

    # Exit a parse tree produced by ConditionParser#comparatorExpression.
    def exitComparatorExpression(self, ctx):
        condition_builder = self.condition_builder_stack.pop()
        if len(self.condition_builder_stack) > 0:
            parent_condition_builder = self.condition_builder_stack[-1]
            parent_condition_builder.add_builder(condition_builder)
        else:
            raise Exception("There is no active condition to add sub-condition: {}".format(ctx.getText()))

    # Enter a parse tree produced by ConditionParser#comparator.
    def enterComparator(self, ctx):
        pass

    # Exit a parse tree produced by ConditionParser#comparator.
    def exitComparator(self, ctx):
        pass

    # Enter a parse tree produced by ConditionParser#binary.
    def enterBinary(self, ctx):
        if len(self.condition_builder_stack) > 0:
            active_condition_builder = self.condition_builder_stack[-1]
            if ctx.AND() is not None:
                active_condition_builder.add_operator(BinaryOperator.AND)
            elif ctx.OR() is not None:
                active_condition_builder.add_operator(BinaryOperator.OR)
            else:
                raise Exception("Unsupported binary operator: {}".format(ctx.getText()))
        else:
            raise Exception("There is no active condition to add binary operator: {}".format(ctx.getText()))

    # Exit a parse tree produced by ConditionParser#binary.
    def exitBinary(self, ctx):
        pass

    # Enter a parse tree produced by ConditionParser#operand.
    def enterOperand(self, ctx):
        condition_builder = self.condition_builder_stack[-1]
        operand = None
        if ctx.BOOLEAN() is not None:
            operand = ConditionFactory.create_boolean_operand(ctx.getText())
        if ctx.CHARACTER() is not None:
            operand = ConditionFactory.create_string_operand(ctx.getText())
        if ctx.STRING() is not None:
            operand = ConditionFactory.create_string_operand(ctx.getText())
        if ctx.NUMBER() is not None:
            operand = ConditionFactory.create_number_operand(ctx.getText())
        if ctx.NULL() is not None:
            operand = ConditionFactory.create_null_operand()
        if ctx.VARIABLE() is not None:
            operand = ConditionFactory.create_variable_operand(ctx.getText())

        if condition_builder.left_operand is None:
            condition_builder.left_operand = operand
        else:
            condition_builder.right_operand = operand

    # Exit a parse tree produced by ConditionParser#operand.
    def exitOperand(self, ctx):
        pass

    def build(self):
        condition_builder = self.condition_builder_stack.pop()
        return condition_builder.build()


class ConditionFactory(object):

    @staticmethod
    def create_boolean_operand(operand_expression):
        return BooleanOperand(ConstantValueProvider(operand_expression.lower() == "true"))

    @staticmethod
    def create_string_operand(operand_expression):
        return StringOperand(ConstantValueProvider(operand_expression[1:-1]))

    @staticmethod
    def create_variable_operand(operand_expression):
        return VariableOperand(operand_expression)

    @staticmethod
    def create_number_operand(number_operand_expression):
        try:
            result = int(number_operand_expression)
        except ValueError:
            try:
                result = float(number_operand_expression)
            except ValueError:
                result = None
        return NumberOperand(ConstantValueProvider(result))

    @staticmethod
    def create_null_operand():
        return NullOperand()

    @staticmethod
    def create_condition_from_expression(expression):
        expression_stream = InputStream(expression)
        lexer = ConditionLexer(expression_stream)
        tokens = CommonTokenStream(lexer)
        parser = ConditionParser(tokens)
        tree = parser.parse()

        listener = ConditionListener()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        return listener.build()
