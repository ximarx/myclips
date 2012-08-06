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


class Read(Function):
    '''
    The read function allows a user to input information for a single field. 
    All of the standard field rules (e.g., multiple symbols must be embedded within quotes) apply.
    
    (read [<logical-name>])

    where <logical-name> is an optional parameter. If specified, read tries to read 
    from whatever is attached to the logical file name. 
    If <logical-name> is t or is not specified, the function will read from stdin. 
    All the delimiters defined in section 2.3.1 can be used as delimiters. 
    The read function always returns a primitive data type. Spaces, carriage returns, 
    and tabs only act as delimiters and are not contained within the return value 
    (unless these characters are included within double quotes as part of a string). 
    If an end of file (EOF) is encountered while reading, read will return the symbol EOF. 
    If errors are encountered while reading, the string "*** READ ERROR ***" will be returned.
    
    WARNING: undocumented
    If EOF is found reading from stdin while parsing a <String> (before the end of the <String>)
    and InvalidArgValueError is raised 

    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.4.html#Heading247
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theName=None, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.4.html#Heading247
        """
        
        theName = self.resolve(theEnv, theName) if isinstance(theName, (types.FunctionCall, types.Variable)) else theName 
        
        if theName is None or (isinstance(theName, types.Symbol) and theName.pyEqual("t")):
            theResource = sys.stdin
            needSeek = False
        elif not isinstance(theName, types.Symbol):
            raise InvalidArgTypeError("Function read expected argument #1 to be of type symbol")
        else:
            theResource = theEnv.RESOURCES[theName.evaluate()]
            needSeek = True
            
        # get a ConstantParser: it will read 1 single Lexeme|Number from a string
        constantParser = theEnv.network.getParser().getSParser('ConstantParser')
        
        quoteGuard = None
        
        try:
        
            theString = theResource.readline()

            # python file.readline() doc:
            #    An empty string is returned only when EOF is encountered immediately
            #    @see http://docs.python.org/release/2.4.4/lib/bltin-file-objects.html
            if theString == "":
                return types.Symbol("EOF")

            quoteGuard = theString[0] == '"'

            if quoteGuard:
                # need to read a <String>
                while True:
                
                    theToken = constantParser.scanString(theString).next()
                    theResult = theToken[0][0]
                    
                    # check if the Result is a String
                    if isinstance(theResult, types.String):
                        # <String> found, continue
                        break
                    else:
                        # i've not found a string
                        # this means i've not read enoght to find
                        # the end quote for the string and the parser
                        # read a symbol instead
                        theOtherString = theResource.readline()
                        if theOtherString == "":
                            raise InvalidArgValueError("Encountered End-Of-File while scanning a string: %s"%theString)
                        theString += theOtherString
                
            else:
                # anything is ok
                # read only the first one
                theToken = constantParser.scanString(theString).next()
                theResult = theToken[0][0]
            
            
            if needSeek:
                # need to seek the resource read pointer
                # to the first not read char
                endPosition = theToken[2]
                theResource.seek(endPosition - len(theString) + 1, 1) # 1 == relative to the position
            
            return theResult
        
        except (StopIteration, EOFError):
            return types.Symbol("EOF")
        except IOError:
            return types.Symbol("*** READ ERROR ***")
        
    
Read.DEFINITION = FunctionDefinition("?SYSTEM?", "read", Read(), types.Symbol, Read.do,
            [
                Constraint_MaxArgsLength(1),
                Constraint_ArgType(types.Symbol, 0, failIfMissing=False)
            ],forward=False)
        
        
        
if __name__ == '__main__':
    
    import os
    from myclips.functions import FunctionEnv
    from myclips.rete.Network import Network
    n = Network()
    fr = open(os.path.dirname(__file__)+ "/read-test.txt", "rU")
    theEnv = FunctionEnv({}, n, n.modulesManager, {"t": sys.stdout, "fr": fr})
    r = Read()
    while True:
        s = r.do(theEnv, types.Symbol("fr"))
        print repr(s)
        if s.pyEqual("EOF"):
            break

    print repr(r.do(theEnv, types.Symbol("t")))
    