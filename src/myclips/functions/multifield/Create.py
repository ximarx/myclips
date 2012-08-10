'''
Created on 07/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType
import myclips.parser.Types as types
from myclips.functions.Function import Function
from myclips.rete.WME import WME


class Create(Function):
    '''
    This function appends any number of fields together to create a multifield value.
    
    (create$ <expression>*)

    The return value of create$ is a multifield value regardless of the number
    or types of arguments (single-field or multifield). 
    Calling create$ with no arguments creates a multifield value of length zero. 
    This function may also be called using the name create$.
    
    WARNING: a nested create$ call doesn't create a nested multifield,
    but values in the inner multifield are appended to the main one.
    Always a flat (1 level) multifield is returned
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading218
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading218
        """

        theArgs = []
        for i, theArg in enumerate(args):        
            # semplify to a BaseParsedType if variable or function call and check types
            theArg = self.semplify(theEnv, theArg, (types.BaseParsedType, list, WME), (str(i+1), "number, lexeme, multifield or WME"))
            if isinstance(theArg, list):
                theArgs += theArg
            else:
                theArgs.append(theArg)

        return theArgs
        
    
Create.DEFINITION = FunctionDefinition("?SYSTEM?", "create$", Create(), list, Create.do,
            [
                Constraint_ArgType((WME, list, types.Lexeme, types.Number), failIfMissing=False)
            ],forward=False)
        
        