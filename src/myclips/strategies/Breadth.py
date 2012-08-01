'''
Created on 01/ago/2012

@author: Francesco Capozzo
'''
from myclips.strategies import Strategy
import collections

class Breadth(Strategy):
    '''
    Adds new activations using a FIFO strategy 
    '''
    
    def newContainer(self):
        return collections.deque()
    
    def insert(self, perSalienceContainer, thePNode, theToken):
        perSalienceContainer.append(tuple(thePNode, theToken))
        
    def pop(self, perSalienceContainer):
        perSalienceContainer.popleft()
    
    def resort(self, perSalienceContainer, theOldStrategy):
        return collections.deque(sorted(theOldStrategy.iterable(perSalienceContainer),key=lambda x: self._get_max_epoch(x[1])))
            
    def remove(self, perSalienceContainer, thePNode, theToken):
        perSalienceContainer.remove((thePNode, theToken))
        
    def iterable(self, perSalienceContainer):
        return perSalienceContainer
    
    def _get_max_epoch(self, token):
        return max([x.factId for x in token.linearize(False)])
    