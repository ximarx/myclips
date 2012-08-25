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

class BenchRun(Function):
    '''
    Execute a benchmark over a run-call
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theRuns=None, *args, **kargs):
        """
        function handler implementation
        """
        
        if theRuns is not None:
            theRuns = self.resolve(theEnv, self.semplify(theEnv, theRuns, types.Integer, ("1", "integer")))
            
        start_time = time.time()
        theEnv.network.run(theRuns)
        runTime = time.time() - start_time
        
        return types.Float(runTime)
    
    
BenchRun.DEFINITION = FunctionDefinition("?SYSTEM?", "bench-run", BenchRun(), types.Float, BenchRun.do ,
            [
                Constraint_MaxArgsLength(1),
                Constraint_ArgType(types.Integer, 0, False),
            ],forward=False)
                