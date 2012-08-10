'''
Created on 06/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType
import myclips.parser.Types as types
from myclips.functions.Function import Function
from myclips.rete.WME import WME


class SymbolConcat(Function):
    '''
    The symcat function will concatenate its arguments into a single symbol. 
    It is functionally identical to the str-cat function with the exception that the returned value is a symbol and not a string.
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading232
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading232
        """
        
        concat = ""
        
        for arg in args:
            concat += str(self.resolve(theEnv, 
                                 self.semplify(theEnv, arg, (types.BaseParsedType, WME), ("ALL", "lexeme, number or fact-address"))))
                
        return types.Symbol(concat)
        
        
    
SymbolConcat.DEFINITION = FunctionDefinition("?SYSTEM?", "sym-cat", SymbolConcat(), types.Symbol, SymbolConcat.do,
            [
                Constraint_ArgType((types.Symbol, types.String, types.Float, types.Integer, types.Number, types.Lexeme, WME))
            ],forward=False)
        
        