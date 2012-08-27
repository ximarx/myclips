'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.tests.BetaTest import BetaTest
import myclips
from myclips.rete.tests import getTokenAnchestor
import myclips.parser.Types as types

class DynamicFunctionTest(BetaTest):
    '''
    the test is satisfied if the function call 
    evaluates to a non- <Symbol:FALSE> value 
    and unsatisfied if the function call evaluates to <Symbol:FALSE>
    '''


    def __init__(self, aFunctionCall, aFakeVariablesMap):
        '''
        Create a new DynamicFunctionTest. This test make sure
        the function return value (with variables bindings
        information provided by reference) is not <Symbol:FALSE>
        
        @param aFunctionCall: is the dynamic function
        @type aFunctionCall: types.FunctionCall
        @param aFakeVariablesMap: is a map of fakeVariablesName => relativeVariableLocation to a previous found variable
        @type aFakeVariablesMap: dict
        @return: False if test fail, True otherwise
        @rtype: Boolean  
        '''
        
        self._references = aFakeVariablesMap
        self._function = aFunctionCall
        
        
    @property
    def references(self):
        return self._references
    
    @property
    def function(self):
        return self._function
    
    def isValid(self, token, wme):
        '''
        Evaluate the token and check if constraints are valid
        
        @param token: a token
        @type token: Token
        @param wme: NONE! Test-CE tests are not performed with a wme from right
        @type wme: None
        '''

        try:
            
            # replace all fake variables with their real values
            # from the token
            
            varValues = {}
            
            for fakeName, reference in self.references.items():
            
                # if token relative index is 0, then the test is an intra-element
                # test performed in the beta network
                # this means that the wme where the variable was found first
                # is the same where the variable was found again
                if reference.relPatternIndex != 0:
                    token = getTokenAnchestor(token, (-1 * reference.relPatternIndex) - 1)
        
                    # get the exact wme value of the token where variable for used first
                    valueInTokenWme = reference.reference.toValue(token.wme)
                else:
                    valueInTokenWme = reference.reference.toValue(wme)
                
                # get the value in current wme there variable must have the same value
                varValues[fakeName] = valueInTokenWme
                
            # create a new FunctionEnv for function execution
            # network, modulesManager and RESOURCES are not valid values
            # because all functions that use knoledge about the network configuration
            # have to raise exception if called
            
            from myclips.functions import FunctionEnv
        
            theEnv = FunctionEnv(varValues, None, None, None)
            
            # execute the function and get back the result
            
            theReturnValue = self.function.funcDefinition.linkedType.__class__.execute(self.function.funcDefinition.linkedType, 
                                                                      theEnv, 
                                                                      *(self.function.funcArgs))
            
            if isinstance(theReturnValue, types.Symbol) and theReturnValue.pyEqual("FALSE"):
                return False
            else:
                return True
            
        
        except KeyError:
            # it's ok. If a catch this exception
            # means that the wme has not an index at all
            # so no value can be tested.
            # This make the test fail
            return False
        
        except Exception, e:
            # Another type of exception catch
            # better log this
            myclips.logger.warning("Unexpected exception catch in %s: token=%s, wme=%s, exception=%s", self, token, wme, repr(e))
            #import traceback
            #import sys
            #traceback.print_stack(file=sys.stderr)
            # anyway test failed
            return False
    
    def __str__(self, *args, **kwargs):
        return self._function.toClipsStr() + " with "+", ".join(["%s=%s"%(str(k),str(v).split("=", 2)[-1]) for (k,v) in self.references.items()])
        
    def __eq__(self, other):
        return self.__class__ == other.__class__ \
                and self._references == other._references \
                and self._function == other._function
    def __neq__(self, other):
        return not self.__eq__(other)