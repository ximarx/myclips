'''
Created on 19/lug/2012

@author: Francesco Capozzo
'''
from myclips.Observer import Observer
from myclips.TemplatesManager import TemplatesManager
from myclips.GlobalsManager import GlobalsManager
from myclips.FunctionsManager import FunctionsManager
from myclips.RestrictedManager import RestrictedDefinition, RestrictedManager

class Scope(Observer):
    '''
    Describe and give access to all construct available
    in a specific scope while parsing
    '''

    PROMISE_TYPE_TEMPLATE = 'deftemplate'
    PROMISE_TYPE_FUNCTION = 'deffunction'
    PROMISE_TYPE_GLOBAL = 'defglobal'
    PROMISE_NAME_ALL = '?ALL'
    PROMISE_NAME_NONE = '?NONE'

    def __init__(self, moduleName, mManager, imports=None, exports=None):
        '''
        All managers are relative to this instance only
        '''
        self._templates = TemplatesManager(self)
        self._globals = GlobalsManager(self)
        self._functions = FunctionsManager(self)
        self._moduleName = moduleName
        self._moduleManager = mManager
        self._exports = _ScopeExportPromise(exports)
        
        if imports is None:
            imports = []
            
        self._imports = imports
            
        typeMap = {
            Scope.PROMISE_TYPE_TEMPLATE   : self.templates,
            Scope.PROMISE_TYPE_FUNCTION   : self.functions,
            Scope.PROMISE_TYPE_GLOBAL     : self.globalsvars
        }
            
        try:
            
            # imports buffer: i need it
            # because otherwise i will destroy
            # Scope own definition on import ?NONE
            tmp_imports = {}
                
            for imDef in imports:
                if not isinstance(imDef, ScopeImport):
                    raise ValueError("Export definition must be a ScopeExport instance")
                
                assert isinstance(imDef, ScopeImport)
                # first thing: let's check the module
                try:
                    otherModDef = self._moduleManager.getScope(imDef.iModule)
                    
                    otherTypeMap = {
                        Scope.PROMISE_TYPE_TEMPLATE   : otherModDef.templates,
                        Scope.PROMISE_TYPE_FUNCTION   : otherModDef.functions,
                        Scope.PROMISE_TYPE_GLOBAL     : otherModDef.globalsvars
                    }
                    
                    
                except KeyError:
                    raise ScopeDefinitionNotFound("Unable to find defmodule {0}".format(imDef.iModule))
                else:
                    if imDef.iType == Scope.PROMISE_NAME_NONE:
                        if tmp_imports.has_key(imDef.iModule):
                            del tmp_imports[imDef.iModule]
                        #else it's ok, i don't any def yet
                    else:
                        importQueue = []
                        if imDef.iType == Scope.PROMISE_NAME_ALL:
                            # i have to import everything already defined
                            # and set a listener on the scope
                            # for future definitions
                            importQueue = [Scope.PROMISE_TYPE_FUNCTION, Scope.PROMISE_TYPE_GLOBAL, Scope.PROMISE_TYPE_TEMPLATE]
                        else:
                            importQueue = [imDef.iType]
                        # i know what i have to import now
                        for iqType in importQueue:
                            
                            # get the list of definition i need to import
                            imported = otherModDef.getExports(iqType, imDef.iName)
    
                            # if i haven't imported anything for this module
                            # yet, just create a skeleton dict                        
                            if not tmp_imports.has_key(imDef.iModule):
                                mod_imports = {Scope.PROMISE_TYPE_FUNCTION: {},
                                               Scope.PROMISE_TYPE_GLOBAL: {},
                                               Scope.PROMISE_TYPE_TEMPLATE: {}}
                                tmp_imports[imDef.iModule] = mod_imports
                            else:
                                # otherwise i use the one i already got
                                mod_imports = tmp_imports[imDef.iModule]
    
                            # get the subdict for the import type i need
                            mod_imports = mod_imports[iqType]
                            
                            # time to iterate over every single import definition
                            # if i got a definition with the same name
                            # i raise a ScopeDefinitionConflict,
                            # and abort scope creation this way
                            for (defName, defObj) in imported:
                                if mod_imports.has_key(defName):
                                    raise ScopeDefinitionConflict(("Cannot define defmodule {0} "
                                                                  + "because of an import/export conflict caused by the {0} {1}").format(
                                                        self.moduleName,
                                                        iqType,
                                                        defName
                                                ))
                                else:
                                    # otherwise i definite it and i'm happy
                                    mod_imports[defName] = defObj
                            
                            # if i get a ?ALL definition
                            # i have to add a listner in the other scope
                            # so when there is a new construct definition
                            # the definition is forwarded here
                            if imDef.iName == Scope.PROMISE_NAME_ALL:
                                otherTypeMap[iqType].registerObserver(otherTypeMap[iqType].EVENT_NEW_DEFINITION, self)
            
            # time to merge all imports with the definitions
            # avaiables in the scope
            
            
            for (modName, defDict) in tmp_imports.items():
                for (constType, constDict) in defDict.items():
                    for (defName, defObj) in constDict.items():
                        if typeMap[constType].has(defName):
                            raise ScopeDefinitionConflict(("Cannot define defmodule {0} "
                                                          + "because of an import/export conflict caused by the {0} {2}::{1}").format(
                                                self.moduleName,
                                                constType,
                                                defName,
                                                modName
                                        ))
                        typeMap[constType].addDefinition(defObj)
            
            # all right,
            # include the scope in the MM
            self._moduleManager.addScope(self)
            
        except Exception, mainE:
            # i need to cleanup
            # all listeners
            if len(tmp_imports) > 0:
                for modName in tmp_imports.keys():
                    try:
                        otherModDef = self._moduleManager.getScope(modName)
                        otherModDef.functions.cleanupObserver(self)
                        otherModDef.templates.cleanupObserver(self)
                        otherModDef.globalsvars.cleanupObserver(self)
                    except:
                        continue
            
            # and then raise
            raise mainE

        
            
    def notify(self, eventName, *args, **kargs):
        if eventName == TemplatesManager.EVENT_NEW_DEFINITION:
            self._handleEventNewDefinition(self.templates, args[0])
            
        elif eventName == GlobalsManager.EVENT_NEW_DEFINITION:
            self._handleEventNewDefinition(self.globalsvars, args[0])
            
        elif eventName == FunctionsManager.EVENT_NEW_DEFINITION:
            self._handleEventNewDefinition(self.functions, args[0])
            
    def _handleEventNewDefinition(self, manager, definition):
        
        assert isinstance(definition, RestrictedDefinition)
        assert isinstance(manager, RestrictedManager)
        
        # i need to verify the case (1):
        #    module A import ?ALL module B
        #    module B import ?ALL module A
        # in this case if there is a new definition
        # in A, it is forwarded to B
        # the new addition is then re-forwarded to
        # A itself... In this case, i need to ignore
        # the re-forwarded addition
        if definition.moduleName != self.moduleName:
            # i need to verify the case (2):
            #    module A
            #    module B import ?ALL module A
            #    module C import ?ALL module B and A
            if manager.has(definition.name):
                defPresent = manager.getDefinition(definition.name)
                # I already have a definition with the same name
                # so there is a conflict if they are equals
                if defPresent != definition:
                    raise ScopeDefinitionConflict("Cannot define {1} {0} because of an import/export conflict".format(
                                    definition.name,
                                    definition.definitionType
                                ))
                # otherwise it's ok: i already know about this definition
                # just like in case (2)
            
            # this is a new definition
            # i need to add this to my scope
            manager.addDefinition(definition)
            
        # otherwise it's ok:
        # <-> inclusion just like in case (1)
        # nothing to do 
        
            
    @property
    def moduleName(self):
        return self._moduleName
    
    @property
    def modules(self):
        return self._moduleManager
    
    @property
    def templates(self):
        return self._templates
    
