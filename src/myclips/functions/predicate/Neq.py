'''
Created on 05/aug/2012

@author: Francesco Capozzo
'''
import myclips.parser.Types as types
from myclips.functions.Function import Function
from myclips.FunctionsManager import FunctionDefinition, Constraint_MinArgsLength

class Neq(Function):
    '''
    The neq function returns the symbol TRUE if its first argument is not equal in value to all its subsequent arguments, 
    otherwise it returns the symbol FALSE. 
    Note that neq compares types as well as values. Thus, (neq 3 3.0) is TRUE since 3 is an integer and 3.0 is a float.
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.1.html#Heading208 
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
    def do(self, theEnv, theValue, *args, **kargs):
        """
        handler of the Neq function
        """
        
        # check theValue type and resolve (if needed)
        if isinstance(theValue, (types.FunctionCall, types.Variable)):
            theValue = self.resolve(theEnv, theValue)

        for theArg in args:
            # resolve the real value
            # before comparison
            if isinstance(theArg, (types.FunctionCall, types.Variable)):
                theArg = self.resolve(theEnv, theArg)
            # != and == operators for BaseParsedType are overrided for 
            # types + value comparisong
            if theValue == theArg:
                return types.Symbol("FALSE")
            
        return types.Symbol("TRUE")


Neq.DEFINITION = FunctionDefinition("?SYSTEM?", "neq", Neq(), types.Symbol, Neq.do ,
            [
                Constraint_MinArgsLength(2),
            ],forward=False)
