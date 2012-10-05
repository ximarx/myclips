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
        '''
        Initialize the Observer. Using the router,
        a shot-hand method to forward events to single
        method is provided
        @param router: a dict of eventName => method handler
        @type router: dict
        '''
        self.__router = router if router is not None and isinstance(router, dict) else {}
    
    def notify(self, eventName, *args, **kargs):
        '''
        Slot for event notify
        Standard implementation forward the event to
        the handler linked in the router. Custom implementations
        could override this to manually dispatch events
        @param eventName: an events name
        @type eventName: string
        '''
        self.__router.get(eventName, lambda *a, **k:None)(*args, **kargs)

        