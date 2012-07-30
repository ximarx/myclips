'''
Created on 19/lug/2012

@author: Francesco Capozzo
'''

class Observer(object):
    '''
    This class define an interface
    to allow an Observable object
    to notify an Observer object
    about an event
    '''
    
    def __init__(self, router=None):
        self.__router = router if router is not None and isinstance(router, dict) else {}
    
    def notify(self, eventName, *args, **kargs):
        self.__router.get(eventName, lambda *a, **k:None)(*args, **kargs)

        