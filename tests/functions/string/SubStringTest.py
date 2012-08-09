'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
import unittest
from functions.BaseFunctionTest import BaseFunctionTest
import myclips.parser.Types as types
from myclips.functions.Function import InvalidArgTypeError
from myclips.functions.string.SubString import SubString


class SubStringTest(BaseFunctionTest):

    def setUp(self):
        BaseFunctionTest.setUp(self)
        self._functionSetup(SubString)


    def test_SubStingOfString(self):
        
        self.assertTrue(self.forInput(types.Integer(1), types.Integer(3), types.String("ciao"))
                        .expect(types.String("cia")))

    def test_SubStingOfSymbol(self):
        
        self.assertTrue(self.forInput(types.Integer(1), types.Integer(3), types.Symbol("ciao"))
                        .expect(types.String("cia")))

    def test_SingleCharFromString(self):
        
        self.assertTrue(self.forInput(types.Integer(3), types.Integer(3), types.String("ciao"))
                        .expect(types.String("a")))


    def test_NullStringIfFirstArgIsGreaterThanSecond(self):
        
        self.assertTrue(self.forInput(types.Integer(3), types.Integer(1), types.String("ciao"))
                        .expect(types.String("")))


    def test_ErrorOnInvalidInput(self):

        self.assertRaises(InvalidArgTypeError, 
                                self.theFunc.do, self.theEnv, types.Symbol("1"), types.Integer(2), types.String("blabla"))
        
        self.assertRaises(InvalidArgTypeError, 
                                self.theFunc.do, self.theEnv, types.Integer(2), types.Symbol("1"), types.String("blabla"))
        
        self.assertRaises(InvalidArgTypeError, 
                                self.theFunc.do, self.theEnv, types.Integer(1), types.Integer(2), types.Integer("100"))

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()