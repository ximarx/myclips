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
    
    
class MyClipsBugException(MyClipsException):
    """
    Special exception class to raise if
    myclips is in an unrecoverable failure state,
    and reason is a implementation error
    """
    pass