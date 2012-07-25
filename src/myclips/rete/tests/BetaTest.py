'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.Token import Token
from myclips.rete.WME import WME

class BetaTest(object):
    '''
    Base class for tests in beta network
    '''

    def isValid(self, token, wme):
        raise NotImplementedError()
    
    def __eq__(self, other):
        return (self.__class__ == other.__class__)
    
    @staticmethod
    def getTokenAnchestor(token, tokenRelativeIndex):
        """
        Search a token anchestor from the relative index
        to the current parent
        """
        assert isinstance(token, Token)

        for _ in range(0, tokenRelativeIndex):
            token = token.parent
            
        return token
        
    @staticmethod
    def getWmeFragmentValue(wme, coordinates):
        assert isinstance(wme, WME), wme.__class__.__name__
        
        wmeValue = wme.fact
        
        for subIndex in coordinates:
            wmeValue = wmeValue[subIndex]

        return wmeValue