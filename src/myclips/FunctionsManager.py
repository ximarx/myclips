'''
Created on 17/lug/2012

@author: Francesco Capozzo
'''
from myclips.Observable import Observable
from myclips.RestrictedManager import RestrictedManager, RestrictedDefinition,\
    MultipleDefinitionError
import myclips


class FunctionsManager(RestrictedManager, Observable):
    '''
    Stores the list of allowed functions definitions for the scope
    '''
    instance = None
    EVENT_NEW_DEFINITION = "EVENT_FunctionsManager_NewDefinition"
    """Event sign used when new definition is added, observer will
    be notified with this sign!"""

    def __init__(self, scope):
        '''
        Create a new FunctionsManager for the scope

        @param scope: the scope owner of this manager
        @type scope: L{Scope}
        '''
        Observable.__init__(self, [
                FunctionsManager.EVENT_NEW_DEFINITION
            ])
        RestrictedManager.__init__(self, scope)
        
        # need to import system function definitions
        # bypass registerSystemFunction to avoid debug logger
        self._systemsFunctions = Functions_ImportSystemDefinitions()
        '''definitions of system-functions'''
        
        
    @property
    def systemFunctions(self):
        '''
        Get the list of sys functions signs
        @rtype: list
        '''
        return self._systemsFunctions.keys()
    
    def getSystemFunctionDefinition(self, funcName):
        '''
        Get a sys definition for a function name 
        @param funcName: function name
        @type funcName: string
        @rtype: L{FunctionDefinition}
        '''
        return self._systemsFunctions[funcName] 
        
    def hasSystemFunction(self, funcName):
        '''
        Check if a system function with sign funcName
        is defined
        @param funcName: sign of funcname
        @type funcName: string
        @rtype: boolean
        '''
        return self._systemsFunctions.has_key(funcName)

    def has(self, definitionName):
        '''
        Check if a definition name is used in the this manager
        (search into user-functions and sys-functions)
        
        definitionName will be set as taken if:
            - sys-function exists with same sign
            - a user-function already used with the same sign exists
            
        definitionName will be set as available if:
            - no sys-function or user-function use the same sign
            - a user-function already used the sign, BUT it could
                be redefined (only if not used yet: FunctionDefinition.isForward = True)
        
        @param definitionName: the function name
        @type definitionName: string
        @rtype: boolean
        '''
        return ((self.hasSystemFunction(definitionName) or RestrictedManager.has(self, definitionName))
                    and not self.getDefinition(definitionName).isForward)
    
    def addDefinition(self, definition):
        '''
        Add a new definition and notify observers about this
        @param definition: a new function definition
        @type definition: L{FunctionDefinition}
        '''
        # need to check definition:
        # if definition scope different from this one
        # i need to mark the function as not forward
        # and lock redefinition
        if definition.moduleName != self.scope.moduleName and definition.isForward:
            definition.isForward = False
            myclips.logger.debug("DefFunction %s::%s imported. Can't be redefined", definition.moduleName, definition.name)
             
        RestrictedManager.addDefinition(self, definition)
        
        # after i added the definition, i need to fire the event
        self.fire(self.__class__.EVENT_NEW_DEFINITION, definition)
        
    
    def getDefinition(self, defName):
        '''
        Get a definition (sys or user one) for defName
        @param defName: a function sign
        @type defName: string
        @rtype: FunctionDefinition
        '''
        try:
            return self.getSystemFunctionDefinition(defName)
        except:
            return RestrictedManager.getDefinition(self, defName)
    
    def registerSystemFunction(self, definition):
        '''
        Manually register a new system-function definition
        @param definition: a definition
        @type definition: FunctionDefinition
        @raise MultipleDefinitionError: a previous sys-func definition
            with the same sign exists
        '''
        if self.hasSystemFunction(definition.name):
            raise MultipleDefinitionError("Cannot redefine {0} {2}::{1} while it is in use".format(
                        definition.definitionType,
                        definition.name,
                        "?SYSTEM?"
                    ))
        self._systemsFunctions[definition.name] = definition
        myclips.logger.debug("System function %s registered", definition.name)
            
        
class FunctionDefinition(RestrictedDefinition):
    '''
    Describe a Function Definition
    '''
    def __init__(self, moduleName, defName, linkedType, returnTypes, handler=None, constraints=None, forward=True):
        '''
        Create a new FunctionDefinition instance
        
        @param moduleName: definition owner module's name 
        @type moduleName: string
        @param defName: function sign
        @type defName: string
        @param linkedType: an implementation object instance
        @type linkedType: L{Function}
        @param returnTypes: a tuple of return types classes
        @type returnTypes: tuple
        @param handler: method called on function called execution
        @type handler: method
        @param constraints: a list of function sign constraints
        @type constraints: list of L{FunctionConstraint}
        @param forward: definition could be redefined?
        @type forward: boolean
        '''
        RestrictedDefinition.__init__(self, moduleName, defName, "deffunction", linkedType)
        self._handler = handler
        '''method called on function execution'''
        self._returnTypes = returnTypes if isinstance(returnTypes, tuple) else (returnTypes,)
        '''tuple of return types'''
        self._constraints = constraints if isinstance(constraints, list) else []
        '''function call params constraints'''
        self._forward = bool(forward)
        '''flag: function could be redefined?'''
        
    @property
    def handler(self):
        '''
        Get the callable handler that realize
        the real implementation of the function
        '''
        return self._handler
    
    @property
    def returnTypes(self):
        '''
        Return a tuple of all return types the function
        can use as output
        @rtype: tuple
        '''
        return self._returnTypes
    
    @property
    def isForward(self):
        '''
        Check if definition could be redefined
        '''
        return self._forward
    
    @isForward.setter
    def isForward(self, value):
        '''
        Change redefinition flag
        @param value: new status
        @type value: boolean
        '''
        self._forward = value
    
    def isValidCall(self, args):
        '''
        Check if function call arguments are valid
        againts function sign constraints
        @param args: a list of args
        @type args: list
        @rtype: boolean
        @return: true if all constraints are valid, false otherwise
        '''
        for c in self._constraints:
            # stop validation on first invalid
            if not c.isValid(args):
                return (False, c.getReason())
            
        return self.customValidation(args)
    
    def customValidation(self, args):
        '''
        Override this method to execute custom validations
        on inputs that can't be done with constraints
        This validation is performed as last (after all constraints check)
        if all constraints are ok
        
        @param args: a list/tuple of args
        @type args: list
        @return: a tuple (True|False, None|str:Reason of failure)
        @rtype: tuple
        '''
        return (True, None)
    
