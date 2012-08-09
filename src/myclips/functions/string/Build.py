'''
Created on 07/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType,\
    Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgTypeError
import myclips


class Build(Function):
    '''
    The build function evaluates the string as though it were entered at the command prompt.
    
    (build <string-or-symbol-expression>)

    where the only argument is the construct to be added. 
    The return value is TRUE if the construct was added (or FALSE if an error occurs).
    
    WARNING: undocumented!!
    defmodule/defrule with module/deffacts with module parsing doesn't change the
    scope of the current execution (so, after the construct execution, the scope is reverted
    to the old one of the rule that contains the build command)
    
    The scope changes only if the build command is executed from the shell directly
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading236
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theString, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.3.html#Heading236
        """

        theString = Build.resolve(theEnv, 
                                     Build.semplify(theEnv, theString, (types.String, types.Symbol), ("1", "string or symbol")))
        
        theScope = theEnv.modulesManager.currentScope.moduleName
        
        try:
            theFirstParsed = theEnv.network.getParser().getSParser("ConstructParser").scanString(theString).next()[0][0]
        except Exception, e:
            myclips.logger.warn("Build string parsing failed: %s", e)
            returnValue = types.Symbol("FALSE")
        else:
            try:
                if isinstance(theFirstParsed, types.DefRuleConstruct):
                    # add the new defrule
                    theEnv.network.addRule(theFirstParsed)
                elif isinstance(theFirstParsed, types.DefFactsConstruct):
                    theEnv.network.addDeffacts(theFirstParsed)
            except Exception, e:
                # an error? return FALSE
                print e
                returnValue = types.Symbol("FALSE")
            else:
                # construct added, return TRUE
                returnValue = types.Symbol("TRUE")
        finally:
            # BEFORE the end, the scope must be reverted to the original one
            # even if an exception was raised (deffacts and defrule names could trigger
            # a scope change)
            theEnv.modulesManager.changeCurrentScope(theScope)
            return returnValue
            
        
        
    
Build.DEFINITION = FunctionDefinition("?SYSTEM?", "build", Build(), types.Symbol, Build.do,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType((types.String, types.Symbol), 0),
            ],forward=False)
        
        