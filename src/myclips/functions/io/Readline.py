'''
Created on 06/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType, \
    Constraint_MaxArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgTypeError,\
    InvalidArgValueError
import sys


class Readline(Function):
    '''
    The readline function is similar to the read function, 
    but it allows a whole string to be input instead of a single field. 
    Normally, read will stop when it encounters a delimiter. 
    The readline function only stops when it encounters a carriage return,
    a semicolon, or an EOF. 
    Any tabs or spaces in the input are returned by readline as a part of the string. 
    The readline function returns a string.
    
    (readline [<logical-name>])

    where <logical- name> is an optional parameter. 
    If specified, readline tries to read from whatever is attached to the logical file name. 
    If <logical- name> is t or is not specified, 
    the function will read from stdin. 
    As with the read function, if an EOF is encountered, 
    readline will return the symbol EOF. 
    If an error is encountered during input, readline returns the string "*** READ ERROR ***"

    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.4.html#Heading248
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theName=None, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.4.html#Heading248
        """
        
        theName = self.resolve(theEnv, theName) if isinstance(theName, (types.FunctionCall, types.Variable)) else theName 
        
        if theName is None or (isinstance(theName, types.Symbol) and theName.pyEqual("t")):
            theResource = sys.stdin
        elif not isinstance(theName, types.Symbol):
            raise InvalidArgTypeError("Function read expected argument #1 to be of type symbol")
        else:
            theResource = theEnv.RESOURCES[theName.evaluate()]
        
        try:
        
            theString = theResource.readline()

            # python file.readline() doc:
            #    An empty string is returned only when EOF is encountered immediately
            #    @see http://docs.python.org/release/2.4.4/lib/bltin-file-objects.html
            if theString == "":
                return types.Symbol("EOF")

            return types.String(theString)
        
        except EOFError:
            return types.Symbol("EOF")
        except IOError:
            return types.Symbol("*** READ ERROR ***")
        
    
Readline.DEFINITION = FunctionDefinition("?SYSTEM?", "readline", Readline(), types.String, Readline.do,
            [
                Constraint_MaxArgsLength(1),
                Constraint_ArgType(types.Symbol, 0, failIfMissing=False)
            ],forward=False)
        
        
