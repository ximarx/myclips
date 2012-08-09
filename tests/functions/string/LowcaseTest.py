'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
import unittest
from myclips.functions.string.Lowcase import Lowcase
from functions.BaseFunctionTest import BaseFunctionTest
import myclips.parser.Types as types
import string
from myclips.functions.Function import InvalidArgTypeError


class LowcaseTest(BaseFunctionTest):

    def setUp(self):
        BaseFunctionTest.setUp(self)
        self._functionSetup(Lowcase)

    def test_StringToLowcase(self):
        theString = "This Is a MiXed StrIng"
        theResult = self.theFunc.do(self.theEnv, types.String(theString))
        
        self.assertEqual(len(set(string.ascii_uppercase).intersection(set(theResult.evaluate()))), 0)
        
    def test_SymbolToLowcase(self):
        
        theSymbol = "aSymBol"
        theResult = self.theFunc.do(self.theEnv, types.Symbol(theSymbol))
        
        self.assertEqual(len(set(string.ascii_uppercase).intersection(set(theResult.evaluate()))), 0)

    def test_InputClassKept(self):
        
        theString = "This_Is_a_MiXed_StrIng"
        theResultString = self.theFunc.do(self.theEnv, types.String(theString))
        theResultSymbol = self.theFunc.do(self.theEnv, types.Symbol(theString))
        
        self.assertEqual(theResultString.__class__, types.String)
        self.assertEqual(theResultSymbol.__class__, types.Symbol)
        
    def test_FunctionResultToLowcase(self):
        
        theString = types.String("This_Is_a_MiXed_StrIng")
        theFuncCall = types.FunctionCall(types.Symbol("lowcase"), self.theEnv.modulesManager, [theString])
        theResult = self.theFunc.do(self.theEnv, theFuncCall)
        
        self.assertEqual(theResult.__class__, types.String)
        self.assertEqual(len(set(string.ascii_uppercase).intersection(set(theResult.evaluate()))), 0)
        self.assertEqual(theResult, self.theFunc.do(self.theEnv, theString))

    def test_ErrorOnNotStringOrSymbolInpyt(self):
        
        self.assertRaisesRegexp(InvalidArgTypeError, "Function lowcase expected argument #1 to be of type string or symbol", 
                                self.theFunc.do, self.theEnv, types.Integer(10))

        self.assertRaisesRegexp(InvalidArgTypeError, "Function lowcase expected argument #1 to be of type string or symbol", 
                                self.theFunc.do, self.theEnv, types.Float(1.5))
        
        self.assertRaisesRegexp(InvalidArgTypeError, "Function lowcase expected argument #1 to be of type string or symbol", 
                                self.theFunc.do, self.theEnv, [types.Symbol("bla")])
        

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()