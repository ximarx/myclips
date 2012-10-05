'''
Created on 01/ago/2012

@author: Francesco Capozzo
'''
from myclips.strategies import Strategy

try:
    
    import blist

except ImportError:
    
    from myclips.strategies.Depth import Depth as Mea
    import myclips
    
    myclips.logger.warning("BList library is required by Mea strategy. Depth will be used in place of Mea")
    myclips.logger.warning("\tPlease install BList: easy_install blist")
    
else:

    class Mea(Strategy):
        '''
        Adds new activations using a MEA strategy 
        '''
        NAME = "mea"
        
        def newContainer(self):
            return blist.sortedlist(key=lambda x: self._first_epoc(x[1]))
        
        def insert(self, perSalienceContainer, thePNode, theToken):
            perSalienceContainer.add((thePNode, theToken))
            
        def pop(self, perSalienceContainer):
            return perSalienceContainer.pop(0)
        
        def resort(self, perSalienceContainer, theOldStrategy):
            return blist.sortedlist(iterable=theOldStrategy.iterable(perSalienceContainer),key=lambda x: self._first_epoc(x[1]))
                
        def remove(self, perSalienceContainer, thePNode, theToken):
            perSalienceContainer.remove((thePNode, theToken))
            
        def iterable(self, perSalienceContainer):
            return list(perSalienceContainer)
        
        def _first_epoc(self, theToken):
            return min([x.factId for x in theToken.linearize(False)])

