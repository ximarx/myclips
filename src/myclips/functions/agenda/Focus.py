'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, \
    Constraint_ExactArgsLength, Constraint_MinArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgValueError


class Focus(Function):
    '''
    Pushes one or more modules onto the focus stack. 
    The specified modules are pushed onto the focus stack 
    in the reverse order they are listed. 
    The current module is set to the last module pushed onto the focus stack. 
    The current focus is the top module of the focus stack. 
    Thus (focus A B C) pushes C, then B, then A unto the focus stack so that A is now the current focus. 
    Note that the current focus is different from the current module. 
    Focusing on a module implies "remembering" the current module so that it can be returned to later. 
    Setting the current module with the setcurrentmodule function changes it without remembering the old module. 
    Before a rule executes, the current module is changed to the module in which the executing rule is defined (the current focus). 
    This function returns a boolean value: FALSE if an error occurs, otherwise TRUE.
           
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-13.7.html#Heading450
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-13.7.html#Heading450
        """
        
        args = list(args)
        args.reverse()
        
        try:
            for theModule in args:
                theModule = self.resolve(theEnv,
                                         self.semplify(theEnv, theModule, types.Symbol, ("ALL", "symbol")))
                
                if not theEnv.modulesManager.isDefined(theModule):
                    raise InvalidArgValueError("Unable to find defmodule %s"%theModule)
                else:
                    theEnv.network.agenda.focusStack.append(theModule)
                    
            return types.Symbol("TRUE")        
        except IndexError:
            return types.Symbol("FALSE")

        
    
Focus.DEFINITION = FunctionDefinition("?SYSTEM?", "focus", Focus(), types.Symbol, Focus.do,
            [
                Constraint_MinArgsLength(1),
                Constraint_ArgType(types.Symbol)
            ],forward=False)
        
        