'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_MaxArgsLength
import myclips.parser.Types as types
from myclips.rete.WME import WME
from myclips.functions.Function import Function, BreakException,\
    InvalidArgValueError, ReturnException

class Return(Function):
    '''
    Return function
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading285
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theExpression=None, *args, **kargs):
        """
        handler of the Return function:
            stop deffunction/rule rhs execution and return a value
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading285
        """
        
        returnValue = None
        
        # theExpression could contain the return value
        # if it's a function call, it must be evaluated
        if theExpression is not None:
            # check if it's a function call
            if isinstance(theExpression, types.FunctionCall):
                returnValue = self.resolve(theEnv, theExpression)
            else:
                returnValue = theExpression
        
        
        # CLIPS documentation:
        # return_stmt ::= ( return [<expression>] )
        # if the expression is not provided,
        # no return value is returned
        # otherwise the return value of the expression
        # is returned
        raise ReturnException(returnValue)
            
            
    
Return.DEFINITION = FunctionDefinition("?SYSTEM?", "return", Return(), (types.Lexeme, types.Symbol, types.String, 
                                                                                    types.Number, types.Integer, types.Float,
                                                                                    list, types.NullValue, WME ), 
                                                                Return.do,
            [
                Constraint_MaxArgsLength(1)
            ],forward=False)
        
        