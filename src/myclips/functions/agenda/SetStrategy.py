'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, \
    Constraint_ExactArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgValueError
from myclips import strategies


class SetStrategy(Function):
    '''
    This function sets the current conflict resolution strategy. The default strategy is depth.
    
    (setstrategy <strategy>)

    where <strategy> is either depth, breadth, simplicity, complexity, lex, mea, or random. 
    The old conflict resolution strategy is returned. 
    The agenda will be reordered to reflect the new conflict resolution strategy.
           
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-13.7.html#Heading452
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theStrategy, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-13.7.html#Heading452
        """
        
        
        theStrategy = self.resolve(theEnv,
                                 self.semplify(theEnv, theStrategy, types.Symbol, ("1", "symbol")))

        if strategies.factory.isValid(theStrategy):
            theOld = theEnv.network.agenda.changeStrategy(strategies.factory.newInstance(theStrategy))
            return types.Symbol(theOld)
        else:
            raise InvalidArgValueError("Function set-strategy expected argument #1 to be of type symbol "
                                       + "with value depth, breadth, lex, mea, complexity, simplicity, or random")

        
    
SetStrategy.DEFINITION = FunctionDefinition("?SYSTEM?", "set-strategy", SetStrategy(), types.Symbol, SetStrategy.do,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType(types.Symbol)
            ],forward=False)
        
        