'''
Created on 06/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType, \
    Constraint_MaxArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgTypeError


class Close(Function):
    '''
    The close function closes a file stream previously opened with the open command. 
    The file is specified by a logical name previously attached to the desired stream.
    If close is called without arguments, all open files will be closed        
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.4.html#Heading245
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theName=None, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.4.html#Heading245
        """
        
        theName = self.resolve(theEnv, theName) if isinstance(theName, (types.FunctionCall, types.Variable)) else theName 
        
        if theName is None:
            toClose = theEnv.RESOURCES.keys()
        elif not isinstance(theName, types.Symbol):
                raise InvalidArgTypeError("Function open expected argument #1 to be of type symbol")
        else:
            toClose = [theName.evaluate()]
            
        try:
            for resourceName in toClose:
                theEnv.RESOURCES[resourceName].close()
                del theEnv.RESOURCES[resourceName]
            return types.Symbol("TRUE")
        except KeyError:
            return types.Symbol("FALSE")
            
    
Close.DEFINITION = FunctionDefinition("?SYSTEM?", "close", Close(), types.Symbol, Close.do,
            [
                Constraint_MaxArgsLength(1),
                Constraint_ArgType(types.Symbol, 0, failIfMissing=False)
            ],forward=False)
        
        