'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.BetaMemory import BetaMemory
from myclips.rete.NccPartnerNode import NccPartnerNode
from myclips.rete.Token import Token

class NccNode(BetaMemory):
    '''
    Left part of the Ncc/NccPartner duo
    for negative condition of a subconditions chain
    This node act like a beta memory: store activations
    from the left parent and try to combine it
    with items from the right parent (which is a
    ncc-partner-node)
    
    Ncc/NccPartner are a special composition of nodes
    because negation of multiple condition requires
    a node to get left activations from 2 different 
    left parent. To avoid double parent, ncc parent is
    used to convert one of the parent as a right input
    for the ncc main node
    '''


    def __init__(self, leftParent, rightParent, partnerCircuitLength):
        '''
        Create the new ncc node
        '''
        BetaMemory.__init__(self, leftParent=leftParent)
        
        self._partner = NccPartnerNode(leftParent=rightParent, partnerCircuitLength, self)
        
    def leftActivation(self, token, wme):
        
        # combine match in new token
        token = Token(self, token, wme)
        
        # store it inside the local memory
        self.addItem(token)
        
        # get the token stored in the partner node
        # (getFlushBuffer automatically flush the buffer)
        for pToken in self.partner.getFlushBuffer():
            # and link them to this token as ncc result
            # (and link this token as their nccOnwer:
            #    this is done automaticcaly inside the
            #    linkNccResult method
            # )
            token.linkNccResult(pToken)
        
        # i can propagate the token ONLY if
        # not ncc results are linked to this token
        if not token.hasNccResults():
            for child in self.children:
                child.leftActivation(token, None)
        
    def delete(self):
        """
        Remove this node and the partner from the network
        """
        # notify unlink between ncc and partner
        #EventManager.trigger(EventManager.E_NODE_UNLINKED, self.get_partner(), self)
        # then destroy the partner
        self.partner.delete()
        # and last destroy this node itself
        BetaMemory.delete(self)
        
    def updateChild(self, child):
        """
        Propagate activation to a child
        only if no ncc-result is found
        for each activation
        """
        for token in self.items():
            if not token.hasNccResults():
                child.leftActivation(token, None)
        
    @property
    def partner(self):
        return self._partner