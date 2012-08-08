'''
Created on 08/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength, Constraint_ExactArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.rete.WME import WME
from myclips.functions.Function import Function, InvalidArgValueError
from myclips.Fact import Fact

class AssertString(Function):
    '''
    The assert-string function is similar to assert 
    in that it will add a fact to the fact-list. 
    However, assert-string takes a single string representing a fact 
    (expressed in either ordered or deftemplate format ) 
    and asserts it. Only one fact may be asserted with each assert-string statement.
    
    @see http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.9.html#Heading305 
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theString, *args, **kargs):
        """
        Function handler implementation
        
        @see http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.9.html#Heading305
        """
        
        theString = Function.resolve(theEnv, 
                                     Function.semplify(theEnv, theString, types.String, ("1", "string")))
        
        try:
            theRhsPattern = theEnv.network.getParser().getSParser("RhsPatternParser").parseString(theString).asList()[0]
        except IndexError:
            return types.Symbol("FALSE")
        else:
            theFact = AssertString.createFact(theEnv, theRhsPattern)
            theWme, isNew = theEnv.network.assertFact(theFact)
            return theWme if isNew else types.Symbol("FALSE")
            
    
            
            
    @classmethod
    def createFact(cls, theEnv, arg):
        if isinstance(arg, types.OrderedRhsPattern):
            # convert it in a new Ordered Fact
            return Fact([Function.semplify(theEnv, v, types.BaseParsedType) for v in arg.values], templateName=None, moduleName=theEnv.modulesManager.currentScope.moduleName)
        elif isinstance(arg, types.TemplateRhsPattern):
            # convert it in a new Template Fact
            # the fact value is a dict with (slotName, slotValue) where slotValue:
                                # is a baseparsedtype if singlefield
            return Fact(dict([(v.slotName, Function.semplify(theEnv, v.slotValue, types.BaseParsedType)) if isinstance(v, types.SingleFieldRhsSlot)
                                # or a list if multifield (solved, this means is a list of base-parsed-type)
                                else (v.slotName, Function.semplify(theEnv, v.slotValue, list)) if isinstance(v, types.MultiFieldRhsSlot)
                                    else (v.slotName, v.slotValue) #don't know what to do FIXME
                              for v in arg.templateSlots]),
                        templateName=arg.templateName, 
                        moduleName=theEnv.modulesManager.currentScope.templates.getDefinition(arg.templateName).moduleName)
        else:
            raise InvalidArgValueError("Unknown fact format in RHS pattern")
            
    
AssertString.DEFINITION = FunctionDefinition("?SYSTEM?", "assert-string", AssertString(), (WME, types.Symbol), AssertString.do ,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType(types.String, 0)
            ],forward=False)
        
        