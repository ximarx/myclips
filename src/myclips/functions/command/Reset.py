'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function

class Reset(Function):
    '''
    Refresh a rule status in the agenda
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theResets=None, *args, **kargs):
        """
        function handler implementation
        """

        theEnv.network.reset()
        
        return types.NullValue()
    
    
Reset.DEFINITION = FunctionDefinition("?SYSTEM?", "reset", Reset(), types.NullValue, Reset.do ,
            [
                Constraint_ExactArgsLength(0)
            ],forward=False)
        
        