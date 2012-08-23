'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ExactArgsLength,\
    Constraint_ArgType
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgValueError
from genericpath import exists
import os

class Load(Function):
    '''
    Load all construct in a file
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, aPath, *args, **kargs):
        """
        function handler implementation
        """

        aPath = self.resolve(theEnv, 
                             self.semplify(theEnv, aPath, types.Lexeme, ('1', 'symbol or string')))
        
        aPath = os.path.abspath(aPath)
        
        if not exists(aPath):
            raise InvalidArgValueError("Function load was unable to open file %s"%aPath)
        
        aFile = open(aPath, 'rU')
        aString = aFile.read()

        try:
            parsed = theEnv.network.getParser().parse(aString, extended=True)
        except Exception, e:
            print >> theEnv.RESOURCES['werror'], theEnv.network.getParser().ExceptionPPrint(e, aString)
            return types.Symbol('FALSE')
        else:
            cString = ""
            for p in parsed:
                if isinstance(p, types.DefRuleConstruct):
                    cString += "*"
                    theEnv.network.addRule(p)
                elif isinstance(p, types.DefFactsConstruct):
                    cString += "$"
                    theEnv.network.addDeffacts(p)
                elif isinstance(p, types.DefTemplateConstruct):
                    cString += "%"
                elif isinstance(p, types.DefGlobalConstruct):
                    cString += ":"
                elif isinstance(p, types.DefFunctionConstruct):
                    cString += "!"
                    
            print >> theEnv.RESOURCES['wtrace'], cString
                    
            return types.Symbol('TRUE')
    
    
Load.DEFINITION = FunctionDefinition("?SYSTEM?", "load", Load(), types.Symbol, Load.do ,
            [
                Constraint_ExactArgsLength(1),
                Constraint_ArgType((types.Symbol, types.String), 0)
            ],forward=False)
        
        