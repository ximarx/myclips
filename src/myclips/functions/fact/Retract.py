'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_MinArgsLength
import myclips.parser.Types as types
from myclips.rete.WME import WME
from myclips.functions.Function import Function

class Retract(Function):
    '''
    Retract a wme from the working memory
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, funcEnv, *args, **kargs):
        """
        Retract function handler implementation
        """
        
        returnValue = types.Symbol("FALSE")
    
        for wme in args:
            
            # revolve variables, function calls, fact-id and fact-address 
            wme = Function.resolve(funcEnv, wme)
            
            if isinstance(wme, list):
                # wme was <Symbol:*>
                # the resolve gave me back a list of wme to retract
                for rWme in wme:
                    returnValue = funcEnv.network.retractFact(rWme)
                    
            else:
                returnValue = funcEnv.network.retractFact(wme)
            
        return returnValue
            
    @classmethod
    def resolve(cls, funcEnv, arg):
        """
        Override Function.resolve facts from args
        """
        if isinstance(arg, types.Integer):
            #convert the <Interger:INT> into a <WME:f-INT>
            return funcEnv.network.getWmeFromId(arg.evaluate())
        elif isinstance(arg, types.Symbol) and arg.evaluate() == "*":
            # if (retract *) format is used, i have to retract all
            # fact in working memory that this scope can see
            return funcEnv.network.factsForScope()
        else:
            # nested call to resolve have not to resolve the Int to WME
            # so i call the Function version of resolve
            # instead use the super receipt
            return Function.resolve(funcEnv, arg)
            
    
Retract.DEFINITION = FunctionDefinition("?SYSTEM?", "retract", Retract(), (WME, types.Symbol), Retract.do ,
            [
                Constraint_MinArgsLength(1),
            ],forward=False)
        
        