#    @templates.setter
#    def templates(self, value):
#        self._templates = value
        
    @property
    def globalsvars(self):
        return self._globals
    
#    @globalsvars.setter
#    def globalsvars(self, value):
#        self._globals = value

    @property
    def functions(self):
        return self._functions


    def isImportable(self, eType, eName):
        return self._exports.canExport(eType, eName)
    
    def getExports(self, eType, eName=None):
        exDefs = self._exports.getExports(eType)
        
        typeMap = {
            Scope.PROMISE_TYPE_TEMPLATE   : self.templates,
            Scope.PROMISE_TYPE_FUNCTION   : self.functions,
            Scope.PROMISE_TYPE_GLOBAL     : self.globalsvars
        }
        
        # check if export all is here!
        if exDefs.has_key(Scope.PROMISE_NAME_ALL):
            # i need to get all definitions i already got
            # and replace the array
            exDefs = dict([(defName, defName) for defName in typeMap[eType].definitions])
        
        if eName is None or eName == Scope.PROMISE_NAME_ALL:
            return [(eName, typeMap[eType].getDefinition(eName)) for eName in exDefs.keys() if eName != Scope.PROMISE_NAME_ALL]
        else:
            # this ensure the export for the name exists
            # otherwise a KeyError is raised
            exDefs[eName]
            return [(eName, typeMap[eType].getDefinition(eName))]
        
    def __str__(self, *args, **kwargs):
        retStr = [super(Scope, self).__repr__(*args, **kwargs)]
        TAB = "\t|"
        retStr.append(TAB + "-moduleName: " + self.moduleName)
        retStr.append(TAB + "-exports: ")
        retStr.append(str(self._exports))
        retStr.append(TAB + "-imports: ")
        for im in self._imports:
            retStr.append(TAB + TAB + "-" + str(im))
        
        iMan = [("functions", self.functions),
                ("globals", self.globalsvars),
                ("templates", self.templates)]
        for (aN, aM) in iMan:
            retStr.append(TAB + "-{0}: ".format(aN))
            for iDef in aM.definitions:
                retStr.append(TAB + TAB + "-{0}::{1}".format(
                        aM.getDefinition(iDef).moduleName, 
                        iDef
                    ))
        return "\n".join(retStr)+"\n"
        
        
        
