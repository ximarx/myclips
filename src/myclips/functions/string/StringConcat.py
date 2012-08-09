'''
Created on 06/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType
import myclips.parser.Types as types
from myclips.functions.Function import Function
from myclips.rete.WME import WME


class StringConcat(Function):
    '''
    The strcat function will concatenates its arguments into a single string.     
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading231
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading231
        """
        
        concat = ""
        
        for arg in args:
            concat += str(StringConcat.resolve(theEnv, 
                                 StringConcat.semplify(theEnv, arg, (types.BaseParsedType, WME), ("ALL", "lexeme, number or fact-address"))))
                
        return types.String(concat)
        
        
    
StringConcat.DEFINITION = FunctionDefinition("?SYSTEM?", "str-cat", StringConcat(), types.String, StringConcat.do,
            [
                Constraint_ArgType((types.Symbol, types.String, types.Float, types.Integer, types.Number, types.Lexeme, WME))
            ],forward=False)
        
        