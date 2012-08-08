'''
Created on 07/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType,\
    Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgValueError


class Explode(Function):
    '''
    This function constructs a multifield value from a string by using 
    each field in a string as a field in a new multifield value.

    (explode$ <string-expression>)

    A new multifield value is created in which each delimited field in 
    order in <string- expression> is taken to be a field in the new 
    multifield value which is returned. A string with no fields creates
    a multifield value of length zero. Fields other than symbols, 
    strings, integer, floats, or instances names 
    (such as parentheses or variables) are converted to strings.
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading222
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theString, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading222
        """

        
        theString = Function.resolve(theEnv, 
                                    Function.semplify(theEnv, theString, types.String, ("1", "string")))
        
        if theString.strip() == "":
            return [] # return an empty list
        
        # \" -> "
        theString.replace("\\\"", "\"")
        
        import pyparsing as pp
        
        constantParser = theEnv.network.getParser().getSParser("ConstantParser")
        variableParser = ((pp.Literal("$?") + theEnv.network.getParser().getSParser("VariableSymbolParser"))\
                                .setParseAction(lambda s,l,t: types.String("".join([str(x) for x in t.asList()])) )
                            | pp.Literal("$?")\
                                .setParseAction(lambda s,l,t: types.String("$?") )                                
                            | theEnv.network.getParser().getSParser("GlobalVariableParser").copy()\
                                .setParseAction(lambda s,l,t: types.String("".join([str(x) for x in t.asList()])) )
                            | (pp.Literal("?") + theEnv.network.getParser().getSParser("VariableSymbolParser"))\
                                .setParseAction(lambda s,l,t: types.String("".join([str(x) for x in t.asList()])) )
                            | pp.Literal("?")\
                                .setParseAction(lambda s,l,t: types.String("?") )                                
                        ).setParseAction(lambda s,l,t: t.asList())
        
        trapParser = pp.SkipTo(constantParser | variableParser).setParseAction(lambda s,l,t: types.String(t[0].strip()) )
        wrapperParser = pp.ZeroOrMore( variableParser
                            | constantParser
                            | trapParser ).setParseAction(lambda s,l,t: t.asList())
                            
        return wrapperParser.parseString(theString, True).asList()
        
    
Explode.DEFINITION = FunctionDefinition("?SYSTEM?", "explode$", Explode(), list, Explode.do,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType(types.String, 0)
            ],forward=False)


if __name__ == '__main__':
    
    from myclips.functions import FunctionEnv
    from myclips.rete.Network import Network
    
    n = Network()
    fe = FunctionEnv({}, n, n.modulesManager, {})
    
    f = Explode()
    
    import pprint
    pprint.pprint(f.do(fe, types.String("ciao $?$f 12 \"clbl\" ?*ijo* esterno ? ( interno1 interno2) $? ?ioew $?fepwjf ?$of ")))
    
    
    
    