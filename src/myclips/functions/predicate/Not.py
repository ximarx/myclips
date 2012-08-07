'''
Created on 05/aug/2012

@author: Francesco Capozzo
'''
import myclips.parser.Types as types
from myclips.functions.Function import Function
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType, Constraint_ExactArgsLength

class Not(Function):
    '''
    The not function returns the symbol TRUE if its argument evaluates to FALSE, 
    otherwise it returns the symbol FALSE.
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.1.html#Heading216
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
    def do(self, theEnv, theExpression, *args, **kargs):
        """
        handler of the function
        """
        
        # comparison is done against the <Symbol:FALSE>
        theValue = types.Symbol("FALSE")

        # resolve the real value
        # before comparison
        if isinstance(theExpression, (types.FunctionCall, types.Variable)):
            theArg = self.resolve(theEnv, theExpression)
        # types + value comparison
        if theValue == theArg:
            return types.Symbol("TRUE") # return <Symbol:TRUE>
        else:
            return theValue


Not.DEFINITION = FunctionDefinition("?SYSTEM?", "not", Not(), types.Symbol, Not.do ,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType(types.Symbol, 0)
            ],forward=False)
