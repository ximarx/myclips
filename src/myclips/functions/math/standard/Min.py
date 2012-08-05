'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgTypeError

class Min(Function):
    '''
    The min function returns the value of its smallest numeric argument. 
    Each of its arguments should be a numeric expression. 
    When necessary, integers are temporarily converted to floats for comparison. 
    The return value will either be integer or float (depending upon the type of the smallest argument).
    
    Undocumented in CLIPS:
    in the case of equality, the result is the one found first
    (min 2 2.0) => 2
    (min 2.0 2) => 2.0
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.5.html#Heading260
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theFirst, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.5.html#Heading260
        """
        
        theFirst = self.resolve(theEnv, theFirst) if isinstance(theFirst, (types.FunctionCall, types.Variable)) else theFirst 
        
        if not isinstance(theFirst, (types.Integer, types.Float)):
            raise InvalidArgTypeError("Function max expected argument #1 to be of type integer or float")
        
        theMin = theFirst
        
        for (index, theSecond) in enumerate(args):
            if isinstance(theSecond, (types.FunctionCall, types.Variable)):
                theSecond = self.resolve(theEnv, theSecond)
                
            if not isinstance(theSecond, (types.Integer, types.Float)):
                raise InvalidArgTypeError("Function max expected argument #%d to be of type integer or float"%index + 2)
            
            
            theMin = theMin if theMin.evaluate() <= theSecond.evaluate() else theSecond
            
        return theMin
        
            
    
Min.DEFINITION = FunctionDefinition("?SYSTEM?", "min", Min(), (types.Integer, types.Float, types.Number), 
                                                                Min.do,
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(types.Number)
            ],forward=False)
        
        