'''
Created on 06/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType, \
    Constraint_MinArgsLength, Constraint_MaxArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgTypeError,\
    InvalidArgValueError
from myclips.functions import FunctionEnv


class Open(Function):
    '''
    The open function allows a user to open a file from the RHS 
    of a rule and attaches a logical name to it. 
    This function takes three arguments: 
        (1) the name of the file to be opened; 
        (2) the logical name which will be used by other CLIPS I/O functions to access the file; 
        and (3) an optional mode specifier.
    The mode specifier must be one of the following strings:
        <String:"r">: read only access
        <String:"r+">: read and write access
        <String:"w">: write only
        <String:"a">: append only
        
    (open <file-name> <logical-name> [<mode>])
    
    The <file-name> must either be a string or symbol and may include directory specifiers. 
    If a string is used, the backslash (\) and any other special characters that 
    are part of <file-name> must be escaped with a backslash. 
    The logical name should not have been used previously. 
    The open function returns <Symbol:TRUE> if it was successful, otherwise <Symbol:FALSE>.        
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.4.html#Heading244
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, thePath, theName, theMode=None, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.4.html#Heading244
        """
        
        thePath = self.resolve(theEnv, thePath) if isinstance(thePath, (types.FunctionCall, types.Variable)) else thePath
        theName = self.resolve(theEnv, theName) if isinstance(theName, (types.FunctionCall, types.Variable)) else theName 
        theMode = self.resolve(theEnv, theMode) if isinstance(theMode, (types.FunctionCall, types.Variable)) \
                    else theMode if theMode is not None else types.String("r")
        
        if not isinstance(thePath, (types.String, types.Symbol)):
            raise InvalidArgTypeError("Function open expected argument #1 to be of type string or symbol")
        
        # normalize the string to a path. In documentation:
        # all special chars and \ in the path must be escaped
        # these means that the path is already a valid path
        # for python
        thePath = thePath.evaluate() if isinstance(thePath, types.Symbol) else thePath.evaluate()[1:-1]
        
        if not isinstance(theName, types.Symbol):
            raise InvalidArgTypeError("Function open expected argument #2 to be of type symbol")
         
        # check if a resource with the same logical name is already used
        assert isinstance(theEnv, FunctionEnv)
        if theEnv.RESOURCES.has_key(theName.evaluate()):
            raise InvalidArgValueError("Illegal logical name used for open function: %s"%theName.evaluate())
            
        if not isinstance(theMode, types.String):
            raise InvalidArgTypeError("Function open expected argument #3 to be of type string")
        
        # normalize the mode removing quotes if <String>
        theMode = theMode.evaluate()[1:-1]
        
        modeMap = {"r": "rU",
                   "r+": "rU+",
                   "w": "w",
                   "a": "a"}
        
        import myclips
        try:
            theMode = modeMap[theMode]
            fileResource = open(thePath, theMode)
            theEnv.RESOURCES[theName.evaluate()] = fileResource
            return types.Symbol("TRUE")
        except KeyError:
            myclips.logger.error("Invalid mode for Open: %s", theMode)
            return types.Symbol("FALSE")
        except IOError, e:
            myclips.logger.error("IOError in Open: %s", e)
            return types.Symbol("FALSE")
            
            
    
Open.DEFINITION = FunctionDefinition("?SYSTEM?", "open", Open(), types.Symbol, Open.do,
            [
                Constraint_MinArgsLength(2),
                Constraint_MaxArgsLength(3),
                Constraint_ArgType((types.Symbol, types.String), 0),
                Constraint_ArgType(types.Symbol, 1),
                Constraint_ArgType(types.String, 2, failIfMissing=False)
            ],forward=False)
        
        