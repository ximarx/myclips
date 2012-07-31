'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength
import myclips.parser.Types as types
from myclips.rete.WME import WME
from myclips.functions.Function import Function

class Assert(Function):
    '''
    classdocs
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def doAssert(self, funcEnv, *args, **kargs):
        
        returnValue = types.Symbol("FALSE")
    
        for fact in args:
            
            # revolve variables and function calls
            fact = Function.resolve(funcEnv, fact)
            
            returnValue = funcEnv.network.assertFact(fact)
            
        return returnValue
            
            
    
Assert.DEFINITION = FunctionDefinition("?SYSTEM?", "assert", object(), (WME, types.Symbol), Assert().doAssert ,
            [
                Constraint_MinArgsLength(1),
            ],forward=False)
        
        