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
        
        resourceId =  self.semplify(funcEnv, resourceId, (types.Symbol), ("1", "symbol"))

        theFormat = self.resolve(funcEnv, self.semplify(funcEnv, theFormat, (types.String), ("2", "string")))


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
                returnValueRaw.append(self.resolve(funcEnv, self.semplify(funcEnv, fragment)))
                
            # execute replacement of special chars:
            #     
            theFormat = theFormat.replace("%n", "\n")\
                                    .replace("%r", "\r")\
                                    #.replace("%%", "%")
                
                
            # theFormat is a string
            returnValueRaw = theFormat%tuple(returnValueRaw)

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
        
        