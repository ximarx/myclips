'''
Created on 06/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgValueError,\
    InvalidArgTypeError

class Format(Function):
    '''
    The format function allows a user to send formatted output 
    to a device attached to a logical name. 
    It can be used in place of printout when special formatting 
    of output information is desired. 
    Although a slightly more complicated function, 
    format provides much better control over how the output is formatted. 
    The format commands are similar to the printf statement in C. 
    The format function always returns a string containing the formatted output. 
    A logical name of nil may be used when the formatted return string is desired without writing to a device.
    @http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.4.html#Heading249
    
    WARNING:
    supported format string commands are the ones from % operand:
    @http://docs.python.org/library/stdtypes.html#string-formatting 
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, funcEnv, resourceId, theFormat, *args, **kargs):
        """
        Function handler implementation
        """
        
        # convert <FunctionCall> to his value if needed for theFormat
        resourceId = Format.resolve(funcEnv, resourceId) if isinstance(resourceId, (types.Variable, types.FunctionCall)) else resourceId
        if not isinstance(resourceId, types.Symbol):
            raise InvalidArgTypeError("Function format expected argument #1 to be of type symbol")
        
        # convert <FunctionCall> to his value if needed for theFormat
        theFormat = Format.resolve(funcEnv, theFormat) if isinstance(resourceId, (types.Variable, types.FunctionCall)) else theFormat
        if not isinstance(theFormat, types.String):
            raise InvalidArgTypeError("Function format expected argument #2 to be of type string")
        
        try:
            if not resourceId.pyEqual('nil'):
                resource = funcEnv.RESOURCES[resourceId.evaluate()]
            else:
                resource = None
        except KeyError:
            raise InvalidArgValueError("Resource with logical name %s cannot be found"%str(resourceId))
        else:
            
            returnValueRaw = []
            
            for fragment in args:
                
                # revolve variables and function calls
                returnValueRaw.append(Format.resolve(funcEnv, fragment))
                
                
            # theFormat is a string
            returnValueRaw = theFormat.evaluate()[1:-1]%tuple([x.evaluate() if isinstance(x, types.BaseParsedType) else x for x in returnValueRaw])

            if resource is not None:
                resource.write(returnValueRaw)
            
            return types.String(returnValueRaw)
    
# Function definition

Format.DEFINITION = FunctionDefinition("?SYSTEM?", "format", Format(), types.String, Format.do ,
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(types.Symbol, 0),
                Constraint_ArgType(types.String, 1),
            ],forward=False)
        
        