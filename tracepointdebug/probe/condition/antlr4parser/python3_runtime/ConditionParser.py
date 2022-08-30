# Generated from Condition.g4 by ANTLR 4.9
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\27")
        buf.write("*\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\3\2\3\2")
        buf.write("\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\5\3\31\n\3\3\3\3")
        buf.write("\3\3\3\3\3\7\3\37\n\3\f\3\16\3\"\13\3\3\4\3\4\3\5\3\5")
        buf.write("\3\6\3\6\3\6\2\3\4\7\2\4\6\b\n\2\5\3\2\n\17\3\2\4\5\5")
        buf.write("\2\3\3\t\t\22\26\2&\2\f\3\2\2\2\4\30\3\2\2\2\6#\3\2\2")
        buf.write("\2\b%\3\2\2\2\n\'\3\2\2\2\f\r\5\4\3\2\r\16\7\2\2\3\16")
        buf.write("\3\3\2\2\2\17\20\b\3\1\2\20\21\7\20\2\2\21\22\5\4\3\2")
        buf.write("\22\23\7\21\2\2\23\31\3\2\2\2\24\25\5\n\6\2\25\26\5\6")
        buf.write("\4\2\26\27\5\n\6\2\27\31\3\2\2\2\30\17\3\2\2\2\30\24\3")
        buf.write("\2\2\2\31 \3\2\2\2\32\33\f\4\2\2\33\34\5\b\5\2\34\35\5")
        buf.write("\4\3\5\35\37\3\2\2\2\36\32\3\2\2\2\37\"\3\2\2\2 \36\3")
        buf.write("\2\2\2 !\3\2\2\2!\5\3\2\2\2\" \3\2\2\2#$\t\2\2\2$\7\3")
        buf.write("\2\2\2%&\t\3\2\2&\t\3\2\2\2\'(\t\4\2\2(\13\3\2\2\2\4\30")
        buf.write(" ")
        return buf.getvalue()


