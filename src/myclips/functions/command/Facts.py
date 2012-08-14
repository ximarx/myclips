'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ExactArgsLength,\
    Constraint_MaxArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.functions.Function import Function
import sys

class Facts(Function):
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
        
        
    def do(self, theEnv, *args, **kargs):
        """
        function handler implementation
        """
        
        argsLen = len(args)

        if argsLen == 4:
            # 0 = theModule, 1 = theStart, 2 = theEnd, 3 = theMax
            theModules = self.resolve(theEnv, self.semplify(theEnv, args[0], types.Symbol, ("1", "symbol or * (in a 4 args configuration)")))
            theStart = self.resolve(theEnv, self.semplify(theEnv, args[1], types.Integer, ("2", "integer (in a 4 args configuration)")))
            theEnd = self.resolve(theEnv, self.semplify(theEnv, args[2], types.Integer, ("3", "integer (in a 4 args configuration)")))
            theMax = self.resolve(theEnv, self.semplify(theEnv, args[3], types.Integer, ("4", "integer (in a 4 args configuration)")))
            
        elif argsLen == 3:
            # 0 = theModule, 1 = theStart, 2 = theEnd
            # or
            # 0 = theStart, 1 = theEnd, 2 = theMax
            theFirst = self.semplify(theEnv, args[0], (types.Integer, types.Symbol), ("1", "integer, symbol or * (in a 3 args configuration)"))
            if isinstance(theFirst, types.Symbol):
                # first case
                theModules = self.resolve(theEnv, theFirst)
                theStart = self.resolve(theEnv, self.semplify(theEnv, args[1], types.Integer, ("2", "integer (in a 3 args configuration)")))
                theEnd = self.resolve(theEnv, self.semplify(theEnv, args[2], types.Integer, ("3", "integer (in a 3 args configuration)")))
                theMax = None
            else:
                theModules = theEnv.modulesManager.currentScope.moduleName
                theStart = self.resolve(theEnv, theFirst)
                theEnd = self.resolve(theEnv, self.semplify(theEnv, args[1], types.Integer, ("2", "integer (in a 3 args configuration)")))
                theMax = self.resolve(theEnv, self.semplify(theEnv, args[2], types.Integer, ("3", "integer (in a 3 args configuration)")))
                
        elif argsLen == 2:
            # 0 = theModule, 1 = theStart
            # or
            # 0 = theStart, 1 = theEnd
            theFirst = self.semplify(theEnv, args[0], (types.Integer, types.Symbol), ("1", "integer, symbol or * (in a 2 args configuration)"))
            if isinstance(theFirst, types.Symbol):
                # first case
                theModules = self.resolve(theEnv, theFirst)
                theStart = self.resolve(theEnv, self.semplify(theEnv, args[1], types.Integer, ("2", "integer (in a 2 args configuration)")))
                theEnd = sys.maxint
                theMax = None
            else:
                theModules = theEnv.modulesManager.currentScope.moduleName
                theStart = self.resolve(theEnv, theFirst)
                theEnd = self.resolve(theEnv, self.semplify(theEnv, args[1], types.Integer, ("2", "integer (in a 2 args configuration)")))
                theMax = None

        elif argsLen == 1:
            # 0 = theModule
            # or
            # 0 = theStart
            theFirst = self.semplify(theEnv, args[0], (types.Integer, types.Symbol), ("1", "integer, symbol or * (in a 1 args configuration)"))
            if isinstance(theFirst, types.Symbol):
                # first case
                theModules = self.resolve(theEnv, theFirst)
                theStart = 0
                theEnd = sys.maxint
                theMax = None
            else:
                theModules = theEnv.modulesManager.currentScope.moduleName
                theStart = self.resolve(theEnv, theFirst)
                theEnd = sys.maxint
                theMax = None
                
        else:
            # only show the current modules fact, without filters about fact-id
            theModules = theEnv.modulesManager.currentScope.moduleName
            theStart = 0
            theEnd = sys.maxint
            theMax = None

        #normalize theModules
        theModules = [] if theModules == "*" else [theModules]

        theFacts = []
        if len(theModules) > 0:
            for theModule in theModules:
                theFacts += theEnv.network.factsForScope(theModule)
        else:
            theFacts = theEnv.network.facts


        # filter and cut the wme list to display
        theFacts = [wme for wme in theFacts if wme.factId >= theStart and wme.factId <= theEnd][:theMax] 
        
        if len(theFacts):

            theStdout = theEnv.RESOURCES['wdisplay']
                    
            for wme in theFacts:
                theStdout.write("f-%-5d %s\n"%(wme.factId, wme.fact))
            
            theStdout.write("For a total of %d facts.\n"%len(theFacts))
        
        return types.NullValue()
    
    
Facts.DEFINITION = FunctionDefinition("?SYSTEM?", "facts", Facts(), types.NullValue, Facts.do ,
            [
                Constraint_MaxArgsLength(4),
                Constraint_ArgType((types.Symbol, types.Integer), 0, False),
                Constraint_ArgType(types.Integer, (1,None), False)
            ],forward=False)
        
        