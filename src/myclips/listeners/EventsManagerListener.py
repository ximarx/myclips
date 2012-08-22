'''
Created on 30/lug/2012

@author: Francesco Capozzo
'''
from myclips.Observer import Observer
from myclips.EventsManager import EventsManager

class EventsManagerListener(Observer):
    '''
    Print network build debug info in a resource
    (stderr/stdout/file)
    '''


    def __init__(self, handlerMap):
        '''
        Constructor
        '''
        self._EM = None
        self._regEvents = handlerMap.keys() if isinstance(handlerMap, dict) and len(handlerMap) > 0 else None
        Observer.__init__(self, handlerMap)
        
    def install(self, eventsManager=None):
        '''
        Install this listener inside an observable EventsManager
        If no EventsManager is submitted, EventsManager.default will be used
        
        Before the listener can be installed, any previous installation
        will be reverted
        
        @param eventsManager: the EventsManager to install to
        @type eventsManager: EventsManager
        @return: The listener itself
        @rtype: EventsManagerListener
        '''
        if eventsManager is None:
            eventsManager = EventsManager.default
        
        # uninstall this object
        # from old eventsmanager (if any)
        self.uninstall()
        
        self._EM = eventsManager
        self._installImpl()
        return self
        
    def _installImpl(self):
        
        for event in (self._regEvents if self._regEvents is not None else []):
            self._EM.registerObserver(event, self)
        
    def uninstall(self):
        '''
        Remove this object from the eventsManager's listeners 
        '''
        
        if self._EM is None:
            return
        
        # try to uninstall this listener from the observable
        # using the events in the handlerMap
        # if the listners doesn't use the handlerMap
        # try to remove this listener from all events the observable
        # can fire
        iterateOver = self._regEvents if self._regEvents is not None else self._EM.events
        
        for event in iterateOver:
            self._EM.unregisterObserver(event, self)
            
    def __repr__(self, *args, **kwargs):
        return "<%s>"%repr(self.__class__)
    
        

    