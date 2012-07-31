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
    Assert new fact in the working memory
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, funcEnv, *args, **kargs):
        """
        handler of the Assert function:
            assert new fact in the network working memory
        """
        
        returnValue = types.Symbol("FALSE")
    
        for fact in args:
            
            # revolve variables and function calls
            fact = Function.resolve(funcEnv, fact)
            
            returnValue = funcEnv.network.assertFact(fact)
            
        return returnValue
            
            
    
Assert.DEFINITION = FunctionDefinition("?SYSTEM?", "assert", object(), (WME, types.Symbol), Assert().do ,
            [
                Constraint_MinArgsLength(1),
            ],forward=False)
        
        