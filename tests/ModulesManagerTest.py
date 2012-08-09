'''
Created on 19/lug/2012

@author: Francesco Capozzo
'''
import unittest
from myclips.ModulesManager import ModulesManager,\
    ModulesManagerRedefinitionError, UnknownModuleError
from myclips.Scope import Scope
import logging
from MyClipsBaseTest import MyClipsBaseTest

# disable all logging from modules
#logging.disable(logging.CRITICAL)

class ModulesManagerTest(MyClipsBaseTest):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.MM = ModulesManager()

    def test_AddNewScope(self):
        Scope("MAIN", self.MM)
        
        self.assertTrue(self.MM.isDefined("MAIN"))

    def test_AutoChangeScopeOnAddScope(self):
        prevScope = self.MM.getCurrentScope()
        
        Scope("MAIN", self.MM)
        
        self.assertNotEqual(prevScope, self.MM.getCurrentScope())
        
    def test_NoScopeInNewModulesManager(self):
        self.assertEqual(len(self.MM.getModulesNames()), 0)
        
    def test_CurrentScopeIsNoneInNewModuleManager(self):
        self.assertIsNone(self.MM.getCurrentScope())
        
    def test_CurrentScopeChange(self):
        Scope("MAIN", self.MM)
        Scope("A", self.MM)
        prevScope = self.MM.getCurrentScope()
        self.MM.changeCurrentScope("MAIN")
        self.assertNotEqual(prevScope, self.MM.getCurrentScope())
        self.assertEqual(self.MM.getCurrentScope().moduleName, "MAIN")

    def test_RaiseErrorOnMultipleDefinitionOfTheSameModule(self):
        Scope("MAIN", self.MM)

        self.assertRaisesRegexp(ModulesManagerRedefinitionError, "Cannot redefine defmodule MAIN while it is in use", Scope, "MAIN", self.MM)

    def test_RaiseErrorOnChangeCurrentScopeToInvalid(self):
        self.assertRaisesRegexp(UnknownModuleError, "Unable to find defmodule MAIN", self.MM.changeCurrentScope, "MAIN")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()