'''
Created on 22/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.Node import Node
from myclips.rete.AlphaInput import AlphaInput
from myclips.rete.BetaInput import BetaInput
from myclips.rete.Memory import Memory
from myclips.rete.HasJoinTests import HasJoinTests
from myclips.MyClipsException import MyClipsBugException
import myclips

class JoinNode(Node, HasJoinTests, AlphaInput, BetaInput):
    '''
    JoinNode: a beta network node that checks inter-elements
        constraints between a beta network circuit
        (the leftParent) and an alpha network circuit
        (the rightParent).
        New token is created and propagated only if
        tests pass 
    '''


    def __init__(self, rightParent=None, leftParent=None, tests=None):
        '''
        Constructor
        '''
        Node.__init__(self, rightParent, leftParent)
        HasJoinTests.__init__(self, tests)
        myclips.logger.debug("JoinNode created: %s", self)
        
    def rightActivation(self, wme):
        
        leftItems = []
        
        # check if this is not a dummy node
        if self.isLeftRoot() or not isinstance(self.leftParent, Memory):
            leftItems = [None]
        else:
            # left parent is a Memory or a subclass of Memory
            leftItems = self.leftParent.items
        
        #leftParent is a Memory or has Memory properties
        for token in leftItems:
            if self.isValid(token, wme):
                # join test is valid for token + wme
                # create new token and propagate
                for child in self.children:
                    child.leftActivation(token, wme)
            
        
    def leftActivation(self, token, _=None):
        """
        Execute tests about a token propagated
        vs wme from alpha memory
        """
        
        if not isinstance(self.rightParent, Memory):
            myclips.logger.critical("Rete compiler right linked a JoinNode to a non-Memory node %s"%self.rightParent.__class__.__name__)
            raise MyClipsBugException("Invalid right parent for a JoinNode: %s"%self.rightParent.__class__.__name__)
        
        for wme in self.rightParent.items:
            if self.isValid(token, wme):
                for child in self.children:
                    child.leftActivation(token, wme)
        
    
    def updateChild(self, child):
        """
        Update the child with all partial instantiantions 
        available to this join node
        """
        
        # To avoid code duplication, the strategy used to update
        # the new child is to:
        #    1) swap the children container (it's a deque) to 
        #        a temp list with only the new child as item
        #    2) call the rightActivation for every wme in the rightParent memory
        #        (this forward all activations to the new child only)
        #    3) restore the old children list
        
        # 1)
        children_buffer = self._children
        self._children = [child]    # i can use a list instead of a deque
                                    # i will not leftAppend anything to the list while i update
                                    # the new child
                                    
        # 2)                
        for wme in self.rightParent.items():
            self.rightActivation(wme)
            
            
        # 3)
        self._children = children_buffer

    def delete(self):
        """
        Delete the JoinNode
        """
        Node.delete(self)
        #EventManager.trigger(EventManager.E_NODE_REMOVED, self)
        
    def __str__(self, *args, **kwargs):
        return "<%sJoinNode,children:%d,tests:%s>"%("Dummy" if self.isLeftRoot() else "",
                                                    len(self.children), 
                                                    self.tests)
    
        
if __name__ == '__main__':
    print JoinNode()