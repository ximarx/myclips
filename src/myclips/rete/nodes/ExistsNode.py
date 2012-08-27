'''
Created on 23/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.nodes.JoinNode import JoinNode
from myclips.rete.Memory import Memory
from myclips.rete.Token import Token

class ExistsNode(JoinNode, Memory):
    '''
    Negative Join Node: check for negative conditions
        and propagate activation only if no match
        is possible between right items (wmes) and 
        left items (tokens)
        This node act also like a local storage
    '''


    def __init__(self, rightParent, leftParent):
        '''
        Constructor
        '''
        JoinNode.__init__(self, rightParent, leftParent, [])
        Memory.__init__(self)
        self._existsCount = 0
        
    def rightActivation(self, wme):
        """
        Check new fact activation: if something
        is activated by the new wme, all activations
        from this node are retracted
        """
        
        wme.linkExistsNode(self)
        
        self._existsCount += 1

        if self._existsCount == 1:
            for token in self.leftParent.items:
                token = Token(self, token, None)
                self.addItem(token)
                for child in self.children:
                    child.leftActivation(token, None)

    def reduceCount(self):
        self._existsCount -= 1
        if self._existsCount == 0:
            Memory.delete(self)
        
    def leftActivation(self, token, _):
        """
        Left activation for Negative join node:
            when a new token + wme come from
            a previous JoinNode, left activation
            try to combine the new token<token,wme> with
            all wme in right memory and if no match is found
            then token<token, wme> is propagated (tnx to no match)
            Otherwise for every match, a negative join result is
            created and linked to token and wme. no propagation
            will ever be place until all njr aren't gone
        """
        
        if self._existsCount > 0:
            token = Token(self, token, None)
            # store the token inside the memory
            self.addItem(token)
            
            for child in self.children:
                child.leftActivation(token, None)
                
        # all done
            
    def updateChild(self, child):
        """
        Propagate all previous match (for negative
        match are not-match)
        """
        
        if self._existsCount > 0:
        
            for token in self.items:
                child.leftActivation(token, None)
    
    def delete(self, notifierRemoval=None, notifierUnlinking=None):
        """
        Remove the negative join node from the network
        and delete all tokens created by this node
        """
        
        for wme in self.rightParent.items:
            wme.unlinkExistsNode(self)
        
        # destroy tokens in memory
        Memory.delete(self)
            
        # then i can call parent destructor
        JoinNode.delete(self, notifierRemoval, notifierUnlinking)
        
    def __str__(self, *args, **kwargs):
        return "<{0}: left={2}, right={3}, children={4}, items={5}, tests={6}>".format(
                        self.__class__.__name__,
                        str(id(self)),
                        str(id(self.leftParent)) if not self.isLeftRoot() else "None",
                        str(id(self.rightParent)) if not self.isRightRoot() else "None",
                        len(self.children),
                        len(self._items),
                        [str(t) for t in self.tests]
                    )
        
    
    
class NegativeJoinResult(object):
    
    def __init__(self, token, wme):
        
        self._token = token
        self._wme = wme
        
        token.linkNegativeJoinResult(self)
        wme.linkNegativeJoinResult(self)
        
    @property
    def token(self):
        return self._token
    
    @property
    def wme(self):
        return self._wme
        
    