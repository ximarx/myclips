'''
Created on 19/lug/2012

@author: Francesco Capozzo
'''
import unittest
from myclips.Scope import Scope, ScopeExport, ScopeImport,\
    ScopeDefinitionConflict, ScopeDefinitionNotFound
from myclips.ModulesManager import ModulesManager
from myclips.GlobalsManager import GlobalVarDefinition
import logging
from MyClipsBaseTest import MyClipsBaseTest

# disable all logging from modules
#logging.disable(logging.CRITICAL)

class ScopeTest(MyClipsBaseTest):


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

    def test_ExportAListOfConstructsIsPossible(self):
        scope = Scope("MAIN", ModulesManager(), exports=[
                            ScopeExport(Scope.PROMISE_TYPE_GLOBAL, ["?*a*","?*b*","?*c*" ])
                        ])
        
        self.assertTrue(scope.isImportable(Scope.PROMISE_TYPE_GLOBAL, "?*a*"))
        self.assertTrue(scope.isImportable(Scope.PROMISE_TYPE_GLOBAL, "?*b*"))
        self.assertTrue(scope.isImportable(Scope.PROMISE_TYPE_GLOBAL, "?*c*"))
        self.assertFalse(scope.isImportable(Scope.PROMISE_TYPE_GLOBAL, "?*unknown*"))
        
    def test_ImportAListOfConstructsIsPossible(self):
        MM = ModulesManager()
        scopeM = Scope("MAIN", MM, exports=[
                            ScopeExport(Scope.PROMISE_TYPE_GLOBAL, ["?*a*","?*b*","?*c*" ])
                        ])
        
        scopeM.globalsvars.addDefinition(GlobalVarDefinition(scopeM.moduleName, "?*a*", object()))
        scopeM.globalsvars.addDefinition(GlobalVarDefinition(scopeM.moduleName, "?*b*", object()))
        scopeM.globalsvars.addDefinition(GlobalVarDefinition(scopeM.moduleName, "?*c*", object()))
        
        
        scope1 = Scope("FIRST", MM, imports=[
                            ScopeImport("MAIN", Scope.PROMISE_TYPE_GLOBAL, ["?*a*", "?*b*"])
                        ])
        
        self.assertTrue(scope1.globalsvars.has("?*a*"))
        self.assertTrue(scope1.globalsvars.has("?*b*"))
        self.assertFalse(scope1.globalsvars.has("?*c*"))
        
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

    def test_ImportDefinitionFromAnotherScope(self):
        MM = ModulesManager()
        
        scope1 = Scope("MAIN", MM, exports=[
                            ScopeExport(Scope.PROMISE_TYPE_GLOBAL, "?*A*"),
                            ScopeExport(Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL)
                        ])
        
        scope1.globalsvars.addDefinition(GlobalVarDefinition(scope1.moduleName, "?*A*", object()))
        
        scope2 = Scope("SECOND", MM, imports=[
                            ScopeImport("MAIN", Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL)
                        ])
        

        self.assertTrue(scope2.globalsvars.has("?*A*"))
        self.assertEqual(scope2.globalsvars.getDefinition("?*A*").moduleName, "MAIN")
        
    def test_ImportDefinitionFromAnotherScopeWithObserver(self):
        MM = ModulesManager()
        
        scope1 = Scope("MAIN", MM, exports=[
                            ScopeExport(Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL)
                        ])
        
        
        scope2 = Scope("SECOND", MM, imports=[
                            ScopeImport("MAIN", Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL)
                        ])
        

        scope1.globalsvars.addDefinition(GlobalVarDefinition(scope1.moduleName, "?*A*", object()))
        
        self.assertTrue(scope2.globalsvars.has("?*A*"))
        self.assertEqual(scope2.globalsvars.getDefinition("?*A*").moduleName, "MAIN")
        
    def test_GuardOnRecursiveInclusion(self):
        
        MM = ModulesManager()
        
        scopeM = Scope("MAIN", MM, exports=[
                                ScopeExport(Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL)
                            ])
        

        scope1 = Scope("FIRST", MM, exports=[
                                ScopeExport(Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL)
                            ], imports=[
                                ScopeImport("MAIN", Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL),
                            ])
        

        
        scope2 = Scope("SECOND", MM, exports=[
                                ScopeExport(Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL)
                            ], imports=[
                                ScopeImport("MAIN", Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL),
                                ScopeImport("FIRST", Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL)
                            ])
        

        scopeM.globalsvars.addDefinition(GlobalVarDefinition(scopeM.moduleName, "?*A*", object()))
        
        self.assertTrue(scopeM.globalsvars.has("?*A*"))
        self.assertTrue(scope1.globalsvars.has("?*A*"))
        self.assertTrue(scope2.globalsvars.has("?*A*"))
        self.assertEqual(scopeM.globalsvars.getDefinition("?*A*").moduleName, "MAIN")
        self.assertEqual(scope1.globalsvars.getDefinition("?*A*").moduleName, "MAIN")
        self.assertEqual(scope2.globalsvars.getDefinition("?*A*").moduleName, "MAIN")
        self.assertEqual(scopeM.globalsvars.getDefinition("?*A*"), scope1.globalsvars.getDefinition("?*A*"))
        self.assertEqual(scopeM.globalsvars.getDefinition("?*A*"), scope2.globalsvars.getDefinition("?*A*"))
        self.assertEqual(scope1.globalsvars.getDefinition("?*A*"), scope2.globalsvars.getDefinition("?*A*"))
        
    def test_ListenerCleanupOnScopeCreationFail(self):
        
        MM = ModulesManager()
        
        scopeM = Scope("MAIN", MM, exports=[
                                ScopeExport(Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL)
                            ])
        
        
        scopeM.globalsvars.addDefinition(GlobalVarDefinition(scopeM.moduleName, "?*A*", object()))

        scope1 = Scope("FIRST", MM, exports=[
                                ScopeExport(Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL)
                            ])
        
        
        scope1.globalsvars.addDefinition(GlobalVarDefinition(scope1.moduleName, "?*A*", object()))

        
        self.assertRaises(ScopeDefinitionConflict, Scope, "SECOND", MM, exports=[
                                    ScopeExport(Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL)
                                ], imports=[
                                    ScopeImport("MAIN", Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL),
                                    ScopeImport("FIRST", Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL)
                                ])
        
        self.assertEqual(len(scope1.globalsvars.getObservers(scope1.globalsvars.EVENT_NEW_DEFINITION)), 0)
        self.assertEqual(len(scopeM.globalsvars.getObservers(scopeM.globalsvars.EVENT_NEW_DEFINITION)), 0)
        
    def test_ErrorOnInclusionOfNotDefinedModule(self):

        MM = ModulesManager()
        self.assertRaises(ScopeDefinitionNotFound, Scope, "MAIN", MM, imports=[
                                ScopeImport("FIRST", Scope.PROMISE_NAME_ALL, Scope.PROMISE_NAME_ALL)
                            ])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()