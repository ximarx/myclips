'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function
from myclips.listeners.NetworkBuildPrinter import NetworkBuildPrinter

class Watch(Function):
    '''
    Clear network status
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, *args, **kargs):
        """
        function handler implementation
        """

        NetworkBuildPrinter(theEnv.RESOURCES['wtrace']).install(theEnv.network.eventsManager)
        
        return types.NullValue()
    
    
Watch.DEFINITION = FunctionDefinition("?SYSTEM?", "watch", Watch(), types.NullValue, Watch.do ,
            [
                Constraint_ExactArgsLength(0)
            ],forward=False)
        
        