class _ScopeExportPromise(object):
    
    _typeMap = {
            Scope.PROMISE_TYPE_TEMPLATE   : '_pTemplates',
            Scope.PROMISE_TYPE_FUNCTION   : '_pFunctions',
            Scope.PROMISE_TYPE_GLOBAL     : '_pGlobals'
        }
    
    def __init__(self, exports=None):
        if exports == None:
            exports = []
        
        self._pTemplates = {}
        self._pFunctions = {}
        self._pGlobals = {}
            
        for exDef in exports:
            if not isinstance(exDef, ScopeExport):
                raise ValueError("Export definition must be a ScopeExport instance")
            if exDef.eType == Scope.PROMISE_NAME_ALL:
                self._pTemplates[exDef.eName] = exDef
                self._pFunctions[exDef.eName] = exDef
                self._pGlobals[exDef.eName] = exDef
            elif exDef.eType == Scope.PROMISE_NAME_NONE:
                # name is ignored... all must be flushed
                self._pTemplates = {}
                self._pFunctions = {}
                self._pGlobals = {}
            else:
                if exDef.eName == Scope.PROMISE_NAME_NONE:
                    # empty this promise dict type
                    setattr(self, _ScopeExportPromise._typeMap[exDef.eType], {})
                else:
                    pDict = getattr(self, _ScopeExportPromise._typeMap[exDef.eType])
                    pDict[exDef.eName] = exDef
                    
    def canExport(self, eType, eName):
        pDict = getattr(self, _ScopeExportPromise._typeMap[eType])
        return pDict.has_key(Scope.PROMISE_NAME_ALL) or pDict.has_key(eName)
    
    def getExports(self, eType):
        return getattr(self, _ScopeExportPromise._typeMap[eType])

    def __str__(self):
        TAB = "\t|"
        retStr = []
        for eType in _ScopeExportPromise._typeMap.keys():
            retStr.append(TAB + TAB + "-{0}:".format(eType))
            for exDef in self.getExports(eType).keys():
                retStr.append(TAB + TAB + TAB + "-" + exDef)
        return "\n".join(retStr)

class ScopeImport(object):

    def __init__(self, importModule, importType, importName):
        self._importType = importType
        self._importName = importName
        self._importModule = importModule
    
    @property
    def iModule(self):
        return self._importModule
    
    @property
    def iType(self):
        return self._importType

    @property
    def iName(self):
        return self._importName
    
    def __str__(self, *args, **kwargs):
        return "<ScopeImport: from {0} {1} {2}>".format(self.iModule, self.iType, self.iName)

class ScopeExport(object):
    
    def __init__(self, exportType, exportName):
        self._exportType = exportType
        self._exportName = exportName
    
    @property
    def eType(self):
        return self._exportType

    @property
    def eName(self):
        return self._exportName

class ScopeDefinitionNotFound(ValueError):
    pass

class ScopeDefinitionConflict(Exception):
    pass