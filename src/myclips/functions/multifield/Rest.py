'''
Created on 08/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType,\
    Constraint_ExactArgsLength
from myclips.functions.Function import Function


class Rest(Function):
    '''
    This function returns all but the first field of a multifield value as a multifield value.
    
    (rest$ <multifield-expression>)
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading229
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theMultifield, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading229
        """

        
        theMultifield = self.semplify(theEnv, theMultifield, list, ("1", "multifield"))
                
        return theMultifield[1:None]
        
    
Rest.DEFINITION = FunctionDefinition("?SYSTEM?", "rest$", Rest(), list, Rest.do,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType(list, 0),
            ],forward=False)