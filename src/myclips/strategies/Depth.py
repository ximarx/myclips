'''
Created on 01/ago/2012

@author: Francesco Capozzo
'''
from myclips.strategies import Strategy

class Depth(Strategy):
    '''
    Add new activation using a LIFO strategy 
    '''
    
    def newContainer(self):
        return []
    
    def insert(self, perSalienceContainer, thePNode, theToken):
        perSalienceContainer.append((thePNode, theToken))
        
    def pop(self, perSalienceContainer):
        return perSalienceContainer.pop()
    
    def resort(self, perSalienceContainer, theOldStrategy):
        if isinstance(perSalienceContainer, list):
            # if old strategy use list too, in-place sort is possible
            perSalienceContainer.sort(key=lambda x: self._get_max_epoch(x[1]), reverse=True)
        else:
            return [theOldStrategy.iterable(perSalienceContainer)].sort(key=lambda x: self._get_max_epoch(x[1]), reverse=True)
            
    def remove(self, perSalienceContainer, thePNode, theToken):
        perSalienceContainer.remove((thePNode, theToken))
        
    def iterable(self, perSalienceContainer):
        return perSalienceContainer
    
    def _get_max_epoch(self, token):
        return max([x.factId for x in token.linearize(False)])