'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgTypeError

class Division(Function):
    '''
    The / function returns the value of the first argument divided by each of the subsequent arguments. 
    Each of its arguments should be a numeric expression.
    All arguments are converted to float before the computation
    and the return value is always a <Float> type (even if all arguments are integer)
    (integer) function can be used to cast the return value to integer value 
    
    WARNING: this implementation is different from the CLIPS one
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.5.html#Heading257
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theFirst, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.5.html#Heading257
        """
        
        theFirst = self.resolve(theEnv, theFirst) if isinstance(theFirst, (types.FunctionCall, types.Variable)) else theFirst 
        
        if not isinstance(theFirst, (types.Integer, types.Float)):
            raise InvalidArgTypeError("Function / expected argument #1 to be of type integer or float")
        
        theDiv = float(theFirst.evaluate())
        
        for (index, theSecond) in enumerate(args):
            if isinstance(theSecond, (types.FunctionCall, types.Variable)):
                theSecond = self.resolve(theEnv, theSecond)
                
            if not isinstance(theSecond, (types.Integer, types.Float)):
                raise InvalidArgTypeError("Function / expected argument #%d to be of type integer or float"%index + 2)
            
            theDiv = theDiv / float(theSecond.evaluate())
            
        # WARNING:
        # this function always return a Float!
        return types.Float(theDiv)
        
            
    
Division.DEFINITION = FunctionDefinition("?SYSTEM?", "*", Division(), types.Float, 
                                                                Division.do,
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(types.Number)
            ],forward=False)
        
        