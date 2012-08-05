
'''
Created on 05/ago/2012

@author: Francesco Capozzo
'''
from myclips.functions.predicate._TypeTesting import _TypeTesting
import myclips.parser.Types as types
from myclips.FunctionsManager import Constraint_ExactArgsLength,    FunctionDefinition

class Integerp(_TypeTesting):
    '''
    The integerp function returns the symbol TRUE if its argument is a Integer, otherwise it returns the symbol FALSE.
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.1.html#Heading188
    '''
    pass
        
        
Integerp.DEFINITION = FunctionDefinition("?SYSTEM?", "integerp", Integerp(types.Integer), types.Symbol, Integerp.do ,
            [
                Constraint_ExactArgsLength(1)
            ],forward=False)
