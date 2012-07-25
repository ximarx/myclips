'''
Created on 25/lug/2012

@author: Francesco Capozzo
'''
import unittest
import logging
import myclips.parser.Types as types

logging.disable(logging.CRITICAL)

class BaseParsedTypeTest(unittest.TestCase):

    def test_SymbolIsEqualSymbol(self):
        
        s1 = types.Symbol("FirstSymbol")
        s2 = types.Symbol("FirstSymbol")
        
        self.assertTrue(s1 == s2)
        
        
    def test_SymbolIsNotEqualSymbol(self):

        s1 = types.Symbol("FirstSymbol")
        s2 = types.Symbol("SecondSymbol")
        
        self.assertFalse(s1 == s2)

    def test_SymbolIsNotEqualStringWithSameContent(self):
        
        s1 = types.Symbol("FirstSymbol")
        s2 = types.String("FirstSymbol")

        self.assertFalse(s1 == s2)
        
    def test_SymbolIsALexeme(self):
        
        s1 = types.Symbol("FirstSymbol")
        
        self.assertIsInstance(s1, types.Lexeme)
        
    def test_SymbolIsNotANumber(self):
        
        s1 = types.Symbol("FirstSymbol")
        
        self.assertNotIsInstance(s1, types.Number)

    def test_IntegerIsEqualInteger(self):
        
        s1 = types.Integer("1")
        s2 = types.Integer("1")
        
        self.assertTrue(s1 == s2)
        
        
    def test_IntegerIsNotEqualInteger(self):

        s1 = types.Integer("1")
        s2 = types.Integer("2")
        
        self.assertFalse(s1 == s2)

    def test_IntegerIsNotEqualFloatWithSameContent(self):
        
        s1 = types.Integer("1")
        s2 = types.Float("1")

        self.assertFalse(s1 == s2)
        
    def test_IntegerIsANumber(self):
        
        s1 = types.Integer("1")
        
        self.assertIsInstance(s1, types.Number)
        
    def test_IntegerIsNotALexeme(self):
        
        s1 = types.Integer("1")
        
        self.assertNotIsInstance(s1, types.Lexeme)


        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()