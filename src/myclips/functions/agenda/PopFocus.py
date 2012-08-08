'''
Created on 07/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, \
    Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function


class PopFocus(Function):
    '''
    The function pop-focus removes the current focus from 
    the focus stack and returns the module name of the current focus. 
    If the focus stack is empty, then the symbol FALSE is returned.
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.12.html#Heading316
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.12.html#Heading316
        """
        
        try:
            return types.Symbol(theEnv.network.agenda.focusStack.pop())
        except IndexError:
            return types.Symbol("FALSE")

        
    
PopFocus.DEFINITION = FunctionDefinition("?SYSTEM?", "pop-focus", PopFocus(), types.Symbol, PopFocus.do,
            [
                Constraint_ExactArgsLength(0)
            ],forward=False)
        
        