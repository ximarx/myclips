'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, BreakException

class Break(Function):
    '''
    Break function:
        The break function immediately terminates the currently iterating while/loop-for-count loop
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading286
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, *args, **kargs):
        """
        handler of the Break function:
            raise BreakException
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading286
        """
        # CLIPS documentation:
        # return_stmt ::= ( break )
        
        raise BreakException()
            
            
    
Break.DEFINITION = FunctionDefinition("?SYSTEM?", "break", Break(), (types.NullValue ), 
                                                                Break.do,
            [
                Constraint_ExactArgsLength(0)
            ],forward=False)
        
        