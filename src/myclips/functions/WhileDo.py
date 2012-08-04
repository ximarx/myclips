'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.rete.WME import WME
from myclips.functions.Function import Function, BreakException

class WhileDo(Function):
    '''
    While-Do conditional function
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading281
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theCondition, *args, **kargs):
        """
        handler of the WhileDo function:
            while-do conditional structure
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading281
        """
        
        returnValue = types.Symbol("FALSE")
        
        
        theActions = []
        # strip the optional DO from the args[0] if it's there
        if len(args) > 0:
            if isinstance(args[0], types.Symbol) and args[0].pyEqual("do"):
                theActions = list(args[1:])
            else:
                theActions = list(args)
                
        
        # CLIPS documentation:
        # while will loop until theResult is a <Symbol:FALSE> or Return/Break functions are used
        # if return is used, the function execution halt
        # if break is used, loop break and while return a value
        # so, return is not caught here, but from the function caller 
        # break are caught here instead

        try:
            if isinstance(theCondition, (types.FunctionCall, types.Variable)):
                theResult = self.resolve(theEnv, theCondition)
    
            while not (isinstance(theResult, types.Symbol) and theResult.pyEqual("FALSE")):
    
                for action in theActions:
                    # function are executed
                    if isinstance(action, types.FunctionCall):
                        self.resolve(theEnv, action)

                if isinstance(theCondition, (types.FunctionCall, types.Variable)):
                    theResult = self.resolve(theEnv, theCondition)
                    
        except BreakException:
            # break caught, stop loooooooooop!
            pass
            
        # CLIPS documentation:
        # the if-then-else return value is always the value of the last execute action
        return returnValue
            
    
WhileDo.DEFINITION = FunctionDefinition("?SYSTEM?", "while", WhileDo(), (types.Lexeme, types.Symbol, types.String, 
                                                                                    types.Number, types.Integer, types.Float,
                                                                                    list, types.NullValue, WME ), 
                                                                WhileDo.do,
            [
                Constraint_MinArgsLength(1),
                Constraint_ArgType((types.FunctionCall, types.Variable), 0)
            ],forward=False)
        
        