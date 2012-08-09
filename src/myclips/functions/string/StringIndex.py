'''
Created on 07/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType,\
    Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgTypeError
import string as pystring


class StringIndex(Function):
    '''
    The str-index function will return the position of a string inside another string.
    
    (str-index <lexeme-expression> <lexeme-expression>)

    where the second argument is searched for the first occurrence of the first argument.
    The str-index function returns the integer starting position, counting from one, 
    of the first argument in the second argument or returns the symbol FALSE if not found.
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading234
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theNeedle, theHaystack, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading234
        """
        
        theNeedle = self.resolve(theEnv, 
                                 self.semplify(theEnv, theNeedle, types.Lexeme, ("1", "string or symbol")))
        
        theHaystack = self.resolve(theEnv, 
                                 self.semplify(theEnv, theHaystack, types.Lexeme, ("2", "string or symbol")))

        
        thePosition = pystring.find(theHaystack, theNeedle)
        
        if thePosition != -1:
            return types.Integer(thePosition + 1)
        else:
            return types.Symbol("FALSE")
        
        
    
StringIndex.DEFINITION = FunctionDefinition("?SYSTEM?", "str-index", StringIndex(), (types.Integer, types.Symbol), StringIndex.do,
            [
                Constraint_ExactArgsLength(2),
                Constraint_ArgType(types.Lexeme, 0),
                Constraint_ArgType(types.Lexeme, 1)
            ],forward=False)
        
        