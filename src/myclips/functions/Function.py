'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''

        
class Function(object):
    '''
    Base abstract class for system function definition
    '''
    
    # @type DEFINITION: myclips.FunctionsManager.FunctionDefinition.FunctionDefinition
    DEFINITION = None
    
    def __init__(self, *args, **kwargs):
        object.__init__(self, *args, **kwargs)

    @classmethod
    def execute(cls, functionEnv, *args, **kargs):
        #instance = cls(functionEnv)
        return cls.DEFINITION.handler(functionEnv, *args, **kargs)
        
    def definition(self):
        """
        Get the system function FunctionDefinition
        """
        return self.__class__.DEFINITION
    
    @staticmethod
    def resolve(funcEnv, arg):
        pass
