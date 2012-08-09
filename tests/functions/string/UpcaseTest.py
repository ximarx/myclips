'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
import unittest
from myclips.functions.string.Upcase import Upcase
from functions.BaseFunctionTest import BaseFunctionTest
import myclips.parser.Types as types
import string
from myclips.functions.Function import InvalidArgTypeError


class UpcaseTest(BaseFunctionTest):

    def setUp(self):
        BaseFunctionTest.setUp(self)
        self._functionSetup(Upcase)

    def test_StringToUpcase(self):
        theString = "This Is a MiXed StrIng"
        theResult = self.theFunc.do(self.theEnv, types.String(theString))
        
        self.assertEqual(len(set(string.ascii_lowercase).intersection(set(theResult.evaluate()))), 0)
        
    def test_SymbolToUpcase(self):
        
        theSymbol = "aSymBol"
        theResult = self.theFunc.do(self.theEnv, types.Symbol(theSymbol))
        
        self.assertEqual(len(set(string.ascii_lowercase).intersection(set(theResult.evaluate()))), 0)

    def test_InputClassKept(self):
        
        theString = "This_Is_a_MiXed_StrIng"
        theResultString = self.theFunc.do(self.theEnv, types.String(theString))
        theResultSymbol = self.theFunc.do(self.theEnv, types.Symbol(theString))
        
        self.assertEqual(theResultString.__class__, types.String)
        self.assertEqual(theResultSymbol.__class__, types.Symbol)
        
    def test_FunctionResultToUpcase(self):
        
        theString = types.String("This_Is_a_MiXed_StrIng")
        theFuncCall = types.FunctionCall(types.Symbol("upcase"), self.theEnv.modulesManager, [theString])
        theResult = self.theFunc.do(self.theEnv, theFuncCall)
        
        self.assertEqual(theResult.__class__, types.String)
        self.assertEqual(len(set(string.ascii_lowercase).intersection(set(theResult.evaluate()))), 0)
        self.assertEqual(theResult, self.theFunc.do(self.theEnv, theString))

    def test_ErrorOnNotStringOrSymbolInpyt(self):
        
        self.assertRaisesRegexp(InvalidArgTypeError, "Function upcase expected argument #1 to be of type string or symbol", 
                                self.theFunc.do, self.theEnv, types.Integer(10))

        self.assertRaisesRegexp(InvalidArgTypeError, "Function upcase expected argument #1 to be of type string or symbol", 
                                self.theFunc.do, self.theEnv, types.Float(1.5))
        
        self.assertRaisesRegexp(InvalidArgTypeError, "Function upcase expected argument #1 to be of type string or symbol", 
                                self.theFunc.do, self.theEnv, [types.Symbol("bla")])
        

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()