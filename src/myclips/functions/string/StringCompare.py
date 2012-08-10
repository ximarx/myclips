'''
Created on 07/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType,\
    Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function


class StringCompare(Function):
    '''
    The strcompare function will compare two strings to determine their logical relationship
    (i.e., equal to, less than, greater than). 
    The comparison is performed character-by-character until the strings are exhausted 
    (implying equal strings) or unequal characters are found. 
    The positions of the unequal characters within the ASCII
    character set are used to determine the logical relationship of unequal strings.
     
    WARNING:
    this function implementation is based on the python's cmp function 
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading239
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theLeft, theRight, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading239
        """
        
        # resolve to a python value (trim quotes from string too)
        theLeft = self.resolve(theEnv, 
                                        # semplify to a BaseParsedType if variable or function call and check types
                                        self.semplify(theEnv, theLeft, (types.String, types.Symbol), ("1", "string or symbol")))
        # resolve to a python value (trim quotes from string too)
        theRight = self.resolve(theEnv,
                                         # semplify to a BaseParsedType if variable or function call and check types 
                                         self.semplify(theEnv, theRight, (types.String, types.Symbol), ("2", "string or symbol")))

        return types.Integer(cmp(theLeft, theRight))
        
    
StringCompare.DEFINITION = FunctionDefinition("?SYSTEM?", "str-compare", StringCompare(), types.Integer, StringCompare.do,
            [
                Constraint_ExactArgsLength(2),
                Constraint_ArgType(types.Lexeme, 0),
                Constraint_ArgType(types.Lexeme, 1)
            ],forward=False)
        
        