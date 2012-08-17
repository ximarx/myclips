'''
Created on 23/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.nodes.JoinNode import JoinNode
from myclips.rete.Memory import Memory
from myclips.rete.Token import Token

class NegativeJoinNode(JoinNode, Memory):
    '''
    Negative Join Node: check for negative conditions
        and propagate activation only if no match
        is possible between right items (wmes) and 
        left items (tokens)
        This node act also like a local storage
    '''


    def __init__(self, rightParent, leftParent, tests=None):
        '''
        Constructor
        '''
        JoinNode.__init__(self, rightParent, leftParent, tests)
        Memory.__init__(self)
        
    def rightActivation(self, wme):
        """
        Check new fact activation: if something
        is activated by the new wme, all activations
        from this node are retracted
        """

        # need to check all partial activations stored here:
        # if at least one match with this new wme
        # all partial activations propagated must be retracted
        # and a negative join result must be created to store
        # the match
        
        for token in self.items:
            if self.isValid(token, wme):
                # found a match between token and wme
                # checking if something has been propagated by the token
                if not token.hasNegativeJoinResults():
                    # something has been propagated.
                    # delete children
                    token.deleteChildren()
                    
                # then create and store a new negative join result
                NegativeJoinResult(token, wme)
                # a reference to the njr is automatically
                # insered inside token and wme
                
        
    def leftActivation(self, token, wme):
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
        
        # create a new token here
        # this is important because on future
        # negative join result creation
        # i will delete all children of
        # this new token to invalidate all 
        # propagated match 
        # i can reuse token variable, after this
        # old token is no usefull anymore
        token = Token(self, token, wme)
        
        # store the token inside the memory
        self.addItem(token)
        
        # now i need to check and combine
        # the newToken with all results
        # that comes from the alpha memory on the
        # right side of the node
        
        # i can reuse wme variable because old value
        # is useless after the newToken creation
        for wme in self.rightParent.items:
            if self.isValid(token, wme):
                # for each match i create a NegativeJoinResult
                # to store the info
                NegativeJoinResult(token, wme)
                # it's automatically linked inside token and wme
                
        # after i tried to combine the token with all wme
        # i check if negative join results has been created
        if not token.hasNegativeJoinResults():
            # not negative join result: nice... i can propagate
            for child in self.children:
                child.leftActivation(token, None)
                
        # all done
            
    def updateChild(self, child):
        """
        Propagate all previous match (for negative
        match are not-match)
        """
        for token in self.items:
            if not token.hasNegativeJoinResults():
                child.leftActivation(token, None)
    
    def delete(self):
        """
        Remove the negative join node from the network
        and delete all tokens created by this node
        """
        # destroy tokens in memory
        Memory.delete(self)
            
        # then i can call parent destructor
        JoinNode.delete(self)
        
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
        
    