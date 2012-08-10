'''
Created on 10/ago/2012

@author: Francesco Capozzo
'''
from myclips.functions.Function import Function, ReturnException, BreakException,\
    FunctionImplError, FunctionInternalError, HaltException
import myclips.parser.Types as types 
from myclips.functions import FunctionEnv
from myclips.MyClipsException import MyClipsException
import traceback

class UserFunction(Function):
    '''
    Custom function to allow runtime user function definition
    as a list of defined functions
    '''

    def __init__(self, theParams, theActions, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        self._actions = theActions if isinstance(theActions, list) else []
        self._params = theParams if isinstance(theParams, list) else []
        
    def do(self, theEnv, *args, **kwargs):
        
        # 1) read params informations and resolve the values from the *args list
        
        theBindings = {}
        for index, theParam in enumerate(self._params):
            if isinstance(theParam, types.SingleFieldVariable):
                theBindings[theParam.evaluate()] = self.semplify(theEnv, args[index])
            elif isinstance(theParam, types.MultiFieldVariable):
                theBindings[theParam.evaluate()] = [self.semplify(theEnv, x) for x in args[index:None]]
                # it's useless to iterate more, 
                # the only multifield variable allowed must be the last
                # params. So, even if other params are available in the _params
                # they have to be ignored because are illegal
                break
        
        # 2) create a theEnv copy with new bindings
        
        theNewEnv = FunctionEnv(theBindings, theEnv.network, theEnv.modulesManager, theEnv.RESOURCES)
        
        returnValue = types.Symbol("FALSE")
        
        # 3) execute the list of actions
        # to do this, i could use semplify. This whay i always got back the
        # types.Class value form, not the python one
        for theAction in self._actions:
            # theAction is a function call or a variable. In both
            # cases the returnValue of semplify is a types.BaseParsedType instance
            returnValue = self.semplify(theNewEnv, theAction)
            
        
        # 4) return the last action return value!
        return returnValue
    
    
    @classmethod
    def execute(cls, theFunction, theEnv, *args, **kargs):
        """
        Execute a function handler with correct parameters
        This execution protocol override the Function.execute one
        to use the function instance, not its class to call the handler
        (that for UserFunction is static: do)
        
        @raise FunctionImplError: forward exception from function handler implementation
        @raise FunctionInternalError: wrap a non FunctionImplError exception in a FunctionInternalError
                to hide function internal processing. Original exception is available in 
                FunctionInternalError.args[1]. Original exception repr() is used as
                wrapper exception's message
        @return: forward handler return
        @rtype: mixed (based on FunctionDefinition.returnTypes)
        """
        
        try:
            return theFunction.do(theEnv, *args, **kargs)
        except (ReturnException, BreakException, HaltException):
            # break the execution until a catch get it
            raise
        except FunctionImplError:
            raise
        except MyClipsException, e:
            raise FunctionInternalError(str(cls)+": "+e.message, e, traceback.format_exc())
        except Exception, e:
            # wrap python standards exception
            # in functions exception
            raise FunctionInternalError(str(e), e, traceback.format_exc())
