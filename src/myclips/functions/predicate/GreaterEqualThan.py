'''
Created on 05/aug/2012

@author: Francesco Capozzo
'''
import myclips.parser.Types as types
from myclips.functions.Function import Function
from myclips.FunctionsManager import FunctionDefinition, Constraint_MinArgsLength,\
    Constraint_ArgType

class GreaterEqualThan(Function):
    '''
    The >= function returns the symbol TRUE if for all its arguments, argument n- 1 is greater than or equal to argument n, 
    otherwise it returns the symbol FALSE. 
    Note that >= compares only numeric values and will convert integers to floats when necessary for comparison.
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.1.html#Heading211
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
    def do(self, theEnv, theValue, *args, **kargs):
        """
        handler of the GreaterThan function
        """
        
        # check theValue type and resolve (if needed)
        if isinstance(theValue, (types.FunctionCall, types.Variable)):
            theValue = self.resolve(theEnv, theValue)

        for theArg in args:
            # resolve the real value
            # before comparison
            if isinstance(theArg, (types.FunctionCall, types.Variable)):
                theArg = self.resolve(theEnv, theArg)
            # compare the python type (so 3. == 3)
            if theValue.evaluate() < theArg.evaluate():
                return types.Symbol("FALSE")
            
        return types.Symbol("TRUE")


GreaterEqualThan.DEFINITION = FunctionDefinition("?SYSTEM?", ">=", GreaterEqualThan(), types.Symbol, GreaterEqualThan.do ,
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(types.Number)
            ],forward=False)
