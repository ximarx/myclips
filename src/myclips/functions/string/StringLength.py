'''
Created on 07/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType,\
    Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function


class StringLength(Function):
    '''
    The str-length function returns the length of a string as an integer.
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading240
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theString, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading240
        """
        
        # resolve to a python value (trim quotes from string too)
        theString = StringLength.resolve(theEnv, 
                                        # semplify to a BaseParsedType if variable or function call and check types
                                        StringLength.semplify(theEnv, theString, (types.String, types.Symbol), ("1", "string or symbol")))

        return types.Integer(len(theString))
        
    
StringLength.DEFINITION = FunctionDefinition("?SYSTEM?", "str-length", StringLength(), types.Integer, StringLength.do,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType(types.Lexeme, 0),
            ],forward=False)
        
        