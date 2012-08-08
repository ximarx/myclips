'''
Created on 07/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, \
    Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function


class GetFocusStack(Function):
    '''
    The function get-focus-stack returns all of the module names 
    in the focus stack as a multifield value. 
    A multifield value of length zero is returned if the focus stack is empty.
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.12.html#Heading315
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.12.html#Heading315
        """
        
        try:
            return [types.Symbol(x) for x in theEnv.network.agenda.focusStack]
        except IndexError:
            return types.Symbol("FALSE")

        
    
GetFocusStack.DEFINITION = FunctionDefinition("?SYSTEM?", "get-focus-stack", GetFocusStack(), list, GetFocusStack.do,
            [
                Constraint_ExactArgsLength(0)
            ],forward=False)
        
        