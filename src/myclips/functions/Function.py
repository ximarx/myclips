'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.MyClipsException import MyClipsException
import myclips.parser.Types as types
import traceback

        
class Function(object):
    '''
    Base abstract class for system function definition
    '''
    
    # @type DEFINITION: myclips.FunctionsManager.FunctionDefinition.FunctionDefinition
    DEFINITION = None
    
    def __init__(self, *args, **kwargs):
        object.__init__(self, *args, **kwargs)

    @classmethod
    def execute(cls, theEnv, *args, **kargs):
        """
        Execute a function handler with correct parameters
        
        @raise FunctionImplError: forward exception from function handler implementation
        @raise FunctionInternalError: wrap a non FunctionImplError exception in a FunctionInternalError
                to hide function internal processing. Original exception is available in 
                FunctionInternalError.args[1]. Original exception repr() is used as
                wrapper exception's message
        @return: forward handler return
        @rtype: mixed (based on FunctionDefinition.returnTypes)
        """
        try:
            return cls.DEFINITION.handler(cls.DEFINITION.linkedType, theEnv, *args, **kargs)
        except FunctionImplError:
            raise
        except MyClipsException, e:
            raise FunctionInternalError(str(cls)+": "+e.message, e, traceback.format_exc())
        except Exception, e:
            # wrap python standards exception
            # in functions exception
            raise FunctionInternalError(str(e), e, traceback.format_exc())
        
    def definition(self):
        """
        Get the system function FunctionDefinition
        """
        return self.__class__.DEFINITION
    
    @classmethod
    def resolve(cls, theEnv, arg):
        # String is a special value, have to trim out quotes
        if isinstance(arg, types.String):
            return arg.content[1:-1]
        elif isinstance(arg, types.BaseParsedType):
            return arg.evaluate()
        elif isinstance(arg, types.FunctionCall):
            # indirect recursion on execute with
            return arg.funcDefinition.linkedType.__class__.execute(theEnv, *(arg.funcArgs))
        elif isinstance(arg, (types.SingleFieldVariable, types.MultiFieldVariable )):
            # resolve the variable value vs theEnv.variables dict
            return theEnv.variables[arg.evaluate()]
        elif isinstance(arg, types.GlobalVariable):
            # resolve the variable value vs theEnv.globals
            return theEnv.modulesManager.currentScope.globalsvars.getDefinition(arg.evaluate()).linkedType.runningValue


class FunctionImplError(MyClipsException):
    pass

class InvalidArgValueError(FunctionImplError):
    pass

class InvalidArgTypeError(FunctionImplError):
    pass

class InvalidArgsNumberError(FunctionImplError):
    pass

class FunctionInternalError(FunctionImplError):
    pass

