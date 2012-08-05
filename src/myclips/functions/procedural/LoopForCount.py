'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.rete.WME import WME
from myclips.functions.Function import Function, BreakException,\
    InvalidArgValueError

class LoopForCount(Function):
    '''
    Loop-For-Count conditional function
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading282
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theRange, *args, **kargs):
        """
        handler of the Loop-For-Count function:
            classic for-i-from-1-to-n  conditional structure
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading282
        """
        
        returnValue = types.Symbol("FALSE")
        
        # theRange is the range specifier
        # it could be a list([<Variable>, <Integer:MIN>, <Integer:MAX>]) or a <Integer:MAX>
        
        if isinstance(theRange, list):
            # if it's list, then:
            #    [0] is a variable
            #    [1] is the min
            #    [2] is the max
            if len(theRange) != 3 \
                    or not isinstance(theRange[0], types.SingleFieldVariable)\
                    or not isinstance(theRange[1], types.Integer)\
                    or not isinstance(theRange[2], types.Integer)\
                :
                raise InvalidArgValueError("Range specifier format for loop-for-count function must be a <Integer> or a [<Variable>, <Integer>, <Integer>]")
            
            theVarBind = theRange[0].evaluate()
            theMin = theRange[1].evaluate()
            theMax = theRange[2].evaluate() + 1
        else:
            # function definition restriction ensure theRange to  be a list or a <Integer>
            theMax = theRange.evaluate() + 1
            theMin = 1
            theVarBind = None
        
        
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
    
            for theVarValue in range(theMin, theMax):
                if theVarBind is not None:
                    theEnv.variables[theVarBind] = types.Integer(theVarValue)
                    
                for action in theActions:
                    # function are executed
                    if isinstance(action, types.FunctionCall):
                        self.resolve(theEnv, action)
                    
        except BreakException:
            # break caught, stop loooooooooop!
            pass
            
        # CLIPS documentation:
        # the if-then-else return value is always the value of the last execute action
        return returnValue
            
    
LoopForCount.DEFINITION = FunctionDefinition("?SYSTEM?", "loop-for-count", LoopForCount(), (types.Lexeme, types.Symbol, types.String, 
                                                                                    types.Number, types.Integer, types.Float,
                                                                                    list, types.NullValue, WME ), 
                                                                LoopForCount.do,
            [
                Constraint_MinArgsLength(1),
                Constraint_ArgType((types.Integer, list), 0)
            ],forward=False)
        
        