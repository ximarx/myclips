'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import Constraint_ArgType,\
    Constraint_MaxArgsLength, FunctionDefinition
import myclips.parser.Types as types
from myclips.functions.Function import Function

class Run(Function):
    '''
    Refresh a rule status in the agenda
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theRuns=None, *args, **kargs):
        """
        function handler implementation
        """

        if theRuns is not None:
            theRuns = self.resolve(theEnv, self.semplify(theEnv, theRuns, types.Integer, ("1", "integer")))
            
        theEnv.network.run(theRuns)
        
        return types.NullValue()
    
    
Run.DEFINITION = FunctionDefinition("?SYSTEM?", "run", Run(), types.NullValue, Run.do ,
            [
                Constraint_MaxArgsLength(1),
                Constraint_ArgType(types.Integer, 0, False),
            ],forward=False)
        
        