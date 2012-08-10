'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, \
    Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function


class GetStrategy(Function):
    '''
    This function returns the current conflict resolution strategy 
    (depth, breadth, simplicity, complexity, lex, mea, or random).
    
    (getstrategy)

    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-13.7.html#Heading453
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-13.7.html#Heading453
        """
        
        
        return types.Symbol(theEnv.network.agenda.strategy)

        
    
GetStrategy.DEFINITION = FunctionDefinition("?SYSTEM?", "get-strategy", GetStrategy(), types.Symbol, GetStrategy.do,
            [
                Constraint_ExactArgsLength(0)
            ],forward=False)
        
        