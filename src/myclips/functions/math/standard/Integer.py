'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType, Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgTypeError

class Integer(Function):
    '''
    The integer function converts its only argument 
    (which should be a numeric expression) 
    to type integer and returns this value.
    
    WARNING: 
    float to integer conversion is performed always
    using truncate(x) where x is the float value
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.5.html#Heading263
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theNumber, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.5.html#Heading263
        """
        
        theNumber = self.resolve(theEnv, theNumber) if isinstance(theNumber, (types.FunctionCall, types.Variable)) else theNumber 
        
        if not isinstance(theNumber, (types.Integer, types.Integer)):
            raise InvalidArgTypeError("Function integer expected argument #1 to be of type integer or float")
            
        return types.Integer(int(theNumber.evaluate()))
            
    
Integer.DEFINITION = FunctionDefinition("?SYSTEM?", "integer", Integer(), types.Integer, 
                                                                Integer.do,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType(types.Number)
            ],forward=False)
        
        