'''
Created on 11/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType,\
    Constraint_ExactArgsLength
from myclips.functions.Function import Function, InvalidArgTypeError
import myclips.parser.Types as types
import myclips


class _Length(Function):
    '''
    The length$ function returns an integer indicating the number of fields contained in a multifield value
    or a length of a string or symbol 
    If the argument passed to length$ is not the appropriate type, an exception is raised
    
    (length$ <symbol-string-multifield-expression>)
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.7.html#Heading295
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theMultifield, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.7.html#Heading295
        """
        
        theMultifield = self.semplify(theEnv, theMultifield, (list, types.Lexeme), ("1", "multifield, string or symbol"))
        
        return types.Integer(len(theMultifield) if isinstance(theMultifield, list) else len(self.resolve(theEnv, theMultifield)))


class Length(_Length):
    '''
    The length$ function returns an integer indicating the number of fields contained in a multifield value.
    If the argument passed to length$ is not the appropriate type, a negative one (-1) is returned
    
    (length$ <multifield-expression>)
    
    
    WARNING: the clips implementation of this function return the length
    or symbol and strings too (instead of -1)
    It's a alias for "length" in non-strict mode.
    In STRICT MODE this function acts as the documentation 
    (return -1 if arg is a multifield)
    
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.7.html#Heading295
    '''
    def __init__(self, *args, **kwargs):
        _Length.__init__(self, *args, **kwargs)
        
    def do(self, theEnv, theMultifield, *args, **kargs):
        if myclips.STRICT_MODE:
            try:
                theMultifield = self.semplify(theEnv, theMultifield, list)
                theLength = len(theMultifield)
            except InvalidArgTypeError:
                theLength = -1
            finally:
                return types.Integer(theLength)
        else:
            return _Length.do(self, theEnv, theMultifield, *args, **kargs)
    

_Length.DEFINITION = FunctionDefinition("?SYSTEM?", "length", _Length(), types.Integer, _Length.do,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType((list, types.Lexeme), 0),
            ],forward=False)        
    
Length.DEFINITION = FunctionDefinition("?SYSTEM?", "length$", Length(), types.Integer, Length.do,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType((list, types.Lexeme) if not myclips.STRICT_MODE else list, 0),
            ],forward=False)