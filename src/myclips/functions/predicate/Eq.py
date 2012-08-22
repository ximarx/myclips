'''
Created on 05/aug/2012

@author: Francesco Capozzo
'''
import myclips.parser.Types as types
from myclips.functions.Function import Function
from myclips.FunctionsManager import FunctionDefinition, Constraint_MinArgsLength

class Eq(Function):
    '''
    The eq function returns the symbol TRUE if its first argument is equal in value to all its subsequent arguments, 
    otherwise it returns the symbol FALSE. 
    Note that eq compares types as well as values. Thus, (eq 3 3.0) is FALSE since 3 is an integer and 3.0 is a float.
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.1.html#Heading206 
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
    def do(self, theEnv, theValue, *args, **kargs):
        """
        handler of the Eq function
        """
        
        # check theValue type and resolve (if needed)
        #if isinstance(theValue, (types.FunctionCall, types.Variable)):
        #    theValue = self.resolve(theEnv, theValue)
        theValue = self.semplify(theEnv, theValue)

        for theArg in args:
            # resolve the real value
            # before comparison
            theArg = self.semplify(theEnv, theArg)
            # != and == operators for BaseParsedType are overrided for 
            # types + value comparisong
            if not theValue == theArg:
                return types.Symbol("FALSE")
            
        return types.Symbol("TRUE")


Eq.DEFINITION = FunctionDefinition("?SYSTEM?", "eq", Eq(), types.Symbol, Eq.do ,
            [
                Constraint_MinArgsLength(2),
            ],forward=False)
