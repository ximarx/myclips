'''
Created on 05/aug/2012

@author: Francesco Capozzo
'''
import myclips.parser.Types as types
from myclips.functions.Function import Function
from myclips.FunctionsManager import FunctionDefinition, Constraint_MinArgsLength,\
    Constraint_ArgType

class Or(Function):
    '''
    TThe or function returns the symbol TRUE if any of its arguments evaluates to TRUE, 
    otherwise it returns the symbol FALSE. 
    The or function performs short- circuited boolean logic. 
    Each argument of the function is evaluated from left to right. 
    If any argument evaluates to TRUE, then the symbol TRUE is immediately returned by the function.
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.1.html#Heading215
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
    def do(self, theEnv, *args, **kargs):
        """
        handler of the function
        """
        
        # comparison is done against the <Symbol:TRUE>
        theValue = types.Symbol("TRUE")

        for theArg in args:
            # resolve the real value
            # before comparison
            if isinstance(theArg, (types.FunctionCall, types.Variable)):
                theArg = self.resolve(theEnv, theArg)
            # types + value comparison
            if theValue == theArg:
                return theValue # return <Symbol:TRUE>
            
        return types.Symbol("FALSE")


Or.DEFINITION = FunctionDefinition("?SYSTEM?", "or", Or(), types.Symbol, Or.do ,
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(types.Symbol)
            ],forward=False)
