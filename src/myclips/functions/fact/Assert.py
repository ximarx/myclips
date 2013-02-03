'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength
import myclips.parser.Types as types
from myclips.rete.WME import WME
from myclips.functions.Function import Function, InvalidArgValueError
from myclips.facts.OrderedFact import OrderedFact
from myclips.facts.TemplateFact import TemplateFact

class Assert(Function):
    '''
    Assert new fact in the working memory
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, funcEnv, *args, **kargs):
        """
        handler of the Assert function:
            assert new fact in the network working memory
        """
        
        returnValue = types.Symbol("FALSE")
    
        for fact in args:
            
            # revolve variables and function calls
            fact = self.createFact(funcEnv, fact)
            
            returnValue = funcEnv.network.assertFact(fact)
            returnValue = returnValue[0] if returnValue[1] else types.Symbol("FALSE")
            
        return returnValue
            
            
    def createFact(self, theEnv, arg):
        if isinstance(arg, types.OrderedRhsPattern):
            
            return OrderedFact(values=[self.semplify(theEnv, v) # resolve to BaseParsedTypes if needed
                            for v in arg.values], moduleName=theEnv.modulesManager.currentScope.moduleName)
            
        elif isinstance(arg, types.TemplateRhsPattern):
            # convert it in a new Template Fact
            # the fact value is a dict with (slotName, slotValue) where slotValue
                                # need to be resolved
                                
            return TemplateFact(templateName=arg.templateName, 
                                values=dict([(v.slotName, self.semplify(theEnv, v.slotValue))
                                             for v in arg.templateSlots]), 
                                moduleName=theEnv.modulesManager.currentScope.templates.getDefinition(arg.templateName).moduleName)
                                
        else:
            raise InvalidArgValueError("Invalid fact format")
            
    
Assert.DEFINITION = FunctionDefinition("?SYSTEM?", "assert", Assert(), (WME, types.Symbol), Assert.do ,
            [
                Constraint_MinArgsLength(1),
            ],forward=False)
        
        