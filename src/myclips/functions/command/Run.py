'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import Constraint_ArgType,\
    Constraint_MaxArgsLength, FunctionDefinition
import myclips.parser.Types as types
from myclips.functions.Function import Function, FunctionInternalError,\
    HaltException
from myclips.Agenda import AgendaNoMoreActivationError

class Run(Function):
    '''
    Refresh a rule status in the agenda
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theRuns=None, *args, **kargs):
        """
        function handler implementation
        """

        if theRuns is not None:
            theRuns = self.resolve(theEnv, self.semplify(theEnv, theRuns, types.Integer, ("1", "integer")))
        else:
            theRuns = True
            
        theEnv.network.run(theRuns)
        
#        try:
#            while theRuns:
#                #decrease theRuns if integer
#                if theRuns is not True:
#                    theRuns -= 1
#                    
#                try:
#                    pnode, token = theEnv.network.agenda.getActivation()
#                    pnode.execute(token)
##                    print '-----', pnode.mainRuleName
##                    for (salience, pnode, token) in theEnv.network.agenda.activations():
##                        print "%-6d %s: %s"%(salience, pnode.mainRuleName, token)
##                    print '---------'
#                    
#                except AgendaNoMoreActivationError:
#                    try:
#                        # try to pop the focusStack
#                        theEnv.network.agenda.focusStack.pop()
#                    except IndexError:
#                        # pop from an empty stack
#                        break
#            
#        except (FunctionInternalError, HaltException):
#            raise
            
        
        return types.NullValue()
    
    
Run.DEFINITION = FunctionDefinition("?SYSTEM?", "run", Run(), types.NullValue, Run.do ,
            [
                Constraint_MaxArgsLength(1),
                Constraint_ArgType(types.Integer, 0, False),
            ],forward=False)
        
        