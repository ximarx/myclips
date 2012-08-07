'''
Created on 07/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType,\
    Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function
from myclips.rete.WME import WME


class Member(Function):
    '''
    The member$ function will tell if a single field value is contained in a multifield value.

    (member$ <single-field-expression> <multifield-expression>)

    If the first argument is one of the fields within the second argument, 
    member$ will return the integer position of the field 
    (from 1 to the length of the second argument). 
    Otherwise, it will return FALSE.
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading220
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theValue, theMultifield, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading220
        """

        theValue = Member.semplify(theEnv, theValue, (types.Lexeme, types.Number, WME), ("1", "number, lexeme or fact"))
        theMultifield = Member.semplify(theEnv, theMultifield, list, ("2", "multifield"))
        
        try:
            theIndex = theMultifield.index(theValue)
        except ValueError:
            return types.Symbol("FALSE")
        else:
            return types.Integer(theIndex)
    
Member.DEFINITION = FunctionDefinition("?SYSTEM?", "member$", Member(), (types.Symbol, types.Integer), Member.do,
            [
                Constraint_ExactArgsLength(2),
                Constraint_ArgType((types.Number, types.Lexeme, WME), 0),
                Constraint_ArgType(list, 1)
            ],forward=False)
        
        