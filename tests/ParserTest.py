'''
Created on 11/lug/2012

@author: Francesco Capozzo
'''
import unittest
from myclips.parser.Parser import Parser
import myclips.parser.types as types
from pyparsing import ParseException, ParseFatalException
from unittest.case import expectedFailure

class ParserTest(unittest.TestCase):

    def setUp(self):
        if not hasattr(self, "parser"):
            self.parser = Parser()

    def _testImpl(self, parsername, parsable, parseAll=False):
        p = self.parser.getSParser(parsername)
        #p.enablePackrat()
        return p.parseString(parsable, parseAll)

    def test_deffact_Normal(self):
        '''Check parse result for normal deffacts construct'''
        
        res = self._testImpl('DefFactsConstructParser', r"""
        (deffacts nome1 "commento1"
            (1 2 3)
            (a b c)
        )
        """).asList()
        
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], types.DefFactsConstruct)
        self.assertEqual(res[0].deffactsName, "nome1")
        self.assertEqual(res[0].deffactsComment, "commento1")
        self.assertIsInstance(res[0].rhs, list)

    def test_deffact_WithoutComment(self):
        '''Check parse result for deffacts construct without comment field'''
        res = self._testImpl('DefFactsConstructParser', r"""
        (deffacts nome1
            (1 2 3)
            (a b c)
        )
        """).asList()
        
        self.assertEqual(res[0].deffactsComment, None)


    def test_deffact_SpaceBetweenLparAndDeffacts(self):
        '''Check if deffacts is parsed correctly even if there is a whitespace between LPAR and keyword'''
        res = self._testImpl('DefFactsConstructParser', r"""
        ( deffacts nome1 "commento1"
            (1 2 3)
            (a b c)
        )
        """).asList()
        
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], types.DefFactsConstruct)
    
    def test_deffact_NLBetweenLparAndDeffacts(self):
        '''Check if deffacts is parsed correctly even if there is a new-line between LPAR and keyword'''
        res = self._testImpl('DefFactsConstructParser', r"""
        (
            deffacts nome1 "commento1"
            (1 2 3)
            (a b c)
        )
        """).asList()
        
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], types.DefFactsConstruct)

    def test_deffact_TwoRhsPattern(self):
        '''Check if deffacts content is correctly parsed if it's multiple ordered-fact'''
        res = self._testImpl('DefFactsConstructParser', r"""
        (deffacts nome1 "commento1"
            (1 2 3)
            (a b c)
        )
        """).asList()
        
        self.assertEqual(len(res[0].rhs), 2)
        self.assertIsInstance(res[0].rhs[0], types.OrderedRhsPattern)
        self.assertIsInstance(res[0].rhs[1], types.OrderedRhsPattern)


    def test_DefFactsConstructParser_TemplateRhsPattern(self):
        '''Check if deffacts content is correctly parsed if it's a template fact'''
        res = self._testImpl('DefFactsConstructParser', r"""
        (deffacts nome1 "commento1"
            (templateName (slot1k slot1v))
        )
        """).asList()
        
        self.assertEqual(len(res[0].rhs), 1)
        self.assertIsInstance(res[0].rhs[0], types.TemplateRhsPattern)

    def test_DefFactsConstructParser_TemplateRhsPatternAndOrderedRhsPattern(self):
        '''Check if deffacts content is correctly parsed if it's mixed type'''
        res = self._testImpl('DefFactsConstructParser', r"""
        (deffacts nome1 "commento1"
            (templateName (slot1k slot1v))
            (a b c)
        )
        """).asList()
        
        self.assertEqual(len(res[0].rhs), 2)
        self.assertIsInstance(res[0].rhs[0], types.TemplateRhsPattern)
        self.assertIsInstance(res[0].rhs[1], types.OrderedRhsPattern)


    def test_orderedrhspattern_Normal(self):
        '''Check if RHS parsing is correct'''
        res = self._testImpl('RhsPatternParser', r"""
        (A b c)
        """).asList()
        
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], types.OrderedRhsPattern)
        self.assertIsInstance(res[0].content[0], types.Symbol)
        self.assertIsInstance(res[0].content[1], types.Symbol)
        self.assertIsInstance(res[0].content[2], types.Symbol)

    def test_orderedrhspattern_WithSingleFieldVariable(self):
        '''Check if RHS parsing is correct with singlefield variable in it'''
        res = self._testImpl('RhsPatternParser', r"""
        (A ?b c)
        """).asList()
        
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], types.OrderedRhsPattern)
        self.assertIsInstance(res[0].content[0], types.Symbol)
        self.assertIsInstance(res[0].content[1], types.SingleFieldVariable)
        self.assertIsInstance(res[0].content[2], types.Symbol)

    def test_orderedrhspattern_WithInteger(self):
        '''Check if RHS parsing is correct with integer in it'''
        res = self._testImpl('RhsPatternParser', r"""
        (A 1 c)
        """).asList()
        
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], types.OrderedRhsPattern)
        self.assertIsInstance(res[0].content[0], types.Symbol)
        self.assertIsInstance(res[0].content[1], types.Integer)
        self.assertIsInstance(res[0].content[2], types.Symbol)
        
    def test_MultiFieldRhsSlot_SingleValue(self):
        '''Check multifield RHS slot parsing is correct with a single value in it'''
        res = self._testImpl('MultiFieldRhsSlotParser', r"""
        (slotName prova)
        """).asList()

        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], types.MultiFieldRhsSlot)
        self.assertEqual(res[0].slotName, "slotName")
        self.assertIsInstance(res[0].slotValue, list)
        self.assertEqual(len(res[0].slotValue), 1)
        
    def test_MultiFieldRhsSlot_TwoValue(self):
        '''Check multifield RHS slot parsing is correct with a multiple values'''
        res = self._testImpl('MultiFieldRhsSlotParser', r"""
        (slotName prova ciao)
        """).asList()

        self.assertIsInstance(res[0], types.MultiFieldRhsSlot)
        self.assertEqual(len(res[0].slotValue), 2)
        
    def test_MultiFieldRhsSlot_ZeroValue(self):
        '''Check multifield RHS slot parsing is correct without values'''
        res = self._testImpl('MultiFieldRhsSlotParser', r"""
        (slotName )
        """).asList()

        self.assertIsInstance(res[0], types.MultiFieldRhsSlot)
        self.assertEqual(res[0].slotValue, [])
        
    def test_SingleFieldRhsSlot_Normal(self):
        '''Check single-field RHS slot parsing is correct with a single value in it'''
        res = self._testImpl('SingleFieldRhsSlotParser', r"""
        (slotName slotValue)
        """).asList()

        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], types.SingleFieldRhsSlot)
        self.assertEqual(res[0].slotName, "slotName")
        self.assertIsInstance(res[0].slotValue, types.ParsedType )
        
    def test_SingleFieldRhsSlot_NotValid(self):
        '''Check exception raising when parsing single-field without slot value'''
        self.assertRaises(ParseException, self._testImpl, 'SingleFieldRhsSlotParser', r"""
        (slotName )
        """)
        
    def test_RhsSlotParser_Normal(self):
        '''Check general RHS-slot-parser return correct value type'''
        res = self._testImpl('RhsSlotParser', r"""
        (slotName slotValue)
        """).asList()
        
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], (types.SingleFieldRhsSlot, types.MultiFieldRhsSlot))
        self.assertEqual(res[0].slotName, "slotName")
        
    def test_RhsSlotParser_ForcedMultiField(self):
        '''Check general RHS-slot-parser return correct value type when multi-field is required'''
        res = self._testImpl('RhsSlotParser', r"""
        (slotName slotValue1 slotValue2)
        """).asList()
        
        self.assertIsInstance(res[0], types.MultiFieldRhsSlot)
    
    def test_RhsSlotParser_GuessSingleField(self):
        '''Check general RHS-slot-parser return correct value type when single-field is possible'''
        res = self._testImpl('RhsSlotParser', r"""
        (slotName singleField)
        """).asList()
        
        self.assertIsInstance(res[0], types.SingleFieldRhsSlot)

    def test_RhsSlotParser_GuessMultiField(self):
        '''Check general RHS-slot-parser return correct value type when multi-field is possible'''
        res = self._testImpl('RhsSlotParser', r"""
        (slotName )
        """).asList()
        
        self.assertIsInstance(res[0], types.MultiFieldRhsSlot)

    def test_TemplateRhsPatternParser(self):
        '''Check general full template-rhs format '''
        res = self._testImpl('TemplateRhsPatternParser', r"""
        (templateName 
            (slot1k slot1v) 
            (slot2k) 
            (slot3k slot3v1 slot3v2)
        )
        """).asList()
        
        self.assertIsInstance(res[0], types.TemplateRhsPattern)
        self.assertEqual(res[0].templateName, "templateName")
        self.assertEqual(len(res[0].templateSlots), 3)
        self.assertFalse(False in [isinstance(x, types.FieldRhsSlot) for x in res[0].templateSlots])

    def test_TemplateRhsPatternParser_SlotsTypes(self):
        '''Check general full template-rhs slot format'''
        res = self._testImpl('TemplateRhsPatternParser', r"""
        (templateName 
            (slot1k slot1v) 
            (slot2k) 
            (slot3k slot3v1 slot3v2)
        )
        """).asList()
        
        self.assertIsInstance(res[0].templateSlots[0], types.SingleFieldRhsSlot)
        self.assertIsInstance(res[0].templateSlots[1], types.MultiFieldRhsSlot)
        self.assertIsInstance(res[0].templateSlots[2], types.MultiFieldRhsSlot)

    def test_TemplateRhsPatternParser_FunctionInSlot(self):
        '''Check general template-rhs format when function call in it'''
        res = self._testImpl('TemplateRhsPatternParser', r"""
        (templateName 
            (slot1k (funzione 1 2 3)) 
        )
        """).asList()
        
        self.assertIsInstance(res[0].templateSlots[0], types.SingleFieldRhsSlot)
        self.assertIsInstance(res[0].templateSlots[0].slotValue, types.FunctionCall)


    def test_DefRuleConstructParser_Minimal(self):
        '''Check minimal defrule construct parsing'''
        res = self._testImpl('DefRuleConstructParser', r"""
        (defrule rulename
            => 
        )
        """).asList()
        
        self.assertIsInstance(res[0], types.DefRuleConstruct)
        self.assertEqual(res[0].defruleName, "rulename")

    def test_DefRuleConstructParser_WithComment(self):
        '''Check defrule construct parsing with comment'''
        res = self._testImpl('DefRuleConstructParser', r"""
        (defrule rulename "comment"
            => 
        )
        """).asList()
        
        self.assertEqual(res[0].defruleComment, "comment")

    def test_DefRuleConstructParser_WithRHS(self):
        '''Check defrule construct parsing with RHS'''
        res = self._testImpl('DefRuleConstructParser', r"""
        (defrule rulename
            => 
            (assert (A b C))
        )
        """).asList()
        
        self.assertEqual(len(res[0].rhs), 1)
        self.assertIsInstance(res[0].rhs[0], types.FunctionCall)

    def test_DefRuleConstructParser_WithRHSs(self):
        '''Check defrule construct parsing with multiple RHS entry'''
        res = self._testImpl('DefRuleConstructParser', r"""
        (defrule rulename
            => 
            (assert (A b C))
            (retract (A ?a c) ?c)
        )
        """).asList()
        
        self.assertEqual(len(res[0].rhs), 2)
        self.assertIsInstance(res[0].rhs[0], types.FunctionCall)
        self.assertIsInstance(res[0].rhs[1], types.FunctionCall)
        #print res[0].rhs[1]

    def test_DefRuleConstructParser_WithDeclarations(self):
        '''Check defrule construct parsing with property declaration'''
        res = self._testImpl('DefRuleConstructParser', r"""
        (defrule rulename
            (declare 
                (salience 9001)
                (auto-focus TRUE)
            )
            => 
        )
        """).asList()
        
        self.assertEqual(len(res[0].defruleDeclaration), 2)
        self.assertIsInstance(res[0].defruleDeclaration[0], types.RuleProperty)
        self.assertIsInstance(res[0].defruleDeclaration[1], types.RuleProperty)

    def test_DefRuleConstructParser_WithLHS(self):
        '''Check defrule construct parsing with LHS'''
        res = self._testImpl('DefRuleConstructParser', r"""
        (defrule rulename
            (A B C) 
            => 
        )
        """).asList()
        
        self.assertNotEqual(len(res[0].lhs), 0)

    @expectedFailure
    def test_ActionParser_MultifieldValueNested(self):
        '''Check action parsed correct parsing when nested value in it'''
        res = self._testImpl('ActionParser', r"""
        (assert (A B C))
        """).asList()
        
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], types.FunctionCall)
        self.assertNotIsInstance(res[0].funcArgs[0], types.FunctionCall)
    

    def test_RulePropertyParser_Salience(self):
        '''Check salience correct parsing'''
        res = self._testImpl('RulePropertyParser', r"""
        (salience 100)
        """).asList()
        
        self.assertIsInstance(res[0], types.RuleProperty)
        self.assertEqual(res[0].propertyValue, 100)

    def test_RulePropertyParser_NegativeSalience(self):
        '''Check salience correct parsing when negative'''
        res = self._testImpl('RulePropertyParser', r"""
        (salience -100)
        """).asList()
        
        self.assertIsInstance(res[0], types.RuleProperty)
        self.assertEqual(res[0].propertyValue, -100)

    def test_RulePropertyParser_InvalidFloatSalience(self):
        '''Check exception raising for salience when invalid value'''
        self.assertRaises(ParseException, self._testImpl, 'RulePropertyParser', r"""
        (salience -100.34)
        """)
        
    def test_RulePropertyParser_InvalidSymbolSalience(self):
        '''Check exception raising for salience when invalid value'''
        self.assertRaises(ParseException, self._testImpl, 'RulePropertyParser', r"""
        (salience ciao)
        """)

    def test_RulePropertyParser_TrueAutoFocus(self):
        '''Check auto-focus parsin return value'''
        res = self._testImpl('RulePropertyParser', r"""
        (auto-focus TRUE)
        """).asList()
        
        self.assertIsInstance(res[0], types.RuleProperty)

    def test_RulePropertyParser_FalseAutoFocus(self):
        '''Check auto-focus parsin return value'''
        res = self._testImpl('RulePropertyParser', r"""
        (auto-focus FALSE)
        """).asList()
        
        self.assertIsInstance(res[0], types.RuleProperty)

    @expectedFailure
    def test_RulePropertyParser_InvalidAutoFocus(self):
        '''Check exception raising when invalid auto-focus value parsed'''
        self.assertRaises(ParseException, self._testImpl, 'RulePropertyParser', r"""
        (auto-focus ciao)
        """)

    def test_PatternCEParser_OrderedPatternCE(self):
        res = self._testImpl('PatternCEParser', r"""
        (A B C)
        """).asList()
        
        self.assertIsInstance(res[0], types.OrderedPatternCE)

    def test_PatternCEParser_TemplatePatternCE(self):
        res = self._testImpl('PatternCEParser', r"""
        (template 
            (s1 v1)
            (s2 v1 v2 v3)
        )
        """).asList()
        
        self.assertIsInstance(res[0], types.TemplatePatternCE)
        self.assertEqual(len(res[0].templateSlots), 2)

    def test_OrderedPatternCEParser(self):
        res = self._testImpl('OrderedPatternCEParser', r"""
        (A B C)
        """).asList()
        
        self.assertIsInstance(res[0], types.OrderedPatternCE)
        self.assertEqual(len(res[0].constraints), 3)

    def test_OrderedPatternCEParser_Constraints(self):
        res = self._testImpl('OrderedPatternCEParser', r"""
        (A G&3|:(eq 1 ?b)|3 $?)
        """).asList()
        
        self.assertIsInstance(res[0], types.OrderedPatternCE)
        self.assertEqual(len(res[0].constraints), 3)
        self.assertIsInstance(res[0].constraints[0], types.Symbol)
        self.assertIsInstance(res[0].constraints[1], types.ConnectedConstraint)
        self.assertIsInstance(res[0].constraints[2], types.UnnamedMultiFieldVariable)

    def test_TemplatePatternCEParser(self):
        res = self._testImpl('TemplatePatternCEParser', r"""
        (templateName (slot))
        """).asList()
        
        self.assertIsInstance(res[0], types.TemplatePatternCE)
        self.assertEqual(res[0].templateName, "templateName")
        self.assertEqual(len(res[0].templateSlots), 1)
        self.assertIsInstance(res[0].templateSlots[0], types.MultiFieldLhsSlot)
        self.assertEqual(res[0].templateSlots[0].slotName, "slot")

    def test_TemplatePatternCEParser_SlotsType(self):
        res = self._testImpl('TemplatePatternCEParser', r"""
        (templateName 
            (s1 v1) 
            (s2 ) 
            (s3 A ?b $?c)
        )
        """).asList()
        
        self.assertIsInstance(res[0], types.TemplatePatternCE)
        self.assertEqual(res[0].templateName, "templateName")
        self.assertEqual(len(res[0].templateSlots), 3)
        self.assertIsInstance(res[0].templateSlots[0], types.SingleFieldLhsSlot)
        self.assertIsInstance(res[0].templateSlots[1], types.MultiFieldLhsSlot)
        self.assertIsInstance(res[0].templateSlots[2], types.MultiFieldLhsSlot)
        self.assertEqual(res[0].templateSlots[0].slotName, "s1")
        self.assertIsInstance(res[0].templateSlots[0].slotValue, types.Constraint)
        self.assertEqual(res[0].templateSlots[1].slotName, "s2")
        self.assertEqual(len(res[0].templateSlots[1].slotValue), 0)
        self.assertEqual(res[0].templateSlots[2].slotName, "s3")
        self.assertEqual(len(res[0].templateSlots[2].slotValue), 3)
        self.assertIsInstance(res[0].templateSlots[2].slotValue[0], types.Constraint)
        self.assertIsInstance(res[0].templateSlots[2].slotValue[1], types.Constraint)
        self.assertIsInstance(res[0].templateSlots[2].slotValue[2], types.Constraint)
        

    def test_ConstraintParser(self):
        res = self._testImpl('ConstraintParser', r"""
        A
        """).asList()
        
        self.assertIsInstance(res[0], types.Constraint)
        self.assertIsInstance(res[0].constraint, (types.PositiveTerm, types.NegativeTerm))
    
    
    def test_ConstraintParser_PositiveTerm(self):
        res = self._testImpl('ConstraintParser', r"""
        A
        """).asList()
        
        self.assertIsInstance(res[0], types.Constraint)
        self.assertIsInstance(res[0].constraint, types.PositiveTerm)
        self.assertIsInstance(res[0].constraint.term, types.Symbol)
    
    
    def test_ConstraintParser_NegativeTerm(self):
        res = self._testImpl('ConstraintParser', r"""
        ~A
        """).asList()
        
        self.assertIsInstance(res[0], types.Constraint)
        self.assertIsInstance(res[0].constraint, types.NegativeTerm)
        self.assertIsInstance(res[0].constraint.term, types.Symbol)
        
        
    def test_ConnectedConstraintParser(self):
        res = self._testImpl('ConstraintParser', r"""
        A&B
        """).asList()
        
        self.assertIsInstance(res[0], types.ConnectedConstraint)
        self.assertIsInstance(res[0].constraint, (types.PositiveTerm, types.NegativeTerm))
        self.assertEqual(len(res[0].connectedConstraints), 1)
        self.assertEqual(res[0].connectedConstraints[0][0], "&")
        self.assertIsInstance(res[0].connectedConstraints[0][1], types.Constraint)
    
    
    def test_ConnectedConstraintParser_FunctionCall(self):
        res = self._testImpl('ConstraintParser', r"""
        A&:(func 1 2)
        """).asList()
        
        self.assertIsInstance(res[0], types.ConnectedConstraint)
        self.assertIsInstance(res[0].constraint, (types.PositiveTerm, types.NegativeTerm))
        self.assertEqual(len(res[0].connectedConstraints), 1)
        self.assertEqual(res[0].connectedConstraints[0][0], "&")
        self.assertIsInstance(res[0].connectedConstraints[0][1], types.Constraint)
        self.assertIsInstance(res[0].connectedConstraints[0][1].constraint, types.PositiveTerm)
        self.assertIsInstance(res[0].connectedConstraints[0][1].constraint.term, types.FunctionCall)
    
    
    def test_ConnectedConstraintParser_NegativeTermFunctionCall(self):
        res = self._testImpl('ConstraintParser', r"""
        A&~:(func 1 2)
        """).asList()
        
        self.assertIsInstance(res[0], types.ConnectedConstraint)
        self.assertIsInstance(res[0].constraint, (types.PositiveTerm, types.NegativeTerm))
        self.assertEqual(len(res[0].connectedConstraints), 1)
        self.assertEqual(res[0].connectedConstraints[0][0], "&")
        self.assertIsInstance(res[0].connectedConstraints[0][1], types.Constraint)
        self.assertIsInstance(res[0].connectedConstraints[0][1].constraint, types.NegativeTerm)
        self.assertIsInstance(res[0].connectedConstraints[0][1].constraint.term, types.FunctionCall)
        
    def test_ConditionalElementParser_AssignedPatternCE(self):
        res = self._testImpl('ConditionalElementParser', r"""
        ?var <- ( B A&~:(func 1 2) )
        """).asList()

        self.assertIsInstance(res[0], types.AssignedPatternCE)
        self.assertIsInstance(res[0].variable, types.SingleFieldVariable)
        self.assertIsInstance(res[0].pattern, types.PatternCE)
        self.assertNotIsInstance(res[0].pattern, types.AssignedPatternCE)

    def test_ConditionalElementParser_AssignedPatternCE_WithoutWS(self):
        res = self._testImpl('ConditionalElementParser', r"""
        ?var<-( B A&~:(func 1 2) )
        """).asList()

        self.assertIsInstance(res[0], types.AssignedPatternCE)
        self.assertIsInstance(res[0].variable, types.SingleFieldVariable)
        self.assertIsInstance(res[0].pattern, types.PatternCE)
        self.assertNotIsInstance(res[0].pattern, types.AssignedPatternCE)


    def test_ConditionalElementParser_OrderedPatternCEParser(self):
        res = self._testImpl('ConditionalElementParser', r"""
        (A B C D)
        """).asList()

        self.assertIsInstance(res[0], types.OrderedPatternCE)

    def test_ConditionalElementParser_TemplatePatternCEParser(self):
        res = self._testImpl('ConditionalElementParser', r"""
        (template 
            (B) 
            (C c) 
            (D d1 d2 d3)
        )
        """).asList()

        self.assertIsInstance(res[0], types.TemplatePatternCE)
    
    def test_ConditionalElementParser_NotPatternCE(self):
        res = self._testImpl('ConditionalElementParser', r"""
        (not (A B C))
        """).asList()

        self.assertIsInstance(res[0], types.NotPatternCE)
        self.assertIsInstance(res[0].pattern, types.PatternCE)
        self.assertNotIsInstance(res[0].pattern, types.AssignedPatternCE)

    def test_ConditionalElementParser_NotPatternCE_WithWSBefore(self):
        res = self._testImpl('ConditionalElementParser', r"""
        ( not (A B C))
        """).asList()

        self.assertIsInstance(res[0], types.NotPatternCE)
        self.assertIsInstance(res[0].pattern, types.PatternCE)
        self.assertNotIsInstance(res[0].pattern, types.AssignedPatternCE)

    def test_ConditionalElementParser_NotPatternCE_WithoutWSAfter(self):
        res = self._testImpl('ConditionalElementParser', r"""
        (not(A B C))
        """).asList()

        self.assertIsInstance(res[0], types.NotPatternCE)
        self.assertIsInstance(res[0].pattern, types.PatternCE)
        self.assertNotIsInstance(res[0].pattern, types.AssignedPatternCE)

    def test_ConditionalElementParser_NotPatternCE_InnerAssignedPatternCENotAllowed(self):
        self.assertRaises(ParseFatalException, self._testImpl, 'ConditionalElementParser', r"""
        (not ?a <- (A B C))
        """)
        
    def test_ConditionalElementParser_TestPatternCE(self):
        res = self._testImpl('ConditionalElementParser', r"""
        (test (func B C))
        """).asList()

        self.assertIsInstance(res[0], types.TestPatternCE)
        self.assertIsInstance(res[0].function, types.FunctionCall)

    def test_ConditionalElementParser_TestPatternCE_WithWSBefore(self):
        res = self._testImpl('ConditionalElementParser', r"""
        ( test (func B C))
        """).asList()

        self.assertIsInstance(res[0], types.TestPatternCE)
        self.assertIsInstance(res[0].function, types.FunctionCall)

    def test_ConditionalElementParser_TestPatternCE_WithoutWSAfter(self):
        res = self._testImpl('ConditionalElementParser', r"""
        (test(func B C))
        """).asList()

        self.assertIsInstance(res[0], types.TestPatternCE)
        self.assertIsInstance(res[0].function, types.FunctionCall)

    def test_ConditionalElementParser_AndPatternCE(self):
        res = self._testImpl('ConditionalElementParser', r"""
        (and 
            (A B C)
            (B C D)
        )
        """).asList()

        self.assertIsInstance(res[0], types.AndPatternCE)
        self.assertEqual(len(res[0].patterns), 2)

    def test_ConditionalElementParser_AndPatternCE_WithWSBefore(self):
        res = self._testImpl('ConditionalElementParser', r"""
        ( and 
            (A B C)
            (B C D)
        )
        """).asList()

        self.assertIsInstance(res[0], types.AndPatternCE)
        self.assertEqual(len(res[0].patterns), 2)

    def test_ConditionalElementParser_AndPatternCE_WithoutWSAfter(self):
        res = self._testImpl('ConditionalElementParser', r"""
        (and(A B C)
            (B C D)
        )
        """).asList()

        self.assertIsInstance(res[0], types.AndPatternCE)
        self.assertEqual(len(res[0].patterns), 2)

    def test_ConditionalElementParser_AndPatternCE_InnerAssignedPatternCEAsFirstNotAllowed(self):
        self.assertRaises(ParseFatalException, self._testImpl, 'ConditionalElementParser', r"""
        (and 
            ?a <- (A B C) 
            (B C D)
        )
        """)

    def test_ConditionalElementParser_AndPatternCE_InnerAssignedPatternCENotAsFirstAllowed(self):
        res = self._testImpl('ConditionalElementParser', r"""
        (and 
            (B C D)
            ?a <- (A B C)
        )
        """).asList()

        self.assertIsInstance(res[0], types.AndPatternCE)
        self.assertEqual(len(res[0].patterns), 2)
        self.assertIsInstance(res[0].patterns[1], types.AssignedPatternCE)
        
    def test_DefTemplateParser(self):
        res = self._testImpl('ConstructParser', r"""
        (deftemplate NomeTemplate "commento" 
            (slot A)
            (multislot B)
        )
        """).asList()

        self.assertIsInstance(res[0], types.DefTemplateConstruct)
        self.assertEqual(res[0].templateName, "NomeTemplate")
        self.assertEqual(res[0].templateComment, "commento")
        self.assertEqual(len(res[0].slots), 2)
        self.assertEqual(len([True for x in res[0].slots if not isinstance(x, types.SlotDefinition)]), 0)

    def test_DefTemplateParser_SingleSlotDefinition(self):
        res = self._testImpl('ConstructParser', r"""
        (deftemplate NomeTemplate "commento" 
            (slot A)
            (multislot B)
        )
        """).asList()

        self.assertIsInstance(res[0].slots[0], types.SingleSlotDefinition)

    def test_DefTemplateParser_MultiSlotDefinition(self):
        res = self._testImpl('ConstructParser', r"""
        (deftemplate NomeTemplate "commento" 
            (slot A)
            (multislot B)
        )
        """).asList()

        self.assertIsInstance(res[0].slots[1], types.MultiSlotDefinition)

    def test_DefTemplateParser_SlotDefinitions_DefaultAttribute(self):
        res = self._testImpl('ConstructParser', r"""
        (deftemplate NomeTemplate "commento" 
            (slot A 
                (default ?DERIVE))
            (slot B 
                (default ?NONE))
            (slot C 
                (default vC))
        )
        """).asList()

        self.assertIsInstance(res[0].slots[0].attributes[0], types.DefaultAttribute)
        self.assertEqual(res[0].slots[0].attributes[0].defaultValue, types.SPECIAL_VALUES["?DERIVE"])
        self.assertIsInstance(res[0].slots[1].attributes[0], types.DefaultAttribute)
        self.assertEqual(res[0].slots[1].attributes[0].defaultValue, types.SPECIAL_VALUES["?NONE"])
        self.assertIsInstance(res[0].slots[2].attributes[0], types.DefaultAttribute)
        self.assertIsInstance(res[0].slots[2].attributes[0].defaultValue, types.Symbol)

    def test_DefTemplateParser_SlotDefinitions_TypeConstraint(self):
        res = self._testImpl('ConstructParser', r"""
        (deftemplate NomeTemplate "commento" 
            (slot A 
                (type INTEGER))
            (slot B 
                (type ?VARIABLE))
            (slot C 
                (type SYMBOL NUMBER))
        )
        """).asList()

        self.assertIsInstance(res[0].slots[0].attributes[0], types.TypeAttribute)
        self.assertEqual(res[0].slots[0].attributes[0].allowedTypes[0], types.TYPES['INTEGER'])
        self.assertIsInstance(res[0].slots[1].attributes[0], types.TypeAttribute)
        self.assertEqual(res[0].slots[1].attributes[0].allowedTypes[0], types.TYPES["?VARIABLE"])
        self.assertIsInstance(res[0].slots[2].attributes[0], types.TypeAttribute)
        self.assertEqual(len(res[0].slots[2].attributes[0].allowedTypes), 2)
        self.assertEqual(res[0].slots[2].attributes[0].allowedTypes[0], types.TYPES['SYMBOL'])
        self.assertEqual(res[0].slots[2].attributes[0].allowedTypes[1], types.TYPES['NUMBER'])

    def test_DefTemplateParser_SlotDefinitions_BothConstraint(self):
        res = self._testImpl('ConstructParser', r"""
        (deftemplate NomeTemplate "commento" 
            (slot A
                (default 1)
                (type INTEGER))
            (multislot B 
                (default symbol)
                (type ?VARIABLE))
        )
        """).asList()

        self.assertIsInstance(res[0].slots[0].attributes[0], types.DefaultAttribute)
        self.assertIsInstance(res[0].slots[0].attributes[1], types.TypeAttribute)
        self.assertIsInstance(res[0].slots[1].attributes[0], types.DefaultAttribute)
        self.assertIsInstance(res[0].slots[1].attributes[1], types.TypeAttribute)

    def test_DefTemplateParser_AvoidMultipleDefinitionOfSameSlotName(self):
        self.assertRaisesRegexp(ParseFatalException, "Multiple definition for same slot name",
                            self._testImpl, 'DefTemplateConstructParser', r"""
        (deftemplate NomeTemplate "commento" 
            (slot A)
            (multislot A)
            (slot B)
        )
        """)

    def test_DefTemplateParser_SlotDefinitions_AvoidMultipleDefinitionOfSameType_DoubleDefault(self):
        self.assertRaisesRegexp(ParseFatalException, "Multiple definition for same type of attribute",
                            self._testImpl, 'DefTemplateConstructParser', r"""
        (deftemplate NomeTemplate "commento" 
            (slot A
                (default 1)
                (type INTEGER)
                (default 5))
        )
        """)
        
    def test_DefTemplateParser_SlotDefinitions_AvoidMultipleDefinitionOfSameType_DoubleType(self):
        self.assertRaisesRegexp(ParseFatalException, "Multiple definition for same type of attribute",
                            self._testImpl, 'DefTemplateConstructParser', r"""
        (deftemplate NomeTemplate "commento" 
            (slot A
                (default 1)
                (type INTEGER)
                (type SYMBOL))
        )
        """)
        
    def test_VariableParser_GlobalVariable_Normal(self):
        res = self._testImpl('VariableParser', r"""
        ?*gff* 
        """).asList()

        self.assertIsInstance(res[0], types.GlobalVariable)        

    def test_VariableParser_GlobalVariable_AvoidWSBeforeVariableSymbol(self):
        self.assertRaises(ParseException, self._testImpl, 'VariableParser', r"""
        ?* gff*
        """)

    def test_VariableParser_GlobalVariable_AvoidWSAfterVariableSymbol(self):
        self.assertRaises(ParseException, self._testImpl, 'VariableParser', r"""
        ?*gff *
        """)

    def test_VariableParser_GlobalVariable_AvoidWSAfterBeforeVariableSymbol(self):
        self.assertRaises(ParseException, self._testImpl, 'VariableParser', r"""
        ?* gff *
        """)

    def test_DefGlobalConstructParser(self):
        res = self._testImpl('ConstructParser', r"""
        (defglobal MODULE 
            ?*A* = B
        )
        """).asList()

        self.assertIsInstance(res[0], types.DefGlobalConstruct)
        self.assertEqual(res[0].moduleName, "MODULE")
        self.assertEqual(len(res[0].assignments), 1)
        self.assertEqual(len([True for x in res[0].assignments if not isinstance(x, types.GlobalAssignment)]), 0)

    def test_DefGlobalConstructParser_WithoutModuleName(self):
        res = self._testImpl('ConstructParser', r"""
        (defglobal
            ?*A* = B
        )
        """).asList()

        self.assertIsInstance(res[0], types.DefGlobalConstruct)
        self.assertEqual(res[0].moduleName, None)

    def test_DefGlobalConstructParser_MultipleAssignments(self):
        res = self._testImpl('ConstructParser', r"""
        (defglobal 
            ?*A* = B
            ?*B* = A
        )
        """).asList()

        self.assertIsInstance(res[0], types.DefGlobalConstruct)
        self.assertEqual(len(res[0].assignments), 2)
        self.assertEqual(len([True for x in res[0].assignments if not isinstance(x, types.GlobalAssignment)]), 0)

    def test_GlobalAssignmentParser(self):
        res = self._testImpl('GlobalAssignmentParser', r"""
            ?*A* = B
        """).asList()

        self.assertIsInstance(res[0], types.GlobalAssignment)
        self.assertIsInstance(res[0].variable, types.GlobalVariable)
        self.assertIsInstance(res[0].value, types.ParsedType)
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testObjectIsSymbol']
    unittest.main()