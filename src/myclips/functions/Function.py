'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.MyClipsException import MyClipsException

        
class Function(object):
    '''
    Base abstract class for system function definition
    '''
    
    # @type DEFINITION: myclips.FunctionsManager.FunctionDefinition.FunctionDefinition
    DEFINITION = None
    
    def __init__(self, *args, **kwargs):
        object.__init__(self, *args, **kwargs)

    @classmethod
    def execute(cls, functionEnv, *args, **kargs):
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
            return cls.DEFINITION.handler(functionEnv, *args, **kargs)
        except FunctionImplError:
            raise
        except Exception, e:
            # wrap python standards exception
            # in functions exception
            raise FunctionInternalError(repr(e), e)
        
    def definition(self):
        """
        Get the system function FunctionDefinition
        """
        return self.__class__.DEFINITION
    
    @classmethod
    def resolve(cls, funcEnv, arg):
        return arg


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

