'''
Created on 12/ago/2012

@author: Francesco Capozzo
'''

import pyparsing as pp
import myclips.parser.Types as types
from myclips.functions import FunctionEnv

class Interpreter(object):
    '''
    classdocs
    '''


    def __init__(self, aNetwork=None, aShell=None):
        '''
        Constructor
        '''
        self._network = aNetwork
        self._shell = aShell
        self._internalParser = None
        
    def setNetwork(self, network):
        self._network = network
        
    def setShell(self, shell):
        self._shell = shell
    
    @property
    def parser(self):
        if self._internalParser is None:
            aConstruct = self._network.getParser().getSParser('ConstructParser')
            aFunction = self._network.getParser().getSParser('FunctionCallParser')
            aConstant = self._network.getParser().getSParser('ConstantParser')
            aGlobalVar = self._network.getParser().getSParser('GlobalVariableParser')
            
            self._internalParser = (aConstant
                                    | aGlobalVar
                                    | aFunction
                                    | aConstruct).setParseAction(lambda s,l,t:t.asList()[0])
                                    
        return self._internalParser
    
    
    
    def evaluate(self, aString):
        
        try:
            parsed = self.parser.parseString(aString, True)[0]
        except pp.ParseBaseException, e:
            if self._network.getParser()._lastParseError != None and e.msg != self._network.getParser()._lastParseError:
                raise pp.ParseFatalException(e.pstr,
                                             e.loc,
                                             e.msg + ". Possible cause: " + self._network.getParser()._lastParseError )
            else:
                raise
            
        else:
        
            if isinstance(parsed, types.DefRuleConstruct):
                # add the new rule to the network
                self._network.addRule(parsed)
                
            elif isinstance(parsed, types.DefFactsConstruct):
                # add the deffacts
                self._network.addDeffacts(parsed)
                
            elif isinstance(parsed, types.FunctionCall):
                # execute the function
                assert isinstance(parsed, types.FunctionCall)
                
                # prepare the FunctionEnv object    
                theEnv = FunctionEnv({}, self._network, self._network.modulesManager, self._network.resources)
                funcDefinition = parsed.funcDefinition
                
                theResult = funcDefinition.linkedType.__class__.execute(funcDefinition.linkedType, theEnv, *(parsed.funcArgs))
                if not isinstance(theResult, types.NullValue):
                    return theResult
            
            elif isinstance(parsed, types.GlobalVariable):
                # resolve the global value
                
                return self._network.modulesManager.currentScope.globalsvars.getDefinition(parsed.evaluate()).linkedType.runningValue
                
            elif isinstance(parsed, types.BaseParsedType):
                
                return parsed
        
        