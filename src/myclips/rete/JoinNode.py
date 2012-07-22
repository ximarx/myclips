'''
Created on 22/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.HasTests import HasTests
from myclips.rete.Node import Node
from myclips.rete.HasMemory import HasMemory
from myclips.rete.AlphaInput import AlphaInput
from myclips.rete.BetaInput import BetaInput

class JoinNode(Node, HasTests, HasMemory, HasTests, AlphaInput, BetaInput):
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
        HasTests.__init__(self, tests)
        HasMemory.__init__(self, None)
        
        
    def rightActivation(self, wme):
        AlphaInput.rightActivation(self, wme)
        
    def leftActivation(self, token):
        BetaInput.leftActivation(self, token)
        
        