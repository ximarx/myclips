
'''
Created on 05/ago/2012

@author: Francesco Capozzo
'''
from myclips.functions.predicate._TypeTesting import _TypeTesting
import myclips.parser.Types as types
from myclips.FunctionsManager import Constraint_ExactArgsLength,    FunctionDefinition

class Multifieldp(_TypeTesting):
    '''
    The multifieldp function returns the symbol TRUE if its argument is a list, otherwise it returns the symbol FALSE.
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.1.html#Heading204
    '''
        
        
Multifieldp.DEFINITION = FunctionDefinition("?SYSTEM?", "multifieldp", Multifieldp(list), types.Symbol, Multifieldp.do ,
            [
                Constraint_ExactArgsLength(1)
            ],forward=False)
