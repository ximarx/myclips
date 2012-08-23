'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_ArgType, Constraint_MinArgsLength, Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function
from myclips.rete.WME import WME

class TraceScope(Function):
    '''
    Show debug information about a scope (a module)
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theModule, *args, **kargs):
        """
        function handler implementation
        """

        theModule = self.resolve(theEnv, 
                                 self.semplify(theEnv, theModule, types.Symbol, ("1", "symbol")))
            
        
        theEnv.RESOURCES['wtrace'].write(str(theEnv.modulesManager.getScope(theModule)) + "\n")
        
        return types.NullValue()
    
    
TraceScope.DEFINITION = FunctionDefinition("?SYSTEM?", "trace-scope", TraceScope(), types.NullValue, TraceScope.do ,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType(types.Symbol, 0),
            ],forward=False)
        
        