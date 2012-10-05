'''
Created on 01/ago/2012

@author: Francesco Capozzo
'''
from myclips.strategies import Strategy

try:
    
    import blist

except ImportError:
    
    from myclips.strategies.Depth import Depth as Simplicity
    import myclips
    
    myclips.logger.warning("BList library is required by Semplicity strategy. Depth will be used in place of Semplicity")
    myclips.logger.warning("\tPlease install BList: easy_install blist")
    
else:

    class Simplicity(Strategy):
        '''
        Adds new activations using the specificity:
            more specificity = less priority
        '''
        NAME = "simplicity"
        
        def newContainer(self):
            return blist.sortedlist(key=lambda x: x[0].getProperty('specificity', 0))
        
        def insert(self, perSalienceContainer, thePNode, theToken):
            perSalienceContainer.add((thePNode, theToken))
            
        def pop(self, perSalienceContainer):
            return perSalienceContainer.pop(0)
        
        def resort(self, perSalienceContainer, theOldStrategy):
            return blist.sortedlist(iterable=theOldStrategy.iterable(perSalienceContainer),key=lambda x: x[0].getProperty('specificity', 0))
                
        def remove(self, perSalienceContainer, thePNode, theToken):
            perSalienceContainer.remove((thePNode, theToken))
            
        def iterable(self, perSalienceContainer):
            return list(perSalienceContainer)

