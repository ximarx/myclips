'''
Created on 08/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_ExactArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.rete.WME import WME
from myclips.functions.Function import Function

class FactIndex(Function):
    '''
    The factindex function returns the fact- index (an integer) of a fact-address.
    
    WARNING: MyClips's version of fact-address is a WME instance 
    
    @see http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.9.html#Heading306
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theWme, *args, **kargs):
        """
        Function handler implementation
        
        @see http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.9.html#Heading306
        """
        
        theWme = Function.semplify(theEnv, theWme, WME, ("1", "fact-address"))
        
        return types.Integer(theWme.factId)
            
    
            
    
FactIndex.DEFINITION = FunctionDefinition("?SYSTEM?", "fact-index", FactIndex(), (WME, types.Integer), FactIndex.do ,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType(WME, 0)
            ],forward=False)
        
        