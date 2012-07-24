'''
Created on 23/lug/2012

@author: Francesco Capozzo
'''

class WME(object):
    '''
    WME: a working memory element. Rappresent a fact
        inside the rete network
    '''


    def __init__(self, factId, values):
        '''
        Constructor
        '''
        self._alphaMemories = []
        self._tokens = {}
        self._negativeJoinResults = []
        self._factId = factId
        self._values = values
        
        
    def delete(self):
        """
        Revoke all activations made by this wme
        and delete the wme itself
        """
        
        # at first, remove this wme from all
        # alpha memories and reset the container
        for memory in self._alphaMemories:
            memory.removeItem(self)
        self._alphaMemories = []
        
        # then, revoke all token where this wme
        # has a role
        while len(self._tokens) > 0:
            # token removal from wme dict
            # must be required by the token itself
            # so i just pick every time a random token
            # and require removal until all token has been removed
            self._tokens[self._tokens.keys()[0]].delete()
            
        # last but not least, njr cleanup
        #from myclips.rete.nodes.NegativeJoinNode import NegativeJoinResult
        for njr in self._negativeJoinResults:
            #assert isinstance(njr, NegativeJoinResult)
            njr.token.unlinkNegativeJoinResult(njr)
            # after i removed a negative join result from a token
            # i need to revaluate if the njr was the last one.
            # if true, then token must be propagated
            # to token creator node's children 
            if not njr.token.hasNegativeJoinResults():
                for child in njr.token.node.children:
                    child.leftActivation(njr.token, None)
            
        self._negativeJoinResults = [] # for garbage collector ?
        
    @property
    def factId(self):
        return self._factId
    
    @factId.setter
    def factId(self, value):
        self._factId = value
        
    @property
    def values(self):
        return self._values
    
    @values.setter
    def values(self, values):
        self._values = values
        
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
        
    def linkToken(self, token):
        self._tokens[token] = token
        
    def unlinkToken(self, token):
        del self._tokens[token]
        
    def hasNegativeJoinResults(self):
        return len(self._negativeJoinResults) > 0
        
    def linkNegativeJoinResults(self, njr):
        self._negativeJoinResults.append(njr)
        
    def unlinkNegativeJoinResults(self, njr):
        self._negativeJoinResults.remove(njr)
        
    def __hash__(self, *args, **kwargs):
        return self.factId
    
    def __eq__(self, other):
        return ( isinstance(other, WME) and self.factId == other.factId)

    def __neq__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        return "<WME:f-%d,%s>"%(self.factId, self.values)