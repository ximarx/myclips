'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ExactArgsLength,\
    Constraint_MaxArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.functions.Function import Function
import sys

class Agenda(Function):
    '''
    Displays facts stored in the fact-list.
    
    (facts [<module-name>] [<start-integer-expression> [<end-integer-expression> [<max-integer-expression>]]])

    If <module-name> is not specified, then only facts visible to the current module will be displayed. 
    If <module-name> is specified, then only facts visible to the specified module are displayed. 
    If the symbol * is used for <module-name>, then facts from any module may be displayed. 
    If the start argument is specified, only facts with fact-indices greater than or equal to this argument are displayed. 
    If the end argument is specified, only facts with fact-indices less than or equal to this argument are displayed. 
    If the max argument is specified, then no facts will be displayed beyond the specified maximum number of facts to be displayed. 
    This function has no return value.
    
    WARNING:
    
    RESOURCES[wdisplay] is used for output
        
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theModule=None, *args, **kargs):
        """
        function handler implementation
        """
        if theModule is not None:
            theModule = self.resolve(theEnv, self.semplify(theEnv, theModule, types.Symbol, ("1", "symbol")))

        theModules = [theModule] if theModule != '*' else theEnv.modulesManager.getModulesNames()
        
        actCount = 0
        
        theStdout = theEnv.RESOURCES['wdisplay']
        
        if len(theModules) > 1 :
        
            for theModule in theModules:
                theStdout.write("%s:\n"%theModule)
                acts = theEnv.network.agenda.activations(theModule)
                actCount += len(acts)
                for (salience, pnode, token) in acts:
                    theStdout.write("\t%-6d %s: %s\n"%(salience, pnode.mainRuleName, token))
        
        else:
            acts = theEnv.network.agenda.activations(theModule)
            actCount += len(acts)
            for (salience, pnode, token) in acts:
                theStdout.write("%-6d %s: %s\n"%(salience, pnode.mainRuleName, token))
        
            
        if actCount:
            theStdout.write("For a total of %d activations.\n"%actCount)
        
        
        return types.NullValue()
    
    
Agenda.DEFINITION = FunctionDefinition("?SYSTEM?", "agenda", Agenda(), types.NullValue, Agenda.do ,
            [
                Constraint_MaxArgsLength(1),
                Constraint_ArgType(types.Symbol, 0, False),
            ],forward=False)
        
        