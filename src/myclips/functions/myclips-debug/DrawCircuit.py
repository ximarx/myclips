'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_ArgType, Constraint_MinArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgValueError
from myclips.rete.Network import RuleNotFoundError

class DrawCircuit(Function):
    '''
    Refresh a rule status in the agenda
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, *args, **kargs):
        """
        function handler implementation
        """
        try:
            _thePNodes = [theEnv.network.getPNode(ruleName) 
                            for ruleName 
                                in [self.resolve(theEnv, self.semplify(theEnv, ruleName, types.Symbol, ("ALL", "symbol"))) for ruleName in args]]
        except RuleNotFoundError, e:
            
            raise InvalidArgValueError(e.message)
            
        else:
            # RuleNotFoundError could be raised... but it will flow outside of the network
            # and it's ok!
    
            thePNodes = []
    
            for thePNode in _thePNodes:
                from myclips.rete.nodes.PNode import PNode
                assert isinstance(thePNode, PNode)
                thePNodes += [thePNode] + thePNode.getLinkedPNodes()
                
            import myclips.debug as debug
            
            debug.draw_network_fragment(thePNodes)
            
            return types.NullValue()
    
    
DrawCircuit.DEFINITION = FunctionDefinition("?SYSTEM?", "draw-circuit", DrawCircuit(), types.NullValue, DrawCircuit.do ,
            [
                Constraint_MinArgsLength(1),
                Constraint_ArgType(types.Symbol),
            ],forward=False)
        
        