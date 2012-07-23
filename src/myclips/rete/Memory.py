'''
Created on 04/lug/2012

@author: Francesco Capozzo
'''

class Memory(object):
    '''
    Local results storage
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
        self._items[item] = item

    def removeItem(self, item):
        del self._items[item]
        
    def __repr__(self, *args, **kwargs):
        return "<Memory: {0} item(s)>".format(
                                            len(self._items)
                                        )
    
