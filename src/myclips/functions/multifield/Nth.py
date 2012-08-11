'''
Created on 07/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType,\
    Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function
from myclips.rete.WME import WME


class Nth(Function):
    '''
    The nth$ function will return a specified field from a multifield value.
    
    (nth$ <integer-expression> <multifield-expression>)

    where the first argument should be an integer from 1 to the number
    of elements within the second argument. 
    The symbol nil will be returned if the first argument is greater
    than the number of fields in the second argument.
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading219
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theIndex, theMultifield, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading219
        """

        theIndex = self.resolve(theEnv, self.semplify(theEnv, theIndex, types.Integer, ("1", "integer")))

        try:
            return self.semplify(theEnv, theMultifield)[theIndex-1]
        except IndexError:
            return types.Symbol("nil")
    
Nth.DEFINITION = FunctionDefinition("?SYSTEM?", "nth$", Nth(), (types.Integer, types.Float, types.Number,
                                                                types.String, types.Symbol, types.Lexeme, WME), Nth.do,
            [
                Constraint_ExactArgsLength(2),
                Constraint_ArgType(types.Integer, 0),
                Constraint_ArgType(list, 1)
            ],forward=False)
        
        