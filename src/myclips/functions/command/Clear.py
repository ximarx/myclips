'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function

class Clear(Function):
    '''
    Clear network status
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, *args, **kargs):
        """
        function handler implementation
        """

        theEnv.network.clear()
        
        return types.NullValue()
    
    
Clear.DEFINITION = FunctionDefinition("?SYSTEM?", "clear", Clear(), types.NullValue, Clear.do ,
            [
                Constraint_ExactArgsLength(0)
            ],forward=False)
        
        