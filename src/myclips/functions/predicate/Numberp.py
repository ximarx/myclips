
'''
Created on 05/ago/2012

@author: Francesco Capozzo
'''
from myclips.functions.predicate._TypeTesting import _TypeTesting
import myclips.parser.Types as types
from myclips.FunctionsManager import Constraint_ExactArgsLength,    FunctionDefinition

class Numberp(_TypeTesting):
    '''
    The numberp function returns the symbol TRUE if its argument is a Number, otherwise it returns the symbol FALSE.
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.1.html#Heading186
    '''
    pass
        
        
Numberp.DEFINITION = FunctionDefinition("?SYSTEM?", "numberp", Numberp(types.Number), types.Symbol, Numberp.do ,
            [
                Constraint_ExactArgsLength(1)
            ],forward=False)
