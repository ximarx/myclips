'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_MaxArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.functions.Function import Function

class Agenda(Function):
    '''
    Displays all activations on the agenda. This function has no return value.

    (agenda [<module-name>])

    If <module-name> is unspecified, then all activations in the current module (not the current focus) are displayed. 
    If <module-name> is specified, then all activations on the agenda of the specified module are displayed. 
    If <module-name> is the symbol *, then the activations on all agendas in all modules are displayed.
    
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
        
        