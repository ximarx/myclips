'''
Created on 23/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.Node import Node
from myclips.rete.Memory import Memory
from myclips.rete.WME import WME
from myclips.MyClipsException import MyClipsBugException
from myclips.rete.BetaInput import BetaInput
from myclips.rete.Token import Token

class BetaMemory(Node, Memory, BetaInput):
    '''
    BetaMemory: local storage for tokens.
        Combine a wme and a token that create a partial activation
        and pass join tests in a new token. Store it and propagate
        the activation to all children.
        BetaMemory node is a one input node, but it get activations
        only from an another beta network node. So, all activations
        come from the leftParent. This node has no rightParent
    '''


    def __init__(self, leftParent=None):
        '''
        Constructor
        '''
        Node.__init__(self, rightParent=None, leftParent=leftParent)
        Memory.__init__(self)
        
        
    def leftActivation(self, token, wme):
        """
        Get a token + wme that pass all binding tests
        from leftParent node (JoinNode), combine this values
        as a new Token, store it in the local storage
        and forward the activation to children
        Token could be None if the leftParent
        is a DummyNode. 
        
        @param wme: a wme that activate this node
        @type wme: myclips.rete.WME
        @param token: a token
        @type token: myclips.Token | None
        """
        
        if wme is not None and not isinstance(wme, WME):
            raise MyClipsBugException("BetaMemory activated with a non-WME item: <%s:%s>"%(wme.__class__.__name__,
                                                                                            wme))
        if token is not None and not isinstance(token, Token):
            raise MyClipsBugException("BetaMemory activated with a non-Token item: <%s:%s>"%(wme.__class__.__name__,
                                                                                            wme))
        
        # create a new token to combine the token + wme    
        token = Token(self, token, wme)
        
        # store it in the local storage
        self.addItem(token)
        
        # then: propagate the new token to
        #     all children (JoinNode/NegativeNode/etcetc...)
        
        for child in self.children:
            child.leftActivation(token, None)
    
    def delete(self, notifierRemoval=None, notifierUnlinking=None):
        """
        Remove the beta-memory from the network
        """
        # first delete all tokens
        Memory.delete(self)
            
        # then i can call parent destructor
        Node.delete(self, notifierRemoval, notifierUnlinking)
        
        
    def updateChild(self, child):
        """
        Force left activation of the child
        with all local results stored in this
        beta-memory
        """
        for token in self.items:
            child.leftActivation(token, None)
        
        
    def __str__(self, *args, **kwargs):
        return "<{0}: left={2}, children={3}, items={4}>".format(
                        self.__class__.__name__,
                        str(id(self)),
                        str(id(self.leftParent)) if not self.isLeftRoot() else "None",
                        len(self.children),
                        len(self._items),
                    )
        
        