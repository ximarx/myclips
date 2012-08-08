'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength, Constraint_ArgType
import myclips.parser.Types as types
from myclips.rete.WME import WME
from myclips.functions.Function import Function, InvalidArgValueError

class Modify(Function):
    '''
    The modify action allows the user to modify template facts on the fact-list. 
    Only one fact may be modified with a single modify statement. 
    The modification of a fact is equivalent to retracting the present fact and asserting the modified fact.
    
    (modify <fact-specifier> <RHS-slot>*)
    
    The term <fact- specifier> includes variables bound on the LHS to fact-addresses or the fact-index of the desired fact 
    (e.g. 3 for the fact labeled f-3). 
    Note that the fact-index generally is not known during the execution of a program, 
    so facts usually are modified by binding them on the LHS of a rule.
    Static deftemplate checking is not performed when a fact-index is used as the <fact-specifier> 
    since the deftemplate being referenced is usually ambiguous. 
    Only variables or fact indices may be used in a modify. [...] 
    The value returned by this function is the fact-address of the newly modified fact. 
    If the assertion of the newly modified fact causes an error, 
    or if an identical copy of the newly modified fact already exists in the fact-list,
    then the symbol FALSE is returned.
    
    @see http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.9.html#Heading303 
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theFact, *args, **kargs):
        """
        Function handler implementation
        @see http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.9.html#Heading303
        """
        
        # 1) resolve the theFact to a WME
        theFact = Modify.resolveFact(theEnv, Modify.semplify(theEnv, theFact, (WME, types.Integer), ('1', "fact-address or integer" )))
        
        # 2) check if it's a template fact
        if not theFact.fact.isTemplateFact():
            raise InvalidArgValueError("")
        
        # 3) get a copy of the fact inside the wme
        theBackup = theFact.fact
        
        # 4) retract the wme
        theEnv.network.retractFact(theFact)
        
        del theFact
        
        # 5) modify the fact with the new values for the slots:
        
        for theSlot in args:
            # each arg is a types.OrderedRhsQualcosa: index 0 is the slot name, then values
            assert isinstance(theSlot, types.OrderedRhsPattern)
            theSlotName = Function.resolve(theEnv, 
                                           Function.semplify(theEnv, theSlot.values[0], types.Symbol))
            
            if len(theSlot.values) > 2:
                # it's a multifield
                theSlotValues = Function.semplify(theEnv, theSlot.values[1:None])
            else:
                # it's a single field
                theSlotValues = Function.semplify(theEnv, theSlot.values[1])
                
            theBackup[theSlotName] = theSlotValues
            
        # 6) assert the new fact
        
        theWme, isNew = theEnv.network.assertFact(theBackup)
            
        return theWme if isNew else types.Symbol("FALSE")
            
    @classmethod
    def resolveFact(cls, theEnv, arg):
        """
        Override Function.resolve facts from args
        """
        if isinstance(arg, types.Integer):
            #convert the <Interger:INT> into a <WME:f-INT>
            return theEnv.network.getWmeFromId(arg.evaluate())
        else:
            return arg
            
    
Modify.DEFINITION = FunctionDefinition("?SYSTEM?", "modify", Modify(), (WME, types.Symbol), Modify.do ,
            [
                Constraint_MinArgsLength(1),
                Constraint_ArgType((types.Integer, WME), 0),
                Constraint_ArgType(types.OrderedRhsPattern, (1,None), failIfMissing=False),
            ],forward=False)
        
        