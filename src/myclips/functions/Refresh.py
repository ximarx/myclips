'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_ArgType, Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.rete.WME import WME
from myclips.functions.Function import Function

class Refresh(Function):
    '''
    Assert new fact in the working memory
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, funcEnv, ruleName, *args, **kargs):
        """
        handler of the Assert function:
            assert new fact in the network working memory
        """
        
        ruleName = Function.resolve(funcEnv, ruleName)
        
        # resolve the main PNode
        
        # ruleName is automatically converted to CURRENTSCOPE::RULENAME
        # if ruleName is not already a complete rule name
        thePNode = funcEnv.network.getPNode(ruleName)
        # RuleNotFoundError could be raised... but it will flow outside of the network
        # and it's ok!
        
        # now i have to refresh the main rule and all linked
        # slave-rules to the main one (if any)
        funcEnv.network.agenda.refresh(thePNode.completeMainRuleName())
        
        for slavePNode in thePNode.getLinkedPNodes():
            # use the completeRuleName method, not the completeMainRuleName one
            funcEnv.network.agenda.refresh(slavePNode.completeRuleName())
            
        return None
    
    
Refresh.DEFINITION = FunctionDefinition("?SYSTEM?", "refresh", object(), types.NullValue, Refresh().do ,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType(types.Symbol, 0),
            ],forward=False)
        
        