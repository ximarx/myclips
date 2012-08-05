'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType, Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgTypeError

class Float(Function):
    '''
    The float function converts its only argument 
    (which should be a numeric expression) 
    to type float and returns this value.
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.5.html#Heading262
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theNumber, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.5.html#Heading262
        """
        
        theNumber = self.resolve(theEnv, theNumber) if isinstance(theNumber, (types.FunctionCall, types.Variable)) else theNumber 
        
        if not isinstance(theNumber, (types.Integer, types.Float)):
            raise InvalidArgTypeError("Function float expected argument #1 to be of type integer or float")
            
        return types.Float(float(theNumber.evaluate()))
            
    
Float.DEFINITION = FunctionDefinition("?SYSTEM?", "float", Float(), types.Float, 
                                                                Float.do,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType(types.Number)
            ],forward=False)
        
        