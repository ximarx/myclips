'''
Created on 21/lug/2012

@author: Francesco Capozzo
'''
import unittest
from myclips.ModulesManager import ModulesManager
import logging
from myclips.FunctionsManager import FunctionDefinition
from myclips.parser.Types import Symbol, Integer
from myclips.RestrictedManager import MultipleDefinitionError
from myclips.Scope import ScopeImport, Scope

# disable all logging from modules
logging.disable(logging.CRITICAL)

class Test(unittest.TestCase):


    def setUp(self):
        self.MM = ModulesManager()
        self.MM.addMainScope()
        self.scope = self.MM.currentScope


    def test_AddNewFunctionDefinition(self):
        
        self.scope.functions.addDefinition(
                FunctionDefinition(self.scope.moduleName, "NuovaFunzione", object(), Symbol)
            )
        
        self.assertIsInstance(self.scope.functions.getDefinition("NuovaFunzione"),
                                FunctionDefinition)
        self.assertEqual(self.scope.functions.getDefinition("NuovaFunzione").name,
                            "NuovaFunzione")
        
    def test_CanRedefineFunctionIfForwardIsTrue(self):
        self.scope.functions.addDefinition(
                FunctionDefinition(self.scope.moduleName, "NuovaFunzione", object(), Symbol)
            )
        
        self.assertIsInstance(self.scope.functions.getDefinition("NuovaFunzione"),
                                FunctionDefinition)
        self.assertEqual(self.scope.functions.getDefinition("NuovaFunzione").returnTypes,
                            tuple([Symbol]))
        
        self.scope.functions.addDefinition(
                FunctionDefinition(self.scope.moduleName, "NuovaFunzione", object(), Integer)
            )
        self.assertEqual(self.scope.functions.getDefinition("NuovaFunzione").returnTypes,
                            tuple([Integer]))

    def test_CannotRedefineFunctionIfForwardIsFalse(self):
        self.scope.functions.addDefinition(
                FunctionDefinition(self.scope.moduleName, "NuovaFunzione", object(), Symbol, forward=False)
            )
        
        self.assertIsInstance(self.scope.functions.getDefinition("NuovaFunzione"),
                                FunctionDefinition)
        self.assertEqual(self.scope.functions.getDefinition("NuovaFunzione").returnTypes,
                            tuple([Symbol]))
        
        self.assertRaisesRegexp(MultipleDefinitionError, "Cannot redefine deffunction \w+::\w+ while it is in use", self.scope.functions.addDefinition,
                FunctionDefinition(self.scope.moduleName, "NuovaFunzione", object(), Integer)
            )


    def test_CannotRedefineSystemFunctionWithANewDefFunction(self):
        
        self.assertRaisesRegexp(MultipleDefinitionError, "Cannot redefine deffunction \w+::\w+ while it is in use", self.scope.functions.addDefinition,
                FunctionDefinition(self.scope.moduleName, self.scope.functions.systemFunctions[0], object(), Integer)
            )

    def test_CannotRedefineSystemFunctionWithANewSystemFunction(self):
        
        self.assertRaisesRegexp(MultipleDefinitionError, "Cannot redefine deffunction \?SYSTEM\?::\w+ while it is in use", self.scope.functions.registerSystemFunction,
                FunctionDefinition("?SYSTEM?", self.scope.functions.systemFunctions[0], object(), Integer)
            )

    def test_CanRedefineFunctionUntilDefinitionIsImported(self):
        self.scope.functions.addDefinition(
                FunctionDefinition(self.scope.moduleName, "NuovaFunzione", object(), Symbol)
            )
        
        self.assertIsInstance(self.scope.functions.getDefinition("NuovaFunzione"),
                                FunctionDefinition)
        self.assertEqual(self.scope.functions.getDefinition("NuovaFunzione").returnTypes,
                            tuple([Symbol]))
        
        self.scope.functions.addDefinition(
                FunctionDefinition(self.scope.moduleName, "NuovaFunzione", object(), Integer)
            )
        self.assertEqual(self.scope.functions.getDefinition("NuovaFunzione").returnTypes,
                            tuple([Integer]))

        Scope("OTHER", self.MM, imports=[
                ScopeImport("MAIN", Scope.PROMISE_TYPE_FUNCTION, "NuovaFunzione")
            ])
        
        self.assertRaisesRegexp(MultipleDefinitionError, "Cannot redefine deffunction \w+::\w+ while it is in use", self.scope.functions.addDefinition,
                FunctionDefinition(self.scope.moduleName, "NuovaFunzione", object(), Integer)
            )
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()