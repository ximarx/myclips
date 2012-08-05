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
        #except ReturnException, e:
            # convert a returnException to a return value of the function
            #return e.returnValue
        except (ReturnException, BreakException):
            # break the execution until a catch get it
            raise
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
    """
    The base error class for exception raised
    inside function implementation code
    """
    pass

class ReturnException(MyClipsException):
    """
    Exception used by the Return function
    to return a value from an inner function/loop
    stopping function execution flow
    """
    def __init__(self, returnValue=None, message="", *args, **kwargs):
        MyClipsException.__init__(self, message=message, *args, **kwargs)
        self.returnValue = returnValue

class BreakException(MyClipsException):
    """
    Break a loop execution flow and return
    control to a parent function
    """
    pass

class InvalidArgValueError(FunctionImplError):
    """
    An invalid value for a function argument
    """
    pass

class InvalidArgTypeError(FunctionImplError):
    """
    An invalid type for a function argment
    """
    pass

class InvalidArgsNumberError(FunctionImplError):
    """
    The number of args for a function is invalid
    """
    pass

class FunctionInternalError(FunctionImplError):
    """
    A generic, implementation based exception
    (usually to wrap python-based exception)
    """
    pass

