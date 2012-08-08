'''
Created on 07/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, \
    Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function


class GetFocus(Function):
    '''
    The function get-focus returns the module name of the current focus. 
    If the focus stack is empty, then the symbol FALSE is returned.
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.12.html#Heading314
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.12.html#Heading314
        """
        
        try:
            # get the top of the stack, without pop
            return types.Symbol(theEnv.network.agenda.focusStack[-1])
        except IndexError:
            return types.Symbol("FALSE")

        
    
GetFocus.DEFINITION = FunctionDefinition("?SYSTEM?", "get-focus", GetFocus(), types.Symbol, GetFocus.do,
            [
                Constraint_ExactArgsLength(0)
            ],forward=False)
        
        