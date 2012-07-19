'''
Created on 19/lug/2012

@author: Francesco Capozzo
'''
from myclips.Observer import Observer
from myclips.TemplatesManager import TemplatesManager, TemplateDefinition
from myclips.GlobalsManager import GlobalsManager
from myclips.FunctionsManager import FunctionsManager

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
            except ValueError:
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
                            if iqType == Scope.PROMISE_TYPE_TEMPLATE:
                                otherModDef.templates.registerObserver(TemplatesManager.EVENT_NEW_DEFINITION, self)
                            elif iqType == Scope.PROMISE_TYPE_FUNCTION:
                                otherModDef.functions.registerObserver(FunctionsManager.EVENT_NEW_DEFINITION, self)
                            elif iqType == Scope.PROMISE_TYPE_GLOBAL:
                                otherModDef.globalsvars.registerObserver(GlobalsManager.EVENT_NEW_DEFINITION, self)
                        
            
    def notify(self, eventName, *args, **kargs):
        if eventName == TemplatesManager.EVENT_NEW_DEFINITION:
            self._handleEventNewTemplate(args[0])
            
    def _handleEventNewTemplate(self, definition):
        
        assert isinstance(definition, TemplateDefinition)
        
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
            if self.templates.hasDefinition(definition.templateName):
                defPresent = self.templates.getTemplateDefinition(definition.templateName)
                # I already have a definition with the same name
                # so there is a conflict if they are equals
                if defPresent != definition:
                    raise ScopeDefinitionConflict("Cannot define deftemplate {0} because of an import/export conflict".format(
                                    definition.templateName
                                ))
                # otherwise it's ok: i already know about this definition
                # just like in case (2)
            
            # this is a new definition
            # i need to add this to my scope
            self.templates.registerTemplate(definition)
            
        # otherwise it's ok:
        # reciprocate inclusion just like in case (1) 
        
            
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
        if eName is None or eName == Scope.PROMISE_NAME_ALL:
            if eType == Scope.PROMISE_TYPE_TEMPLATE:
                return [(eName, self.templates.getTemplateDefinition(eName)) for eName in exDefs.keys() if eName != Scope.PROMISE_NAME_ALL]
            elif eType == Scope.PROMISE_TYPE_GLOBAL:
                return [(eName, self.globalsvars.getGlobal(eName)) for eName in exDefs.keys() if eName != Scope.PROMISE_NAME_ALL]
            elif eType == Scope.PROMISE_TYPE_FUNCTION:
                return [(eName, self.functions.getFuncDefinition(eName)) for eName in exDefs.keys() if eName != Scope.PROMISE_NAME_ALL]
            else:
                raise ValueError("Syntax Error: check appropriate syntax for defmodule import specification")
        else:
            # this ensure the export for the name exists
            # otherwise a ValueError is raised
            eName = exDefs[eName].eName
            if eType == Scope.PROMISE_TYPE_TEMPLATE:
                return [(eName, self.templates.getTemplateDefinition(eName))]
            elif eType == Scope.PROMISE_TYPE_GLOBAL:
                return [(eName, self.globalsvars.getGlobal(eName))]
            elif eType == Scope.PROMISE_TYPE_FUNCTION:
                return [(eName, self.functions.getFuncDefinition(eName))]
            else:
                raise ValueError("Syntax Error: check appropriate syntax for defmodule import specification")
        
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