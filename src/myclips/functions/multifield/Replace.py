'''
Created on 08/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType,\
    Constraint_MinArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgValueError
from myclips.rete.WME import WME


class Replace(Function):
    '''
    This function replaces a range of field in a 
    multifield value with a series of single-field 
    and/or multifield values and returns a new multifield value 
    containing the replacement values within the original multifield value

    (replace$ <multifield-expression> <begin-integer-expression> <end-integer-expression> <single-or-multi-field-expression>+)

    where <begin-integer-expression> to <end-integer-expression> is the range of values to be replaced.
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading226
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theMultifield, theBegin, theEnd, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading226
        """

        
        theMultifield = Function.semplify(theEnv, theMultifield, list, ("1", "multifield"))
        theBegin = Function.resolve(theEnv, 
                                    Function.semplify(theEnv, theBegin, types.Integer, ("2", "integer")))
        theEnd = Function.resolve(theEnv, 
                                    Function.semplify(theEnv, theEnd, types.Integer, ("3", "integer")))


        try:
            if theBegin - 1 >= len(theMultifield) or theEnd > len(theMultifield):
                raise IndexError()
            
            theBegin = theMultifield[0:theBegin-1]
            theEnd = theMultifield[theEnd:None]
            
        except IndexError:
            # invalid field!
            raise InvalidArgValueError("Multifield index %s out of range 1..%d in function delete$"%(
                                            ("range %d..%d"%(theBegin, theEnd) if theBegin != theEnd else str(theBegin)),
                                            len(theMultifield)
                                        ))
        else:
            theInner = []
            for theArg in args:
                theArg = Function.semplify(theEnv, theArg, (list), ("1", "number, lexeme, fact-address or multifield"))
                if  isinstance(theArg, list):
                    theInner += theArg
                else:
                    theInner.append(theArg)
                    
            return theBegin + theInner + theEnd
        
    
Replace.DEFINITION = FunctionDefinition("?SYSTEM?", "replace$", Replace(), list, Replace.do,
            [
                Constraint_MinArgsLength(4),
                Constraint_ArgType(list, 0),
                Constraint_ArgType(types.Integer, 1),
                Constraint_ArgType(types.Integer, 2),
                Constraint_ArgType((types.Lexeme, types.Number, WME, list), 3),
                Constraint_ArgType((types.Lexeme, types.Number, WME, list), (4,None), failIfMissing=False)
            ],forward=False)