'''
Created on 23/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.Node import Node
from myclips.rete.Memory import Memory
from myclips.rete.AlphaInput import AlphaInput
from myclips.rete.WME import WME
from myclips.MyClipsException import MyClipsBugException

class AlphaMemory(Node, Memory, AlphaInput):
    '''
    AlphaMemory: local storage for wme and feeder for beta network. 
        Stores wme matching a group of constraints (the alpha circuit
        that lead from the root node to this one) and innescate
        beta network partial activations feeding all successors
        (that are always beta network node)
        The group of all alpha memories create a frontier
        between alpha network and beta network
    
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        Node.__init__(self, rightParent=parent, leftParent=None)
        Memory.__init__(self)
        
        
    def rightActivation(self, wme):
        """
        Store the wme in the local storage
        and propagate it to beta network
        
        @param wme: a wme that activate this node
        @type wme: myclips.rete.WME
        """
        
        if not isinstance(wme, WME):
            raise MyClipsBugException("AlphaMemory activated with a non-WME item: <%s:%s>"%(wme.__class__.__name__,
                                                                                            wme))
        
        # first: store the new wme in the memory
        #    to synch the local storage
        self.addItem(wme)
        
        # second: add a reference to this amem
        #    into the wme.
        wme.linkAlphaMemory(self)
        
        # then: propagate the new wme to the
        #     beta network
        
        for child in self.children:
            child.rightActivation(wme)
    
    def delete(self, notifierRemoval=None, notifierUnlinking=None):
        """
        Remove the alpha-memory from the network
        """
        
        # before to call the Node.delete,
        # references to this alpha-memory 
        # have to be removed
        # from all wme object
        # but wme.delete()
        # isn't called because a-memory
        # delete doens't mean fact retract
        for wme in self.items:
            wme.unlinkAlphaMemory(self)
            
            
        # before call the Node.delete,
        # manually remove the parent's reference
        # to this node (because alpha memory is in
        # parent.memory slot, not in children
        
        if not self.isRightRoot():
            if callable(notifierUnlinking):
                notifierUnlinking(self.rightParent, self)
            
            self.rightParent.memory = None
            if self.rightParent.isLeaf():
                self.rightParent.delete(notifierRemoval, notifierUnlinking)
            self.rightParent = None
        
        Node.delete(self, notifierRemoval, notifierUnlinking)
        
    def updateChild(self, child):
        """
        Force right activation of the child
        with all local results stored in this
        alpha-memory
        """
        for wme in self.items:
            child.rightActivation(wme)
        
    def __str__(self, *args, **kwargs):
        return "<{0}: right={2}, children={3}, items={4}>".format(
                        self.__class__.__name__,
                        str(id(self)),
                        str(id(self.rightParent)) if not self.isRightRoot() else "None",
                        len(self.children),
                        len(self._items)
                    )
        
