'''
Created on 01/ago/2012

@author: Francesco Capozzo
'''
from myclips.strategies import Strategy
import random

class Random(Strategy):
    '''
    Add new activation using a Random order. Who knows how??!? 
    '''
    NAME = "random"
    
    def newContainer(self):
        return []
    
    def insert(self, perSalienceContainer, thePNode, theToken):
        rand_index = random.randrange(0, len(perSalienceContainer))
        perSalienceContainer.insert(rand_index, (thePNode, theToken))
        
    def pop(self, perSalienceContainer):
        return perSalienceContainer.pop()
    
    def resort(self, perSalienceContainer, theOldStrategy):
        if isinstance(perSalienceContainer, list):
            # if old strategy use list too, in-place sort is possible
            random.shuffle(perSalienceContainer)
        else:
            perSalienceContainer = [theOldStrategy.iterable(perSalienceContainer)]
            random.shuffle(perSalienceContainer)
            return perSalienceContainer
            
    def remove(self, perSalienceContainer, thePNode, theToken):
        perSalienceContainer.remove((thePNode, theToken))
        
    def iterable(self, perSalienceContainer):
        return perSalienceContainer
    
