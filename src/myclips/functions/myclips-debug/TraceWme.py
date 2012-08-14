'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_ArgType, Constraint_MinArgsLength, Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function
from myclips.rete.WME import WME

class TraceWme(Function):
    '''
    Refresh a rule status in the agenda
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theWme, *args, **kargs):
        """
        function handler implementation
        """

        theWme = self.resolveWme(theEnv, self.semplify(theEnv, theWme, (WME, types.Integer), ("1", "fact-address or i")))
            
        import myclips.debug as debug
        
        debug.show_wme_details(theEnv.RESOURCES['wtrace'], theWme, explodeToken=True, explodeAMem=True)
        
        return types.NullValue()
    
    def resolveWme(self, theEnv, arg):
        if isinstance(arg, types.Integer):
            return theEnv.network.getWmeFromId(self.resolve(theEnv, arg))
        elif isinstance(arg, WME):
            return arg
    
    
TraceWme.DEFINITION = FunctionDefinition("?SYSTEM?", "trace-wme", TraceWme(), types.NullValue, TraceWme.do ,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType((types.Integer, WME), 0),
            ],forward=False)
        
        