'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.tests.BetaTest import BetaTest
import myclips

class VariableBindingTest(BetaTest):
    '''
    Make sure that variable binding is consistent
    through multiple variable locations
    '''


    def __init__(self, wmePositionIndex, tokenRelativeIndex, tokenPositionIndex):
        '''
        Create a new VariableBindingTest. This test make sure
        that if a variable is used in multiple locations,
        it has a consistent value across all locations
        The index of the value in the current wme can be expressed
        as a list of index. Empty list means that the complete fact will be used
        Multiple indexes allow to access more position deeper in the fact instance
        Same coordinate expression must be used for token position index
        The previous wme to check to must be expressed using the relative
        distance in the token tree
        
        @param wmePositionIndex: a list of coordinates to descrive the fact slot/index
        @type wmePositionIndex: list
        @param tokenRelativeIndex: the number of parents token where the wme can be found
        @type tokenRelativeIndex: int [0 for same wme]
        @param tokenPositionIndex: a list of coordinates to descrive the fact slot/index
        @type tokenPositionIndex: list
        @return: False if test fail, True otherwise
        @rtype: Boolean  
        '''
        self._wmePositionIndex = wmePositionIndex
        self._tokenRelativeIndex = tokenRelativeIndex
        self._tokenPositionIndex = tokenPositionIndex   # this is an array of position. 
                                                        # This allow to go deep inside fact-index 
                                                        # and multifield-index in fact index 
        
    
    def isValid(self, token, wme):

        try:
            
            # if token relative index is 0, then the test is an intra-element
            # test performed in the beta network
            # this means that the wme where the variable was found first
            # is the same where the variable was found again
            if self._tokenRelativeIndex > 0:
                token = BetaTest.getTokenAnchestor(token, self._tokenRelativeIndex - 1)
    
                # get the exact wme value of the token where variable for used first
                valueInTokenWme = BetaTest.getWmeFragmentValue(token.wme, self._tokenPositionIndex)
            else:
                valueInTokenWme = BetaTest.getWmeFragmentValue(wme, self._tokenPositionIndex)
            
            # get the value in current wme there variable must have the same value
            valueInWme = BetaTest.getWmeFragmentValue(wme, self._wmePositionIndex)
        
            # when i've found them all
            # i can compare them
            return (valueInTokenWme == valueInWme)
        
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
            # anyway test failed
            return False
    
    def __str__(self, *args, **kwargs):
        return "wme{0}={1}{2}[{3}]".format(self._wmePositionIndex,
                                    "token" if self._tokenRelativeIndex > 0 else "wme",
                                    "[" + str(self._tokenRelativeIndex * -1) + "]" if self._tokenRelativeIndex > 0 else "", 
                                    "][".join([str(x) for x in self._tokenPositionIndex])
                                    )
        
    def __eq__(self, other):
        return self.__class__ == other.__class__ \
                and self._wmePositionIndex == other._wmePositionIndex \
                and self._tokenRelativeIndex == other._tokenRelativeIndex \
                and self._tokenPositionIndex == other._tokenPositionIndex