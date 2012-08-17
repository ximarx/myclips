'''
Created on 04/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.Node import Node
from myclips.rete.HasMemory import HasMemory
from myclips.rete.HasTests import HasTests
from myclips.rete.AlphaInput import AlphaInput
import myclips

class PropertyTestNode(Node, HasMemory, HasTests, AlphaInput):
    '''
    Execute a test over some properties of
    a wme
    This node is part of Alpha Network 
    '''


    def __init__(self, parent=None, tests=None):
        '''
        Constructor
        '''
        Node.__init__(self, rightParent=parent)
        HasMemory.__init__(self, None)
        HasTests.__init__(self, tests)
        #Tester.__init__(self. tests)

    def rightActivation(self, wme):
        """
        Perform a right activation (this is an alpha node)
        for the node and propagate the wme only
        if tests passed.
        Store partial results in memory if needed
        """
        # from right i always got wme item
        if self.isValid(wme):
            # add this wme to local storage
            if self.hasMemory():
                self.memory.rightActivation(wme)
            
            # propagate this wme to all childs
            for child in self.children:
                child.rightActivation(wme)
                
    def updateChild(self, child):
        # to update a child i can read 
        # items in a linked memory if any
        # or use the parent linked memory + test 
        if self.hasMemory() and self.memory != child:
            for wme in self.memory.items:
                child.rightActivation(wme)
        else:
            # store all children in a buffer var
            oldChildren = self._children
            # store the current memory in a buffer var
            oldMemory = self.memory
            self._children = [child]
            
            # this will call the right activation for this node
            # and will forward (if possible)
            # activation to the child ('cause it's the only child)
            self.rightParent.updateChild(self)
            
            # then restore old memory and children
            self.memory = oldMemory
            self._children = oldChildren
    
    
    # alias for rightActivation
    # for backward compatibility with old rete impl
    def activation(self, wme):
        myclips.logger.warn("Deprecated old activation used")
        return self.rightActivation(wme)
    
    def __str__(self, *args, **kwargs):
        return "<{0}: right={2}, memory={3}, children={4}, tests{5}>".format(
                        self.__class__.__name__,
                        str(id(self)),
                        str(id(self.rightParent)) if not self.isRightRoot() else "None",
                        str(id(self.memory)) if not self.hasMemory() else "None",
                        len(self.children),
                        [str(t) for t in self.tests]
                    )
        
