'''
Created on 06/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType,\
    Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgTypeError


class SubString(Function):
    '''
    The substring function will retrieve a portion of a string from another string.
    
    (sub-string <integer-expression> <integer-expression> <string-expression>)

    where the first argument, counting from one, must be a number marking the beginning position
    in the string and the second argument must be a number marking the ending position in the string.
    If the first argument is greater than or equal to the second argument, a null string is returned.
    
    WARNING: clips doc is wrong. The first argument must be greater that the second for the null string
    to be returned
    
    3rd argument can be a string or a symbol too
    
    CLIPS (V6.24 06/15/06)
    CLIPS> (sub-string 3 3 "abcdef")
    "c"
    CLIPS> (sub-string 4 3 "avcdef")
    ""
    CLIPS> (sub-string 3 4 "1234567")
    "34"
    CLIPS> (sub-string 3 3 "ciao")
    "a"
           
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading233
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theStart, theEnd, theString, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading233
        """
        
        
        theStart = self.resolve(theEnv, 
                                self.semplify(theEnv, theStart, types.Integer, ("1", "integer")))
         
        theEnd = self.resolve(theEnv, 
                                self.semplify(theEnv, theEnd, types.Integer, ("2", "integer")))
         
        theString = self.resolve(theEnv, 
                                self.semplify(theEnv, theString, types.Lexeme, ("3", "string or symbol")))


        return types.String(theString[theStart-1:theEnd])
        
        
    
SubString.DEFINITION = FunctionDefinition("?SYSTEM?", "sub-string", SubString(), types.String, SubString.do,
            [
                Constraint_ExactArgsLength(3),
                Constraint_ArgType(types.Integer, 0),
                Constraint_ArgType(types.Integer, 1),
                Constraint_ArgType(types.Lexeme, 2)
            ],forward=False)
        
        