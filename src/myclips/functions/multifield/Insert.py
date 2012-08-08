'''
Created on 08/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType,\
    Constraint_MinArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgValueError
from myclips.rete.WME import WME


class Insert(Function):
    '''
    This function inserts a series of single- field and/or multifield values 
    at a specified location in a multifield value with and returns 
    a new multifield value containing the inserted values within the original multifield value.

    (insert$ <multifield-expression> <integer-expression> <single-or-multi-field-expression>+)

    where <integer-expression> is the location where the values are to be inserted. 
    This value must be greater than or equal to 1. 
    A value of 1 inserts the new value(s) at the beginning of the <multifield-expression>. 
    Any value greater than the length of the <multifield- expression> 
    appends the new values to the end of the <multifield- expression>.
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading227
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theMultifield, theIndex, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading227
        """

        
        theMultifield = Function.semplify(theEnv, theMultifield, list, ("1", "multifield"))
        theIndex = Function.resolve(theEnv, 
                                    Function.semplify(theEnv, theIndex, types.Integer, ("2", "integer")))


        theBegin = theMultifield[0:theIndex-1]
        theEnd = theMultifield[theIndex-1:None]
        
        theInner = []
        for theArg in args:
            theArg = Function.semplify(theEnv, theArg, (list), ("1", "number, lexeme, fact-address or multifield"))
            if  isinstance(theArg, list):
                theInner += theArg
            else:
                theInner.append(theArg)
                
        return theBegin + theInner + theEnd
        
    
Insert.DEFINITION = FunctionDefinition("?SYSTEM?", "insert$", Insert(), list, Insert.do,
            [
                Constraint_MinArgsLength(3),
                Constraint_ArgType(list, 0),
                Constraint_ArgType(types.Integer, 1),
                Constraint_ArgType((types.Lexeme, types.Number, WME, list), 2),
                Constraint_ArgType((types.Lexeme, types.Number, WME, list), (3,None), failIfMissing=False)
            ],forward=False)