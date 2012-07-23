'''
Created on 23/lug/2012

@author: Francesco Capozzo
'''

class Token(object):
    '''
    classdocs
    '''


    def __init__(self, parentToken = None, wme = None):
        '''
        Constructor
        '''
        self._parent = parentToken
        self._wme = wme
        
    