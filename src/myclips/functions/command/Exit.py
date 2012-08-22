'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function
import sys

class Exit(Function):
    '''
    Shutdown MyCLIPS
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, *args, **kargs):
        """
        function handler implementation
        """

        sys.exit()
        
    
    
Exit.DEFINITION = FunctionDefinition("?SYSTEM?", "exit", Exit(), types.NullValue, Exit.do ,
            [
                Constraint_ExactArgsLength(0)
            ],forward=False)
        
        