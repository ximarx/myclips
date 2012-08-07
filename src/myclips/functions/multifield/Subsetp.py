'''
Created on 07/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType,\
    Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function
from myclips.rete.WME import WME


class Subsetp(Function):
    '''
    This function checks if one multifield value is a subset of another; i.e., 
    if all the fields in the first multifield value are also in the second multifield value.

    (subsetp <multifield-expression> <multifield-expression>)

    If the first argument is a subset of the second argument, the function returns TRUE; 
    otherwise, it returns FALSE. 
    The order of the fields is not considered. 
    If the first argument is bound to a multifield of length zero, the subsetp function always returns TRUE.
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading221
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theSubSet, theMultifield, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading221
        """

        theSubSet = Function.semplify(theEnv, theSubSet, list, ("1", "multifield"))
        theMultifield = Function.semplify(theEnv, theMultifield, list, ("2", "multifield"))

        return types.Symbol("TRUE") if set(theSubSet) <= set(theMultifield) else types.Symbol("FALSE")
        
    
Subsetp.DEFINITION = FunctionDefinition("?SYSTEM?", "subsetp", Subsetp(), types.Symbol, Subsetp.do,
            [
                Constraint_ExactArgsLength(2),
                Constraint_ArgType(list, 0),
                Constraint_ArgType(list, 1)
            ],forward=False)