'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgValueError

class Printout(Function):
    '''
    Print a list of statements in an resource (default: stdout) 
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, funcEnv, resourceId, *args, **kargs):
        """
        Retract function handler implementation
        """
        
        # convert <TYPE:value> to python value
        resourceId = Function.resolve(self, funcEnv, self.semplify(funcEnv, resourceId, types.Symbol, ("1", "symbol")))
        
        if resourceId != "nil":
            try:
                resource = funcEnv.RESOURCES[resourceId]
            except KeyError:
                raise InvalidArgValueError("Resource with logical name %s cannot be found"%str(resourceId))
            else:
            
                for fragment in args:
                    
                    # revolve variables and function calls
                    fragment = self.resolve(funcEnv, self.semplify(funcEnv, fragment))
                    
                    resource.write(str(fragment))
                    
        return types.NullValue()
    
    def resolve(self, funcEnv, arg):
        """
        Override Function.resolve to manage the <Symbol:crlf> conversion to NEWLINE
        and to remove quotes in types.String values
        """
        if isinstance(arg, types.Symbol) and arg.pyEqual("crlf"):
            return "\n"
        else:
            return Function.resolve(self, funcEnv, arg)
    
# Function definition

Printout.DEFINITION = FunctionDefinition("?SYSTEM?", "printout", Printout(), types.NullValue, Printout.do ,
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(types.Symbol, 0),
            ],forward=False)
        
        