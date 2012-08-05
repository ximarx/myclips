'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgTypeError

class Addition(Function):
    '''
    The + function returns the sum of its arguments. 
    Each of its arguments should be a numeric expression. 
    Addition is performed using the type of the arguments provided unless mixed mode arguments
    (integer and float) are used. 
    In this case, the function return value 
    and integer arguments are converted to floats 
    after the first float argument has been encountered. 
    This function returns a float if any of its arguments is a float, 
    otherwise it returns an integer.
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.5.html#Heading254
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theFirst, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.5.html#Heading254
        """
        
        theFirst = self.resolve(theEnv, theFirst) if isinstance(theFirst, (types.FunctionCall, types.Variable)) else theFirst 
        
        if not isinstance(theFirst, (types.Integer, types.Float)):
            raise InvalidArgTypeError("Function + expected argument #1 to be of type integer or float")
        
        theSum = theFirst.evaluate()
        
        for (index, theSecond) in enumerate(args):
            if isinstance(theSecond, (types.FunctionCall, types.Variable)):
                theSecond = self.resolve(theEnv, theSecond)
                
            if not isinstance(theSecond, (types.Integer, types.Float)):
                raise InvalidArgTypeError("Function + expected argument #%d to be of type integer or float"%index + 2)
            
            theSum = theSum + theSecond.evaluate()
            
        # CLIPS documentation:
        # after all computations, if the value is still an integer, then create a new <Integer:theSum>
        # otherwise <Float:theSum>
        
        if isinstance(theSum, int):
            return types.Integer(theSum)
        else:
            return types.Float(theSum)
        
            
    
Addition.DEFINITION = FunctionDefinition("?SYSTEM?", "+", Addition(), (types.Number, types.Integer, types.Float), 
                                                                Addition.do,
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(types.Number)
            ],forward=False)
        
        