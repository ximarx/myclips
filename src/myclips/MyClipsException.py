'''
Created on 21/lug/2012

@author: Francesco Capozzo
'''

class MyClipsException(Exception):
    '''
    Base exception class for MyClips
    '''

    def __init__(self, message="", *args, **kwargs):
        self._message = message
        Exception.__init__(self, message, *args, **kwargs)
        
    @property
    def message(self):
        return self._message