'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength
import myclips.parser.Types as types
from myclips.rete.WME import WME
from myclips.functions.Function import Function
from myclips.Fact import Fact

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
            fact = Assert.resolve(funcEnv, fact)
            
            returnValue = funcEnv.network.assertFact(fact)
            returnValue = returnValue[0] if returnValue[1] else types.Symbol("FALSE")
            
        return returnValue
            
            
    @classmethod
    def resolve(cls, theEnv, arg):
        if isinstance(arg, types.OrderedRhsPattern):
            # convert it in a new Ordered Fact
            return Fact([v if isinstance(v, types.BaseParsedType) # use the original value if it's a base type
                            else super(Assert, cls).resolve(theEnv, v) # otherwise try to solve it
                            for v in arg.values], templateName=None, moduleName=theEnv.modulesManager.currentScope.moduleName)
        elif isinstance(arg, types.TemplateRhsPattern):
            # convert it in a new Template Fact
            # the fact value is a dict with (slotName, slotValue) where slotValue:
                                # is the same of v if v is a base type
            return Fact(dict([(v.slotName, v.slotValue) if isinstance(v, types.SingleFieldRhsSlot) and isinstance(v.slotValue, types.BaseParsedType)
                                # is the evaluation of v if v is not a base type 
                                else (v.slotName, super(Assert, cls).resolve(theEnv, v.slotValue)) if isinstance(v, types.SingleFieldRhsSlot) and not isinstance(v.slotValue, types.BaseParsedType)
                                # is an array made by the inner values of v if base types
                                else (v.slotName, [vv if isinstance(vv.slotValue, types.BaseParsedType)
                                                        # or their evaluation if not 
                                                        else super(Assert, cls).resolve(theEnv, vv) for vv in v.slotValue]) if isinstance(v, types.MultiFieldRhsSlot)
                                else (v.slotName, v.slotValue)
                              for v in arg.templateSlots]),
                        templateName=arg.templateName, 
                        moduleName=theEnv.modulesManager.currentScope.templates.getDefinition(arg.templateName).moduleName)
        else:
            return super(Assert, cls).resolve(theEnv, arg)
            
    
Assert.DEFINITION = FunctionDefinition("?SYSTEM?", "assert", Assert(), (WME, types.Symbol), Assert.do ,
            [
                Constraint_MinArgsLength(1),
            ],forward=False)
        
        