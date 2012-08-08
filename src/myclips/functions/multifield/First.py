'''
Created on 08/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType,\
    Constraint_ExactArgsLength
from myclips.functions.Function import Function


class First(Function):
    '''
    This function returns the first field of a multifield value as a multifield value
    
    (first$ <multifield-expression>)
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading228
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theMultifield, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading228
        """

        
        theMultifield = Function.semplify(theEnv, theMultifield, list, ("1", "multifield"))
                
        return theMultifield[0:1]
        
    
First.DEFINITION = FunctionDefinition("?SYSTEM?", "first$", First(), list, First.do,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType(list, 0),
            ],forward=False)