'''
Created on 04/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.Node import Node
from myclips.rete.Memory import Memory
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
                self.memory.addItem(wme)
            
            # propagate this wme to all childs
            for child in self.childrenIterator():
                child.rightActivation()
            
    
    # alias for rightActivation
    # for backward compatibility with old rete impl
    def activation(self, wme):
        myclips.logger.warn("Deprecated old activation used")
        return self.rightActivation(wme)
    
    def __repr__(self, *args, **kwargs):
        # visualizzare informazioni su test
        return "<PropertyTestNode>"
        
if __name__ == '__main__':
    
    ctn = PropertyTestNode()
    print ctn
    print ctn.hasMemory()
    
    m = Memory()
    ctn.memory = m
    
    m.addItem(1)
    m.addItem(2)
    
    print ctn.hasMemory()
    print ctn
    print ctn.memory
        
        
        
    