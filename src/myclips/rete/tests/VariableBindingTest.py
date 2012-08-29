'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.tests.BetaTest import BetaTest
import myclips
from myclips.rete.tests.locations import VariableReference
from myclips.rete.tests import getTokenAnchestor

class VariableBindingTest(BetaTest):
    '''
    Make sure that variable binding is consistent
    through multiple variable locations
    '''


    def __init__(self, reference):
        '''
        Create a new VariableBindingTest. This test make sure
        that if a variable is used in multiple locations,
        it has a consistent value across all locations
        
        @param reference: is a location with a reference to a previous binded variable
        @type reference: VariableReference
        @return: False if test fail, True otherwise
        @rtype: Boolean  
        '''
        
        self._reference = reference
        
        
#        self._wmePositionIndex = wmePositionIndex
#        self._tokenRelativeIndex = tokenRelativeIndex
#        self._tokenPositionIndex = tokenPositionIndex   # this is an array of position. 
                                                        # This allow to go deep inside fact-index 
                                                        # and multifield-index in fact index 
    @property
    def reference(self):
        return self._reference
    
    def isValid(self, token, wme):

        reference = self._reference

        assert isinstance(reference, VariableReference)        
        

        try:
            
            # if token relative index is 0, then the test is an intra-element
            # test performed in the beta network
            # this means that the wme where the variable was found first
            # is the same where the variable was found again
            if reference.relPatternIndex != 0:
                nToken = getTokenAnchestor(token, (-1 * reference.relPatternIndex) - 1)
    
                # get the exact wme value of the token where variable for used first
                valueInTokenWme = reference.reference.toValue(nToken.wme)
            else:
                valueInTokenWme = reference.reference.toValue(wme)
            
            # get the value in current wme there variable must have the same value
            valueInWme = reference.toValue(wme)
        
            # when i've found them all
            # i can compare them
            # for eq or neq based on reference.isNegative value
            eqResult = (valueInTokenWme == valueInWme)
            return eqResult if reference.isNegative is not True else not eqResult
        
        except KeyError:
            # it's ok. If a catch this exception
            # means that the wme has not an index at all
            # so no value can be tested.
            # This make the test fail
            return False
        
        except Exception, e:
            # Another type of exception catch
            # better log this
            myclips.logger.warning("Unexpected exception caught in %s: token=%s, wme=%s, exception=%s", self, token, wme, repr(e))
            # anyway test failed
            return False
    
    def __str__(self, *args, **kwargs):
        return str(self._reference)
    
    def __eq__(self, other):
        return self.__class__ == other.__class__ \
                and self._reference == other._reference
    def __neq__(self, other):
        return not self.__eq__(other)