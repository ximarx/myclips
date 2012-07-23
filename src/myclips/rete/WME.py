'''
Created on 23/lug/2012

@author: Francesco Capozzo
'''

class WME(object):
    '''
    WME: a working memory element. Rappresent a fact
        inside the rete network
    '''


    def __init__(self, factId):
        '''
        Constructor
        '''
        self._alphaMemories = []
        self._tokens = []
        self._negativeJoinResults = []
        self._factId = factId
        
        
    @property
    def factId(self):
        return self._factId
    
    @factId.setter
    def factId(self, value):
        self._factId = value
        
    def linkAlphaMemory(self, alphaMemory):
        """
        Add a reference between this wme and an alpha-memory
        who store it
        """
        self._alphaMemories.append(alphaMemory)
        
    def unlinkAlphaMemory(self, alphaMemory):
        """
        Remove a reference between this wme and an alpha-memory
        """
        self._alphaMemories.remove(alphaMemory)