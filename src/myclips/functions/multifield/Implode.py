'''
Created on 08/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType,\
    Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgValueError


class Implode(Function):
    '''
    This function creates a single string from a multifield value.

    (implode$ <multifield-expression>)

    Each field in <multifield-expression> in order is concatenated 
    into a string value with a single blank separating fields. 
    The new string is returned.
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading224
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)

        
    def do(self, theEnv, theMultifield, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading224
        """

        
        theMultifield = self.semplify(theEnv, theMultifield, list, ("1", "multifield"))
        
        return types.String(" ".join([str(x) for x in theMultifield]))
        
        
    
Implode.DEFINITION = FunctionDefinition("?SYSTEM?", "implode$", Implode(), list, Implode.do,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType(list, 0)
            ],forward=False)

