'''
Created on 04/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.Node import Node
from myclips.rete.AlphaInput import AlphaInput
import myclips

class RootNode(Node, AlphaInput):
    '''
    Execute a test over some properties of
    a wme
    This node is part of Alpha Network 
    '''


    def __init__(self, network):
        '''
        Constructor
        '''
        Node.__init__(self)
        self._network = network

    def rightActivation(self, wme):
        """
        Simply forward all wme to children
        """
        # propagate this wme to all childs
        for child in self.children:
            child.rightActivation(wme)
                
    def updateChild(self, child):
        """
        Forward all wme in working memory
        to the child
        """
        for wme in self.network.facts:
            child.rightActivation(wme)
            
    def delete(self):
        myclips.logger.warning("RootNode delete called. Network is empty")
            
    @property
    def network(self):
        return self._network
    
    # alias for rightActivation
    # for backward compatibility with old rete impl
    def activation(self, wme):
        myclips.logger.warn("Deprecated old activation used")
        return self.rightActivation(wme)
    
    def __str__(self, *args, **kwargs):
        return "<{0}: network={2} children={3}>".format(
                        self.__class__.__name__,
                        str(id(self)),
                        self.network,
                        len(self.children)
                    )

