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
    
    WARNING: clips docs is wrong. The first argument must be greater that the second for the null string
    to be returned
    
    CLIPS (V6.24 06/15/06)
    CLIPS> (sub-string 3 3 "abcdef")
    "c"
    CLIPS> (sub-string 4 3 "avcdef")
    ""
    CLIPS> (sub-string 3 4 "1234567")
    "34"
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading233
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theStart, theEnd, theString, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading233
        """
        
        # normalize theStart
        if isinstance(theStart, (types.Variable, types.FunctionCall)):
            theStart = self.resolve(theEnv, theStart)
        if not isinstance(theStart, types.Integer):
            raise InvalidArgTypeError("Function sub-string expected argument #1 to be of type integer")
        theStart = theStart.evaluate() 
        
        # normalize theEnd
        if isinstance(theEnd, (types.Variable, types.FunctionCall)):
            theEnd = self.resolve(theEnv, theEnd)
        if not isinstance(theEnd, types.Integer):
            raise InvalidArgTypeError("Function sub-string expected argument #2 to be of type integer")
        theEnd = theEnd.evaluate()
        
        # normalize theString
        if isinstance(theString, (types.Variable, types.FunctionCall)):
            theString = self.resolve(theEnv, theString)
        if not isinstance(theString, types.String):
            raise InvalidArgTypeError("Function sub-string expected argument #3 to be of type string")
        theString = theString.evaluate()[1:-1] # remove the quotes


        theNew = theString[theStart-1:theEnd]
        
        return types.String(theNew)
        
        
    
SubString.DEFINITION = FunctionDefinition("?SYSTEM?", "sub-string", SubString(), types.String, SubString.do,
            [
                Constraint_ExactArgsLength(3),
                Constraint_ArgType(types.Integer, 0),
                Constraint_ArgType(types.Integer, 1),
                Constraint_ArgType(types.String, 2)
            ],forward=False)
        
        