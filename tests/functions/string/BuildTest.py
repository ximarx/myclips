'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
import unittest
from functions.BaseFunctionTest import BaseFunctionTest
import myclips.parser.Types as types
from myclips.functions.Function import InvalidArgTypeError
from myclips.functions.string.Build import Build


class BuildTest(BaseFunctionTest):

    def setUp(self):
        BaseFunctionTest.setUp(self)
        self._functionSetup(Build)

    def test_BuildRule(self):
        
        preRules = len(self.theEnv.network.rules)
        
        theString = """
        (defrule r (A B C) => )
        """
        theResult = self.theFunc.do(self.theEnv, types.String(theString))
        
        self.assertEqual(theResult, types.Symbol("TRUE"))
        self.assertEqual(len(self.theEnv.network.rules), preRules + 1)

    def test_FirstRuleBuiltOnly(self):
        
        preRules = len(self.theEnv.network.rules)
        
        theString = """
        (defrule r (A B C) => )
        (defrule w (A B C) => )
        """
        theResult = self.theFunc.do(self.theEnv, types.String(theString))
        
        self.assertEqual(theResult, types.Symbol("TRUE"))
        self.assertEqual(len(self.theEnv.network.rules), preRules + 1)
        

    def test_BuildModule(self):

        self.assertFalse(self.theEnv.modulesManager.isDefined("A"))
        
        theString = """
        (defmodule A)
        """
        theResult = self.theFunc.do(self.theEnv, types.String(theString))
        
        self.assertEqual(theResult, types.Symbol("TRUE"))
        self.assertTrue(self.theEnv.modulesManager.isDefined("A"))


    def test_FirstModuleBuiltOnly(self):

        self.assertFalse(self.theEnv.modulesManager.isDefined("A"))
        self.assertFalse(self.theEnv.modulesManager.isDefined("B"))
        
        theString = """
        (defmodule A)
        (defmodule B)
        """
        theResult = self.theFunc.do(self.theEnv, types.String(theString))
        
        self.assertEqual(theResult, types.Symbol("TRUE"))
        self.assertTrue(self.theEnv.modulesManager.isDefined("A"))
        self.assertFalse(self.theEnv.modulesManager.isDefined("B"))

    def test_ScopeRevertedAfterScopeChangeOnModuleBuilt(self):
        
        theOldScope = self.theEnv.modulesManager.currentScope.moduleName
        
        theString = """
        (defmodule A)
        """
        theResult = self.theFunc.do(self.theEnv, types.String(theString))
        
        self.assertEqual(theResult, types.Symbol("TRUE"))
        self.assertTrue(self.theEnv.modulesManager.isDefined("A"))
        
        self.assertEqual(theOldScope, self.theEnv.modulesManager.currentScope.moduleName)
        

    def test_ScopeRevertedAfterScopeChangeOnRuleBuilt(self):
        
        theOldScope = self.theEnv.modulesManager.currentScope.moduleName
        
        theString = """
        (defmodule A)
        """
        theResult = self.theFunc.do(self.theEnv, types.String(theString))
        
        self.assertEqual(theResult, types.Symbol("TRUE"))
        self.assertTrue(self.theEnv.modulesManager.isDefined("A"))

        theString = """
        (defrule A::blabla (A B C) => )
        """
        theResult = self.theFunc.do(self.theEnv, types.String(theString))
        
        self.assertEqual(theResult, types.Symbol("TRUE"))
        
        self.assertEqual(theOldScope, self.theEnv.modulesManager.currentScope.moduleName)
        

    def test_ErrorOnNotStringOrSymbolInpyt(self):
        
        self.assertRaisesRegexp(InvalidArgTypeError, "Function build expected argument #1 to be of type string or symbol", 
                                self.theFunc.do, self.theEnv, types.Integer(10))

        self.assertRaisesRegexp(InvalidArgTypeError, "Function build expected argument #1 to be of type string or symbol", 
                                self.theFunc.do, self.theEnv, types.Float(1.5))
        
        self.assertRaisesRegexp(InvalidArgTypeError, "Function build expected argument #1 to be of type string or symbol", 
                                self.theFunc.do, self.theEnv, [types.Symbol("bla")])
        

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()