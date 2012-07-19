'''
Created on 19/lug/2012

@author: Francesco Capozzo
'''
import unittest
from myclips.Scope import Scope, ScopeExport
from myclips.ModulesManager import ModulesManager


class ScopeTest(unittest.TestCase):


    def test_SimpleScopeGeneration(self):
        scope = Scope("MAIN", ModulesManager())
        
        
        self.assertIsInstance(scope, Scope)
        self.assertEqual(scope.moduleName, "MAIN")
    
    
    def test_ExportedDefinitionIsImportable(self):
        scope = Scope("MAIN", ModulesManager(), exports=[
                            ScopeExport(Scope.PROMISE_TYPE_TEMPLATE, 'template'),
                            ScopeExport(Scope.PROMISE_TYPE_FUNCTION, 'function'),
                            ScopeExport(Scope.PROMISE_TYPE_GLOBAL, '*global*')
                        ])
        
        self.assertTrue(scope.isImportable(Scope.PROMISE_TYPE_TEMPLATE, "template"))
        self.assertTrue(scope.isImportable(Scope.PROMISE_TYPE_FUNCTION, "function"))
        self.assertTrue(scope.isImportable(Scope.PROMISE_TYPE_GLOBAL, "*global*"))

        
    def test_NotExportedDefinitionIsNotImportable(self):
        scope = Scope("MAIN", ModulesManager(), exports=[
                            ScopeExport(Scope.PROMISE_TYPE_TEMPLATE, 'template-other'),
                            ScopeExport(Scope.PROMISE_TYPE_FUNCTION, 'function-other'),
                            ScopeExport(Scope.PROMISE_TYPE_GLOBAL, '*global-other*')
                        ])
        
        self.assertFalse(scope.isImportable(Scope.PROMISE_TYPE_TEMPLATE, "template"))
        self.assertFalse(scope.isImportable(Scope.PROMISE_TYPE_FUNCTION, "function"))
        self.assertFalse(scope.isImportable(Scope.PROMISE_TYPE_GLOBAL, "*global*"))

     
    def test_ExportAllIsImportableAlways(self):
        scope = Scope("MAIN", ModulesManager(), exports=[
                            ScopeExport(Scope.PROMISE_TYPE_TEMPLATE, Scope.PROMISE_NAME_ALL),
                            ScopeExport(Scope.PROMISE_TYPE_FUNCTION, Scope.PROMISE_NAME_ALL),
                            ScopeExport(Scope.PROMISE_TYPE_GLOBAL, Scope.PROMISE_NAME_ALL)
                        ])
        
        self.assertTrue(scope.isImportable(Scope.PROMISE_TYPE_TEMPLATE, "template"))
        self.assertTrue(scope.isImportable(Scope.PROMISE_TYPE_FUNCTION, "function"))
        self.assertTrue(scope.isImportable(Scope.PROMISE_TYPE_GLOBAL, "*global*"))

        
    def test_ExportEverythingIsImportableAlways(self):
        scope = Scope("MAIN", ModulesManager(), exports=[
                            ScopeExport(Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL),
                        ])
        
        self.assertTrue(scope.isImportable(Scope.PROMISE_TYPE_TEMPLATE, "template"))
        self.assertTrue(scope.isImportable(Scope.PROMISE_TYPE_FUNCTION, "function"))
        self.assertTrue(scope.isImportable(Scope.PROMISE_TYPE_GLOBAL, "*global*"))

    def test_ExportNoneRemoveEverything(self):
        scope = Scope("MAIN", ModulesManager(), exports=[
                            ScopeExport(Scope.PROMISE_TYPE_TEMPLATE, 'template'),
                            ScopeExport(Scope.PROMISE_TYPE_FUNCTION, 'function'),
                            ScopeExport(Scope.PROMISE_TYPE_GLOBAL, '*global*'),
                            ScopeExport(Scope.PROMISE_NAME_NONE, Scope.PROMISE_NAME_NONE)
                        ])
        
        self.assertFalse(scope.isImportable(Scope.PROMISE_TYPE_TEMPLATE, "template"))
        self.assertFalse(scope.isImportable(Scope.PROMISE_TYPE_FUNCTION, "function"))
        self.assertFalse(scope.isImportable(Scope.PROMISE_TYPE_GLOBAL, "*global*"))

    def test_ExportNoneForATypeRemoveEverythingForTheType(self):
        scope = Scope("MAIN", ModulesManager(), exports=[
                            ScopeExport(Scope.PROMISE_TYPE_TEMPLATE, 'template'),
                            ScopeExport(Scope.PROMISE_TYPE_FUNCTION, 'function'),
                            ScopeExport(Scope.PROMISE_TYPE_GLOBAL, '*global*'),
                            ScopeExport(Scope.PROMISE_TYPE_GLOBAL, Scope.PROMISE_NAME_NONE)
                        ])
        
        self.assertTrue(scope.isImportable(Scope.PROMISE_TYPE_TEMPLATE, "template"))
        self.assertTrue(scope.isImportable(Scope.PROMISE_TYPE_FUNCTION, "function"))
        self.assertFalse(scope.isImportable(Scope.PROMISE_TYPE_GLOBAL, "*global*"))

    def test_ExportNoneForATypeRemoveEverythingForTheTypeIfPreviousExportEverythingExists(self):
        scope = Scope("MAIN", ModulesManager(), exports=[
                            ScopeExport(Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL),
                            ScopeExport(Scope.PROMISE_TYPE_GLOBAL, Scope.PROMISE_NAME_NONE)
                        ])
        
        self.assertTrue(scope.isImportable(Scope.PROMISE_TYPE_TEMPLATE, "template"))
        self.assertTrue(scope.isImportable(Scope.PROMISE_TYPE_FUNCTION, "function"))
        self.assertFalse(scope.isImportable(Scope.PROMISE_TYPE_GLOBAL, "*global*"))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()