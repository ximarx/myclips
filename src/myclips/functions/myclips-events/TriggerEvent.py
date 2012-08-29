'''
Created on 25/ago/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_ArgType, Constraint_MinArgsLength, \
    Constraint_MaxArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgValueError
from myclips.rete.Network import RuleNotFoundError
import time

class TriggerEvent(Function):
    '''
    Execute a benchmark over a run-call
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theEvent, *args, **kargs):
        """
        function handler implementation
        """
        
        theEvent = self.resolve(theEnv, 
                                self.semplify(theEnv, theEvent, types.Symbol, ("1", "symbol")))
        
        args = self.semplify(theEnv, list(args))
        
        theEnv.network.eventsManager.fire(theEvent, *args)
        
        return types.Symbol("TRUE")
    
    
TriggerEvent.DEFINITION = FunctionDefinition("?SYSTEM?", "trigger-event", TriggerEvent(), types.Symbol, TriggerEvent.do,
            [
                Constraint_MinArgsLength(1),
                Constraint_ArgType(types.Symbol, 0)
             ],forward=False)
                