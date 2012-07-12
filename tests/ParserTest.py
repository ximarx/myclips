'''
Created on 11/lug/2012

@author: Francesco Capozzo
'''
import unittest
from myclips.parser.Parser import Parser
import myclips.parser.types as types

class ParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def _testImpl(self, parsername, parsable, parseAll=False):
        return self.parser.getSParser(parsername).parseString(parsable, parseAll)

    def test_deffact_Normal(self):
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
        res = self._testImpl('DefFactsConstructParser', r"""
        (deffacts nome1
            (1 2 3)
            (a b c)
        )
        """).asList()
        
        self.assertEqual(res[0].deffactsComment, None)



    def test_deffact_SpaceBetweenLparAndDeffacts(self):
        res = self._testImpl('DefFactsConstructParser', r"""
        ( deffacts nome1 "commento1"
            (1 2 3)
            (a b c)
        )
        """).asList()
        
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], types.DefFactsConstruct)
    
    def test_deffact_NLBetweenLparAndDeffacts(self):
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
        res = self._testImpl('DefFactsConstructParser', r"""
        (deffacts nome1 "commento1"
            (1 2 3)
            (a b c)
        )
        """).asList()
        
        self.assertEqual(len(res[0].rhs), 2)
        self.assertIsInstance(res[0].rhs[0], types.OrderedRhsPattern)
        self.assertIsInstance(res[0].rhs[1], types.OrderedRhsPattern)


    def test_orderedrhspattern_Normal(self):
        res = self._testImpl('RhsPatternParser', r"""
        (A b c)
        """).asList()
        
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], types.OrderedRhsPattern)
        self.assertIsInstance(res[0].content[0], types.Symbol)
        self.assertIsInstance(res[0].content[1], types.Symbol)
        self.assertIsInstance(res[0].content[2], types.Symbol)

    def test_orderedrhspattern_WithSingleFieldVariable(self):
        res = self._testImpl('RhsPatternParser', r"""
        (A ?b c)
        """).asList()
        
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], types.OrderedRhsPattern)
        self.assertIsInstance(res[0].content[0], types.Symbol)
        self.assertIsInstance(res[0].content[1], types.SingleFieldVariable)
        self.assertIsInstance(res[0].content[2], types.Symbol)

    def test_orderedrhspattern_WithInteger(self):
        res = self._testImpl('RhsPatternParser', r"""
        (A 1 c)
        """).asList()
        
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], types.OrderedRhsPattern)
        self.assertIsInstance(res[0].content[0], types.Symbol)
        self.assertIsInstance(res[0].content[1], types.Integer)
        self.assertIsInstance(res[0].content[2], types.Symbol)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testObjectIsSymbol']
    unittest.main()