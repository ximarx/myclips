'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
import unittest
from functions.BaseFunctionTest import BaseFunctionTest
import myclips.parser.Types as types
from myclips.functions.Function import InvalidArgTypeError
from myclips.functions.string.StringCompare import StringCompare


class StringCompareTest(BaseFunctionTest):

    def setUp(self):
        BaseFunctionTest.setUp(self)
        self._functionSetup(StringCompare)

    def test_CompareLeftMin(self):
        
        self.assertTrue(self.forInput(types.String("a"), types.String("z"))
                        .expect(types.Integer(-1)))
        

    def test_CompareRightMin(self):
        
        self.assertTrue(self.forInput(types.String("z"), types.String("a"))
                        .expect(types.Integer(1)))

    def test_CompareEquals(self):
        
        self.assertTrue(self.forInput(types.String("a"), types.String("a"))
                        .expect(types.Integer(0)))

    def test_CompareLeftMinLong(self):
        
        self.assertTrue(self.forInput(types.String("Ciao Mucca"), types.String("Ciao Zucca"))
                        .expect(types.Integer(-1)))
        

    def test_CompareRightMinLong(self):
        
        self.assertTrue(self.forInput(types.String("Ciao Zucca"), types.String("Ciao Mucca"))
                        .expect(types.Integer(1)))

    def test_CompareEqualsLong(self):
        
        self.assertTrue(self.forInput(types.String("acqua"), types.String("acqua"))
                        .expect(types.Integer(0)))


    def test_FunctionCallAsArgument(self):
        if not self.theEnv.modulesManager.currentScope.functions.has("upcase"):
            self.skipTest("upcase not defined")
        
        self.assertTrue(self.forInput(types.FunctionCall("upcase", self.theEnv.modulesManager, [types.String("acqua")]), types.String("acqua"))
                        .expect(types.Integer(cmp("acqua".upper(), "acqua"))))

        
        

    def test_ErrorOnNotStringOrSymbolInput(self):

        self.assertRaises(InvalidArgTypeError, 
                                self.theFunc.do, self.theEnv, types.Integer(10), types.String("a"))

        self.assertRaises(InvalidArgTypeError, 
                                self.theFunc.do, self.theEnv, types.Float(1.5), types.String("a"))
        
        self.assertRaises(InvalidArgTypeError, 
                                self.theFunc.do, self.theEnv, [types.Symbol("bla")], types.String("a"))
        
        self.assertRaises(InvalidArgTypeError, 
                                self.theFunc.do, self.theEnv, types.String("a"), types.Integer(10))

        self.assertRaises(InvalidArgTypeError, 
                                self.theFunc.do, self.theEnv, types.String("a"), types.Float(1.5))
        
        self.assertRaises(InvalidArgTypeError, 
                                self.theFunc.do, self.theEnv, types.String("a"), [types.Symbol("bla")])
        

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()