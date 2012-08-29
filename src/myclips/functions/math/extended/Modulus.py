'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength, Constraint_ArgType, Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgTypeError

class Modulus(Function):
    '''
    The mod function returns the remainder of the result of dividing its first argument by its second argument 
    (assuming that the result of division must be an integer). 
    It returns an integer if both arguments are integers, otherwise it returns a float.
    
    (mod <numeric-expression> <numeric-expression>)
    
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.5.html#Heading277
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theFirst, theSecond, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.5.html#Heading277
        """
        
        theFirst = self.semplify(theEnv, theSecond, types.Number, ("2", "integer or float"))
        theSecond = self.semplify(theEnv, theSecond, types.Number, ("2", "integer or float"))
        
        theReturnClass = types.Integer if isinstance(theFirst, types.Integer) and isinstance(theSecond, types.Integer) else types.Float 

        theMod = self.resolve(theEnv, theFirst) % self.resolve(theEnv, theSecond)
        
        return theReturnClass(theMod)
        
            
    
Modulus.DEFINITION = FunctionDefinition("?SYSTEM?", "mod", Modulus(), types.Number, 
                                                                Modulus.do,
            [
                Constraint_ExactArgsLength(2),
                Constraint_ArgType(types.Number)
            ],forward=False)
        
        