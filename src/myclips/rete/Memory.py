'''
Created on 04/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.MemoryItem import MemoryItem

class Memory(object):
    '''
    Local results storage. It contains a group of MemoryItem
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._items = {}

    @property
    def items(self):
        return self._items.values()
    
    @property
    def keys(self):
        return self._items.keys()

    def addItem(self, item):
        assert isinstance(item, MemoryItem)
        self._items[item] = item

    def removeItem(self, item):
        del self._items[item]
        
    def delete(self):
        while len(self._items) > 0:
            self._items[self._items.keys()[0]].delete()
            
        
    def __repr__(self, *args, **kwargs):
        return "<Memory: {0} item(s)>".format(
                                            len(self._items)
                                        )
    
