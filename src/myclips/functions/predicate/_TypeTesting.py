'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
import myclips.parser.Types as types
from myclips.functions.Function import Function

class _TypeTesting(Function):
    '''
    Check if a value is a specific type
    This class execute the same action of the isinstance function in python
    '''
    def __init__(self, cmpType=None, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        self._cmpType = cmpType if cmpType is not None else types.BaseParsedType
        
    def do(self, theEnv, theValue, *args, **kargs):
        """
        handler of the _TypeTesting function:
            execute the comparison
        """
        
        # check theValue type and resolve (if needed)
        if isinstance(theValue, (types.FunctionCall, types.Variable)):
            theValue = self.resolve(theEnv, theValue)
            
        if isinstance(theValue, self._cmpType): 
            returnValue = types.Symbol("TRUE")
        else:
            returnValue = types.Symbol("FALSE")
            
        # CLIPS documentation:
        # the if-then-else return value is always the value of the last execute action
        return returnValue


