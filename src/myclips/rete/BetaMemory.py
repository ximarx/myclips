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
        
        if not isinstance(wme, WME):
            raise MyClipsBugException("BetaMemory activated with a non-WME item: <%s:%s>"%(wme.__class__.__name__,
                                                                                            wme))
        if token != None and not isinstance(token, Token):
            raise MyClipsBugException("BetaMemory activated with a non-Token item: <%s:%s>"%(wme.__class__.__name__,
                                                                                            wme))
        
        # create a new token to combine the token + wme    
        newToken = Token(self, token, wme)
        
        # store it in the local storage
        self.addItem(newToken)
        
        # then: propagate the new token to
        #     all children (JoinNode/NegativeNode/etcetc...)
        
        for child in self.children:
            child.leftActivation(token, None)
    
    def delete(self):
        """
        Remove the beta-memory from the network
        """
        
        # before to call the Node.delete,
        # all tokens created by this node 
        # to combine partial matches
        # must be deleted (and automatically all successors)
        while len(self.items) > 0:
            token = self.items.pop(0)
            token.delete()
            del token
            
        # then i can call parent destructor
        Node.delete(self)
        
        
    def updateChild(self, child):
        """
        Force left activation of the child
        with all local results stored in this
        beta-memory
        """
        for token in self.items:
            child.leftActivation(token)
        
        
        