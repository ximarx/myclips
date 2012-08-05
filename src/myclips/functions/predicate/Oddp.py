'''
Created on 05/aug/2012

@author: Francesco Capozzo
'''
import myclips.parser.Types as types
from myclips.functions.Function import Function
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_ExactArgsLength, Constraint_ArgType

class Oddp(Function):
    '''
    The oddp function returns the symbol TRUE if its argument is an odd number, otherwise it returns the symbol FALSE. 
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
    def do(self, theEnv, theValue, *args, **kargs):
        """
        handler of the Oddp function
        """
        
        # check theValue type and resolve (if needed)
        if isinstance(theValue, (types.FunctionCall, types.Variable)):
            theValue = self.resolve(theEnv, theValue)

        pyValue = theValue.evaluate()
            
        if bool(pyValue & 1): 
            returnValue = types.Symbol("TRUE")
        else:
            returnValue = types.Symbol("FALSE")
            
        return returnValue


Oddp.DEFINITION = FunctionDefinition("?SYSTEM?", "oddp", Oddp(), types.Symbol, Oddp.do ,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType(types.Integer, 0)
            ],forward=False)