class FunctionConstraint(object):
    '''
    Abstract, base, function constraint 
    '''
    def getReason(self):
        '''
        Get the reason (string) why the constraint
        could have failed
        '''
        return ""
    def isValid(self, args):
        '''
        Check if args are valid for this constraint
        @param args: list of args
        @type args: list
        @rtype: boolean
        '''
        return True
    
class Constraint_MinArgsLength(FunctionConstraint):
    '''
    Add a min args length constraint
    '''
    def __init__(self, value):
        '''
        Set the minimum number of args expected
        @param value: the min length of args 
        @type value: integer
        '''
        self.value = value
        '''min length'''
        
    def getReason(self):
        return "expected at least {0} argument(s)".format(self.value)
    
    def isValid(self, args):
        return (len(args) >= self.value)

class Constraint_MaxArgsLength(FunctionConstraint):
    '''
    Add a max args length constraint
    '''
    def __init__(self, value):
        '''
        Create the constaint, setting the max length
        of args
        @param value: the max length
        @type value: integer
        '''
        self.value = value
        '''max lenght'''
    
    def getReason(self):
        return "expected no more than {0} argument(s)".format(self.value)
    
    def isValid(self, args):
        return (len(args) <= self.value)

class Constraint_ExactArgsLength(FunctionConstraint):
    '''
    Add a exact length constraint
    '''
    def __init__(self, value):
        '''
        Create the constraint, setting the exact length
        @param value: the length
        @type value: integer
        '''
        self.value = value
        '''the length'''

    def getReason(self):
        return "expected exactly {0} argument(s)".format(self.value)
    
    def isValid(self, args):
        return (len(args) == self.value)
    
class Constraint_ArgType(FunctionConstraint):
    '''
    Set a type constraint about a single or a group of args
    '''
    def __init__(self, argType, argIndex=None, failIfMissing=True):
        '''
        Create the constraint, setting validity params
        @param argType: a tuple of valid types for a/some params
        @type argType: tuple of types
        @param argIndex: the arg index or a tuple of bound to
            set a subgroup of all args.
            Use N for a single item
            Use (None,None) or None for a "for-all" constaint
            Use (N, None) for a "from N to the end" constraint
            Use (N, -M) for a "from N to the K, where K has M args after" constraint
            0 is a valid value for N :)
        @type argIndex: integer|tuple|None
        @param failIfMissing: the constraint should fail if the arg doesn't exists at all?
        @type failIfMissing: boolean
        '''
        self.argType = argType
        '''the tuple of valid types'''
        self.argIndex = argIndex
        '''the index or the bound of index'''
        self.argRequired = failIfMissing
        '''the constraint should fail if arg misses'''

    def getReason(self):
        return "expected argument {0} to be of type {1}".format("#"+str(self.argIndex + 1) if self.argIndex is not None else "#ALL",
                                                                " or ".join([t.__name__ for t in self.argType])
                                                                    if isinstance(self.argType, tuple) 
                                                                    else self.argType.__name__
                                                                )
        
    def isValid(self, args):
        import myclips.parser.Types as types
        try:
            if self.argIndex == None or isinstance(self.argIndex, tuple):
                argSlice = args
                if isinstance(self.argIndex, tuple):
                    argSlice = args[self.argIndex[0]:self.argIndex[1]]
                invalidArgs = [True if isinstance(x, self.argType)
                                    else True if isinstance(x, types.Variable)
                                        else True if isinstance(x, types.FunctionCall)
                                                        and self.argType in x.funcDefinition.returnTypes
                                            else True if isinstance(x, types.FunctionCall)
                                                            and any([issubclass(retType, self.argType) for retType in x.funcDefinition.returnTypes])
                                                else False
                               for x in argSlice]
                return (not any([not x for x in invalidArgs]))
            else:
                x = args[self.argIndex]
                return (True if isinstance(x, self.argType)
                                    else True if isinstance(x, types.Variable)
                                        else True if isinstance(x, types.FunctionCall)
                                                        and self.argType in x.funcDefinition.returnTypes
                                            else True if isinstance(x, types.FunctionCall)
                                                            and any([issubclass(retType, self.argType) for retType in x.funcDefinition.returnTypes])
                                                else False)
        except (KeyError, IndexError):
            if self.argRequired:
                return False
            else:
                return True

    
def Functions_ImportSystemDefinitions():
    '''
    Facade: get a list of system functions 
    definition from the myclips.functions.SystemFunctionBroker
    @rtype: list of definition
    '''
    
    from myclips.functions import SystemFunctionBroker
    
    return SystemFunctionBroker.definitions()
