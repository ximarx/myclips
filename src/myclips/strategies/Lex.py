'''
Created on 01/ago/2012

@author: Francesco Capozzo
'''
from myclips.strategies import Strategy

try:
    
    import blist

except ImportError:
    
    from myclips.strategies.Depth import Depth as Lex
    import myclips
    
    myclips.logger.warning("BList library is required by Lex strategy. Depth will be used in place of Lex")
    myclips.logger.warning("\tPlease install BList: easy_install blist")
    
else:

    class Lex(Strategy):
        '''
        Adds new activations using a FIFO strategy 
        '''
        
        def newContainer(self):
            return blist.sortedlist(key=lambda x: self._sort_epoch(x[1]))
        
        def insert(self, perSalienceContainer, thePNode, theToken):
            perSalienceContainer.add((thePNode, theToken))
            
        def pop(self, perSalienceContainer):
            perSalienceContainer.pop()
        
        def resort(self, perSalienceContainer, theOldStrategy):
            return blist.sortedlist(iterable=theOldStrategy.iterable(perSalienceContainer),key=lambda x: self._sort_epoch(x[1]))
                
        def remove(self, perSalienceContainer, thePNode, theToken):
            perSalienceContainer.remove((thePNode, theToken))
            
        def iterable(self, perSalienceContainer):
            return list(perSalienceContainer)
        
        def _sort_epoch(self, theToken):
            return sorted([x.factId for x in theToken.linearize(False)])

