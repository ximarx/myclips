'''
Created on 07/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType,\
    Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgTypeError
from myclips.rete.WME import WME
import myclips


class Eval(Function):
    '''
    The eval function evaluates the string as though it were entered at the command prompt.
    
    (eval <string-or-symbol-expression>)

    where the only argument is the command, constant, or global variable to be executed. 
    NOTE: eval does not permit the use of local variables 
    (except when the local variables are defined as part of the command such as with an instance query function), 
    nor will it evaluate any of the construct definition forms 
    (i.e., defrule, deffacts, etc.). 
    The return value is the result of the evaluation of the string (or FALSE if an error occurs).
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading234
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theString, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading234
        """
        
        # normalize theString
        if isinstance(theString, (types.Variable, types.FunctionCall)):
            theString = self.resolve(theEnv, theString)
        if isinstance(theString, types.String):
            theString = theString.evaluate()[1:-1]
        elif isinstance(theString, types.Symbol):
            theString = theString.evaluate()
        else:
            raise InvalidArgTypeError("Function eval expected argument #1 to be of type string or symbol")
        
        
        try:
            theFirstParsed = theEnv.network.getParser().getSParser("ActionParser").parseString(theString).asList()[0]
        except Exception, e:
            myclips.logger.warn("Eval string parsing failed: %s", e)
            return types.Symbol("FALSE")
        else:
            if isinstance(theFirstParsed, types.FunctionCall):
                # create a new funcEnv without the variables
                from myclips.functions import FunctionEnv
                tmpEnv = FunctionEnv({}, theEnv.network, theEnv.modulesManager, theEnv.RESOURCES)
                return self.resolve(tmpEnv, theFirstParsed)
            elif isinstance(theFirstParsed, (types.SingleFieldVariable, types.MultiFieldVariable)):
                myclips.logger.warn("Eval command execution returned a variable: %s", theFirstParsed)
                return types.Symbol("FALSE")
            elif isinstance(theFirstParsed, (types.BaseParsedType, WME, list)):
                return theFirstParsed
            else:
                myclips.logger.error("Unexpected return value from the eval string command parsing: %s", theFirstParsed)
                return types.Symbol("FALSE")
                
        
        
    
Eval.DEFINITION = FunctionDefinition("?SYSTEM?", "eval", Eval(), (types.Integer, types.Float, types.Number,
                                                                  types.String, types.Symbol, types.Lexeme,
                                                                  types.NullValue, list, WME), Eval.do,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType((types.String, types.Symbol), 0),
            ],forward=False)
        
        