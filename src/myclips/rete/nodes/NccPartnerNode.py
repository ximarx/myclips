'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.Node import Node
from myclips.rete.BetaInput import BetaInput
from myclips.rete.Token import Token

class NccPartnerNode(Node, BetaInput):
    '''
    Right part of the Ncc/NccPartner duo: 
    get inputs from a beta subcircuit and store partial results in a buffer
    waiting for ncc node to read them
    '''


    def __init__(self, leftParent, circuitLenght, nccNode):
        '''
        Build a new NccPartner
        '''
        Node.__init__(self, leftParent=leftParent)
        
        self._circuitLength = circuitLenght
        self._nccNode = nccNode
        self._buffer = []
        
    def leftActivation(self, token, wme):
        """
        Left activation for ncc-parnet:
        create a new token and store it
        in the buffer (if no match with
        token in the ncc main node is found)
        or add a new nccresult and destroy
        propagated tokens if there is a match
        """
        
        # basically ncc-partner does 3 things:
        #    1) build a new token and link it to this node
        #    2) check if the new token match with token in 
        #        main ncc node memory
        #    3a) store a new ncc result if match found and revoke
        #        all activation from that token
        #    3b) store the new token in the buffer and wait
        #        for ncc main node to be activated and
        #        evaluate token in buffer
        
        # 1)
        nToken = Token(self, token, wme)
        
        # 2) problem 1: ncc and ncc-partner have a common
        #    parent: the node who feed them both.
        #    this means that i need to compare the new token
        #    agains a token in the ncc main memory
        #    that has same parent. To make this comparison
        #    possible i have to get the token that
        #    create the activation of the ncc circuit.
        #    I can use the circuitLenght property for this
        
        parentToken = token
        parentWme = wme
        for _ in range(0, self._circuitLength):
            parentWme = parentToken.wme
            parentToken = parentToken.parent
        
        # 2) problem 2: new i need to scan all the ncc main memory
        #    and find a token with the same parent token and wme
        for mToken in self.nccNode.items:
            # optimization: puth wme comparison first because is
            #    faster then token comparison
            if mToken.wme == parentWme and mToken.parent == parentToken:
                # 3a) 
                # I found a token who match both circuits
                # this is a new ncc result
                # so it's time to link it
                mToken.linkNccResult(nToken)
                # nToken owner is set by the linkNccResult automatically 
                
                # i need to destroy all children of the
                # mToken because they are revocated now
                mToken.deleteChildren()
                
                # the function end on first match:
                #    - there is no reason to keep scanning the main ncc memory
                #        because only one match can be found
                #    - there is no reason to stay in this method, no need to
                #        to store the nToken in the buffer. It's has been just evaluated
                return
        
        # 3b)
        # if no match has been found in the for loop
        # means that: 
        #    - there is no match at all
        #    OR
        #    - there is a match, but it will in the future
        #        when ncc main node will be left-activated.
        # Anyway, i need to store the partial match in the buffer
        # when main node will be activated, it will read and flush the buffer
        self._buffer.append(nToken)
        
    def delete(self):
        """
        Delete all token in the results buffer
        and then remove the node from the network.
        """
        while len(self._buffer) > 0:
            # i use the pop:
            # token doesn't have
            # link to results buffer
            # so i must force the ref removal
            # from it
            self._buffer.pop().delete()
            
        Node.delete(self)
        
#    # NO UPDATE IS NEEDED
#    def updateChild(self, child):
#        Node.updateChild(self, child)
        
    def getFlushResultsBuffer(self):
        b = self._buffer
        self._buffer = []
        return b
        
    @property
    def resultsBuffer(self):
        return self._buffer
        
    @property
    def nccNode(self):
        return self._nccNode
    
