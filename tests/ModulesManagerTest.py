'''
Created on 19/lug/2012

@author: Francesco Capozzo
'''
import unittest
from myclips.ModulesManager import ModulesManager
from myclips.Scope import Scope



class ModulesManagerTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.MM = ModulesManager()

    def test_AddNewScope(self):
        scope = Scope("MAIN", self.MM)
        self.MM.addScope(scope)
        
        self.assertTrue(self.MM.isDefined("MAIN"))

    def test_AutoChangeScopeOnAddScope(self):
        prevScope = self.MM.getCurrentScope()
        
        scope = Scope("MAIN", self.MM)
        self.MM.addScope(scope)
        
        self.assertNotEqual(prevScope, self.MM.getCurrentScope())
        
    def test_NoScopeInNewModulesManager(self):
        self.assertEqual(len(self.MM.getModulesNames()), 0)
        
    def test_CurrentScopeIsNoneInNewModuleManager(self):
        self.assertIsNone(self.MM.getCurrentScope())
        
    def test_CurrentScopeChange(self):
        self.MM.addScope(Scope("MAIN", self.MM))
        self.MM.addScope(Scope("A", self.MM))
        prevScope = self.MM.getCurrentScope()
        self.MM.changeCurrentScope("MAIN")
        self.assertNotEqual(prevScope, self.MM.getCurrentScope())
        self.assertEqual(self.MM.getCurrentScope().moduleName, "MAIN")

    def test_RaiseErrorOnMultipleDefinitionOfTheSameModule(self):
        scope1 = Scope("MAIN", self.MM)
        self.MM.addScope(scope1)

        scope2 = Scope("MAIN", self.MM)
        self.assertRaisesRegexp(ValueError, "Cannot redefine defmodule MAIN while it is in use", self.MM.addScope, scope2)

    def test_RaiseErrorOnChangeCurrentScopeToInvalid(self):
        self.assertRaisesRegexp(ValueError, "Unable to find defmodule MAIN", self.MM.changeCurrentScope, "MAIN")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()