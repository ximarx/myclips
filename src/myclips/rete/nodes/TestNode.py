'''
Created on 22/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.Node import Node
from myclips.rete.BetaInput import BetaInput
from myclips.rete.Memory import Memory
from myclips.rete.HasJoinTests import HasJoinTests
from myclips.MyClipsException import MyClipsBugException

class TestNode(Node, HasJoinTests, BetaInput):
    '''
    TestNode: a beta network node that checks 
        if a token pass some complex tests.
        Tests are made over the token only.
        This node has no alpha-input
    '''


    def __init__(self, leftParent=None, tests=None):
        '''
        Constructor
        '''
        Node.__init__(self, leftParent=leftParent)
        HasJoinTests.__init__(self, tests)
        
    def leftActivation(self, token, _=None):
        """
        Execute tests against a propagated token
        """
        
        if self.isValid(token, None):
            for child in self.children:
                child.leftActivation(token, None)
        
    
    def updateChild(self, child):
        """
        Update the child with all partial match 
        available to this test node
        """

        # the strategy is:
        #    get all token from the left memory (it's a memory for sure!)
        #    check validity and propagate to the child
        if not isinstance( self.leftParent, Memory ):
            raise MyClipsBugException("The TestNode %s has a non-Memory as left-parent: %s",self, self.leftParent)
        
        for item in self.leftParent.items:
            if self.isValid(item, None):
                child.leftActivation(item, None)

#    def delete(self, notifierRemoval=None, notifierUnlinking=None):
#        """
#        Delete the TestNode
#        """
#        Node.delete(self, notifierRemoval, notifierUnlinking)
        
    
    def __str__(self, *args, **kwargs):
        return "<{0}: left={2}, children={3}, tests={4}>".format(
                        self.__class__.__name__,
                        str(id(self)),
                        str(id(self.leftParent)) if not self.isLeftRoot() else "None",
                        len(self.children),
                        [str(t) for t in self.tests]
                    )
        
    
