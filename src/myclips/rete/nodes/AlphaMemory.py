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
    
    def delete(self):
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
            
        Node.delete(self)
        
    def updateChild(self, child):
        """
        Force right activation of the child
        with all local results stored in this
        alpha-memory
        """
        for wme in self.items:
            child.rightActivation(wme)
        
        
    def __str__(self, *args, **kwargs):
        return "<{0}: parent={1}, children={2}, items={3}>".format(
                self.__class__.__name__,
                str(not self.isRightRoot()),
                len(self.children),
                len(self.items)
            )
        