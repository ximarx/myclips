'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.rete.WME import WME
from myclips.functions.Function import Function

class Bind(Function):
    '''
    Bind a value to a variable name
    (local or global)
    
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading279
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, funcEnv, variable, *args, **kargs):
        """
        handler of the Bind function:
            set a global variable running value
            if variable is a global one
            or set a new local variable value
            
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html#Heading279
        """
        
        returnValue = types.Symbol("FALSE")
        
        # i can't use the resolve method to get
        # the variable name, because resolve will resolve to the value
        # instead, i need to variable name
        
        assert isinstance(variable, types.Variable)
        # this can give me ?*NAME* or ?NAME
        varName = variable.evaluate()
        # compute the new value
        if len(args) == 0:
            # no expression is passed. New value is None
            newValue = None
        elif len(args) == 1:
            # it's a single argument
            newValue = self.semplify(funcEnv, args[0])
        else:
            # more than one, create a multifield for them
            newValue = [self.semplify(funcEnv, arg) for arg in args]

        if isinstance(variable, types.GlobalVariable):
            
            # so i need to modify the definition in the globalsManager for the current scope
            definition = funcEnv.network.modulesManager.currentScope.globalsvars.getDefinition(variable.evaluate())
            # linkedType in a GlobalVarDefinition is a types.GlobalAssignment
            if newValue is not None:
                definition.linkedType.runningValue = newValue
                returnValue = newValue
            else:
                # as for http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html
                # in Bind documentation:
                # if the new value of the global is None, the original value have to be restored
                definition.linkedType.runningValue = definition.linkedType.value
                returnValue = definition.linkedType.value
        
        else:
            # the variable is a rule-scope variable
            if newValue is not None:
                # bind the new variable
                funcEnv.variables[varName] = newValue
                returnValue = newValue
            else:
                # as for http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.6.html
                # in Bind documentation:
                # if the new value of a local variable is None, the variable must be unbound
                del funcEnv.variables[varName]
                
            
        return returnValue
    
    
Bind.DEFINITION = FunctionDefinition("?SYSTEM?", "bind", Bind(), (types.Lexeme, types.Symbol, types.String, 
                                                                       types.Number, types.Integer, types.Float,
                                                                       list, types.NullValue, WME ),
                                                                    Bind.do,
            [
                Constraint_MinArgsLength(1),
                Constraint_ArgType((types.SingleFieldVariable, types.MultiFieldVariable, types.GlobalVariable), 0),
            ],forward=False)
        
        