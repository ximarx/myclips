'''
Created on 25/lug/2012

@author: Francesco Capozzo
'''

class MemoryItem(object):
    '''
    Base class for items that can be stored
    inside memories (alpha or beta)
    '''

    def delete(self):
        return NotImplementedError()
    
    def __hash__(self, *args, **kwargs):
        return NotImplementedError()
    
    def __eq__(self, other):
        return NotImplementedError()
        