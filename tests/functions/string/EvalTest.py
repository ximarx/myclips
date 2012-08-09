'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
import unittest
from functions.BaseFunctionTest import BaseFunctionTest
import myclips.parser.Types as types
from myclips.functions.Function import InvalidArgTypeError
from myclips.functions.string.Eval import Eval


class EvalTest(BaseFunctionTest):

    def setUp(self):
        BaseFunctionTest.setUp(self)
        self._functionSetup(Eval)

    def test_EvalFunctionCall(self):
        
        if not self.theEnv.modulesManager.currentScope.functions.has("+"):
            self.skipTest("+ not defined")
        
        theString = """
        (+ 1 1)
        """
        theResult = self.theFunc.do(self.theEnv, types.String(theString))
        
        self.assertEqual(theResult, types.Integer(2))


    def test_EvalBaseTypes(self):
        
        typesMap = {"1" : types.Integer(1),
                    "1.5": types.Float(1.5),
                    "symbol": types.Symbol("symbol"),
                    '"string"': types.String("string")
                    }
        
        for (theString, theResultCmp) in typesMap.items():
            theResult = self.theFunc.do(self.theEnv, types.String(theString))
            self.assertEqual(theResult, theResultCmp)
            
    def test_EvalGlobalVar(self):
        
        from myclips.GlobalsManager import GlobalVarDefinition
        
        (self.theEnv
                .modulesManager
                    .currentScope
                        .globalsvars
                            .addDefinition(
                                GlobalVarDefinition(
                                        self.theEnv.modulesManager.currentScope.moduleName,
                                        "?*a*",
                                        types.GlobalAssignment(types.GlobalVariable(types.Symbol("a"), self.theEnv.modulesManager, True),
                                                               types.Integer(1)))))
        
        self.assertTrue(self
                            .forInput(types.String("?*a*"))
                            .expect(types.Integer(1)))
        
        
        
    def test_EvalReturnFalseIfVariableIsTheOnlyParsed(self):
        
        self.assertTrue(self
                            .forInput(types.String("?a"))
                            .expect(types.Symbol("FALSE")))


    def test_ErrorOnDefModuleEval(self):
        
        theString = """
        (defmodule A)
        """
        theResult = self.theFunc.do(self.theEnv, types.String(theString))
        
        self.assertEqual(theResult, types.Symbol("FALSE"))
        

    def test_ErrorOnDefRuleEval(self):
        
        theString = """
        (defrule r (A B C) => )
        """
        theResult = self.theFunc.do(self.theEnv, types.String(theString))
        
        self.assertEqual(theResult, types.Symbol("FALSE"))


    def test_ErrorOnNotStringOrSymbolInpyt(self):
        
        self.assertRaisesRegexp(InvalidArgTypeError, "Function eval expected argument #1 to be of type string or symbol", 
                                self.theFunc.do, self.theEnv, types.Integer(10))

        self.assertRaisesRegexp(InvalidArgTypeError, "Function eval expected argument #1 to be of type string or symbol", 
                                self.theFunc.do, self.theEnv, types.Float(1.5))
        
        self.assertRaisesRegexp(InvalidArgTypeError, "Function eval expected argument #1 to be of type string or symbol", 
                                self.theFunc.do, self.theEnv, [types.Symbol("bla")])
        

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()