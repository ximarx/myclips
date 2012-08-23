'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_ArgType, Constraint_MinArgsLength, Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function
from myclips.rete.WME import WME
import myclips

class SetLogLevel(Function):
    '''
    Change MyCLIPS logger level
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theLevel, *args, **kargs):
        """
        function handler implementation
        """

        theLevel = self.resolve(theEnv, 
                                 self.semplify(theEnv, theLevel, types.Integer, ("1", "integer")))
            
        
        myclips.logger.setLevel(theLevel)
        
        return types.NullValue()
    
    
SetLogLevel.DEFINITION = FunctionDefinition("?SYSTEM?", "set-log-level", SetLogLevel(), types.NullValue, SetLogLevel.do ,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType(types.Integer, 0),
            ],forward=False)
        
        