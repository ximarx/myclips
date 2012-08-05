'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType, Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgTypeError

class Absolute(Function):
    '''
    The abs function returns the absolute value of its only argument (which should be a numeric expression). 
    The return value will either be integer or float (depending upon the type the argument).
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.5.html#Heading261
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theNumber, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.5.html#Heading261
        """
        
        theNumber = self.resolve(theEnv, theNumber) if isinstance(theNumber, (types.FunctionCall, types.Variable)) else theNumber 
        
        if not isinstance(theNumber, (types.Integer, types.Float)):
            raise InvalidArgTypeError("Function abs expected argument #1 to be of type integer or float")
            
        return theNumber if theNumber.evaluate() >= 0 else theNumber.__class__(-1 * theNumber.evaluate())
            
    
Absolute.DEFINITION = FunctionDefinition("?SYSTEM?", "abs", Absolute(), (types.Integer, types.Float, types.Number), 
                                                                Absolute.do,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType(types.Number)
            ],forward=False)
        
        