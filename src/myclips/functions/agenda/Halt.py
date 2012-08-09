'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.rete.WME import WME
from myclips.functions.Function import Function, HaltException

class Halt(Function):
    '''
    The halt function may be used on the RHS of a rule to prevent further rule firing.
    It is called without arguments. After halt is called, control is returned from the run command. 
    The agenda is left intact, and execution may be continued with a run command. 
    This function has no return value.
    
    @see http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-13.7.html#Heading451
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, *args, **kargs):
        """
        function handler implementation
        @see http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-13.7.html#Heading451
        """
        
        raise HaltException
            
            
    
Halt.DEFINITION = FunctionDefinition("?SYSTEM?", "halt", Halt(), (types.Lexeme, types.Symbol, types.String, 
                                                                                    types.Number, types.Integer, types.Float,
                                                                                    list, types.NullValue, WME ), 
                                                                Halt.do,
            [
                Constraint_ExactArgsLength(0)
            ],forward=False)
        
        