class ConditionParser ( Parser ):

    grammarFileName = "Condition.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'NOT'", "'true'", "'false'", "'null'", "'>'", "'>='", 
                     "'<'", "'<='", "'=='", "'!='", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "BOOLEAN", "AND", "OR", "NOT", "TRUE", 
                      "FALSE", "NULL", "GT", "GE", "LT", "LE", "EQ", "NE", 
                      "LPAREN", "RPAREN", "CHARACTER", "NUMBER", "STRING", 
                      "VARIABLE", "PLACEHOLDER", "WS" ]

    RULE_parse = 0
    RULE_expression = 1
    RULE_comparator = 2
    RULE_binary = 3
    RULE_operand = 4

    ruleNames =  [ "parse", "expression", "comparator", "binary", "operand" ]

    EOF = Token.EOF
    BOOLEAN=1
    AND=2
    OR=3
    NOT=4
    TRUE=5
    FALSE=6
    NULL=7
    GT=8
    GE=9
    LT=10
    LE=11
    EQ=12
    NE=13
    LPAREN=14
    RPAREN=15
    CHARACTER=16
    NUMBER=17
    STRING=18
    VARIABLE=19
    PLACEHOLDER=20
    WS=21

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ParseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(ConditionParser.ExpressionContext,0)


        def EOF(self):
            return self.getToken(ConditionParser.EOF, 0)

        def getRuleIndex(self):
            return ConditionParser.RULE_parse

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParse" ):
                listener.enterParse(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParse" ):
                listener.exitParse(self)




    def parse(self):

        localctx = ConditionParser.ParseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_parse)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            self.expression(0)
            self.state = 11
            self.match(ConditionParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ConditionParser.RULE_expression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class BinaryExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ConditionParser.ExpressionContext
            super().__init__(parser)
            self.left = None # ExpressionContext
            self.op = None # BinaryContext
            self.right = None # ExpressionContext
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ConditionParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(ConditionParser.ExpressionContext,i)

        def binary(self):
            return self.getTypedRuleContext(ConditionParser.BinaryContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBinaryExpression" ):
                listener.enterBinaryExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBinaryExpression" ):
                listener.exitBinaryExpression(self)


    class ParenExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ConditionParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(ConditionParser.LPAREN, 0)
        def expression(self):
            return self.getTypedRuleContext(ConditionParser.ExpressionContext,0)

        def RPAREN(self):
            return self.getToken(ConditionParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenExpression" ):
                listener.enterParenExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenExpression" ):
                listener.exitParenExpression(self)


    class ComparatorExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ConditionParser.ExpressionContext
            super().__init__(parser)
            self.left = None # OperandContext
            self.op = None # ComparatorContext
            self.right = None # OperandContext
            self.copyFrom(ctx)

        def operand(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ConditionParser.OperandContext)
            else:
                return self.getTypedRuleContext(ConditionParser.OperandContext,i)

        def comparator(self):
            return self.getTypedRuleContext(ConditionParser.ComparatorContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparatorExpression" ):
                listener.enterComparatorExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparatorExpression" ):
                listener.exitComparatorExpression(self)



    def expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ConditionParser.ExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_expression, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 22
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ConditionParser.LPAREN]:
                localctx = ConditionParser.ParenExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 14
                self.match(ConditionParser.LPAREN)
                self.state = 15
                self.expression(0)
                self.state = 16
                self.match(ConditionParser.RPAREN)
                pass
            elif token in [ConditionParser.BOOLEAN, ConditionParser.NULL, ConditionParser.CHARACTER, ConditionParser.NUMBER, ConditionParser.STRING, ConditionParser.VARIABLE, ConditionParser.PLACEHOLDER]:
                localctx = ConditionParser.ComparatorExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 18
                localctx.left = self.operand()
                self.state = 19
                localctx.op = self.comparator()
                self.state = 20
                localctx.right = self.operand()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 30
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = ConditionParser.BinaryExpressionContext(self, ConditionParser.ExpressionContext(self, _parentctx, _parentState))
                    localctx.left = _prevctx
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                    self.state = 24
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 25
                    localctx.op = self.binary()
                    self.state = 26
                    localctx.right = self.expression(3) 
                self.state = 32
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ComparatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GT(self):
            return self.getToken(ConditionParser.GT, 0)

        def GE(self):
            return self.getToken(ConditionParser.GE, 0)

        def LT(self):
            return self.getToken(ConditionParser.LT, 0)

        def LE(self):
            return self.getToken(ConditionParser.LE, 0)

        def EQ(self):
            return self.getToken(ConditionParser.EQ, 0)

        def NE(self):
            return self.getToken(ConditionParser.NE, 0)

        def getRuleIndex(self):
            return ConditionParser.RULE_comparator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparator" ):
                listener.enterComparator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparator" ):
                listener.exitComparator(self)




    def comparator(self):

        localctx = ConditionParser.ComparatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_comparator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 33
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << ConditionParser.GT) | (1 << ConditionParser.GE) | (1 << ConditionParser.LT) | (1 << ConditionParser.LE) | (1 << ConditionParser.EQ) | (1 << ConditionParser.NE))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BinaryContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AND(self):
            return self.getToken(ConditionParser.AND, 0)

        def OR(self):
            return self.getToken(ConditionParser.OR, 0)

        def getRuleIndex(self):
            return ConditionParser.RULE_binary

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBinary" ):
                listener.enterBinary(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBinary" ):
                listener.exitBinary(self)




    def binary(self):

        localctx = ConditionParser.BinaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_binary)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            _la = self._input.LA(1)
            if not(_la==ConditionParser.AND or _la==ConditionParser.OR):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OperandContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOLEAN(self):
            return self.getToken(ConditionParser.BOOLEAN, 0)

        def CHARACTER(self):
            return self.getToken(ConditionParser.CHARACTER, 0)

        def NUMBER(self):
            return self.getToken(ConditionParser.NUMBER, 0)

        def STRING(self):
            return self.getToken(ConditionParser.STRING, 0)

        def NULL(self):
            return self.getToken(ConditionParser.NULL, 0)

        def VARIABLE(self):
            return self.getToken(ConditionParser.VARIABLE, 0)

        def PLACEHOLDER(self):
            return self.getToken(ConditionParser.PLACEHOLDER, 0)

        def getRuleIndex(self):
            return ConditionParser.RULE_operand

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOperand" ):
                listener.enterOperand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOperand" ):
                listener.exitOperand(self)




    def operand(self):

        localctx = ConditionParser.OperandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_operand)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << ConditionParser.BOOLEAN) | (1 << ConditionParser.NULL) | (1 << ConditionParser.CHARACTER) | (1 << ConditionParser.NUMBER) | (1 << ConditionParser.STRING) | (1 << ConditionParser.VARIABLE) | (1 << ConditionParser.PLACEHOLDER))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expression_sempred(self, localctx:ExpressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         




