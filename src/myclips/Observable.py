'''
Created on 19/lug/2012

@author: Francesco Capozzo
'''
from myclips.Observer import Observer
import myclips

class Observable(object):
    '''
    This class define an interface
    to allow an Observer object
    to register for an event fired by 
    the Observable objest
    '''
    
    def __init__(self, events=None):
        '''
        Initialize the observable
        @param events: a tuple of watchable events
        @type events: tuple
        '''
        self._events = tuple(events) if isinstance(events, (list, tuple)) else ()
        '''store the events'''
        self._observers = dict([(event, []) for event in self._events])
        '''store the observer, using event-name as index'''
        
    def registerObserver(self, eventName, observer):
        '''
        Register a new observer for an event
        @param eventName: the event name
        @type eventName: string
        @param observer: the observer instance
        @type observer: L{Observer}
        '''
        if isinstance(observer, Observer):
            try:
                self._observers[eventName].append(observer)
            except KeyError:
                # no observer for the event yet
                self._observers[eventName] = [observer]

            myclips.logger.debug("Registering new observer %s\n\tfor event %s.%s",
                                        repr(observer),
                                        repr(self),
                                        eventName)
            
    def unregisterObserver(self, eventName=None, observer=None):
        '''
        Unregister a single or a group of observer
        from an event (or all events)
        @param eventName: an event name or None for everything
        @type eventName: string
        @param observer: a single observer for a single event. This params
            is ignored if eventName is None
        @type observer: L{Observer}
        '''
        if eventName is None:
            self._observers = dict([(event, []) for event in self._events])
        else:
            try:
                if observer is None:
                    self._observers[eventName] = []
                else:
                    self._observers[eventName].remove(observer)
                    
                myclips.logger.debug("Unregistering observer %s\n\tfrom event %s.%s",
                                            repr(observer),
                                            repr(self),
                                            eventName)
            except:
                # i don't care if the event is unknown or
                # the listner is not registered
                # it's like i've unregistered it 
                pass

    @property
    def events(self):
        '''
        Get watchable events
        '''
        return self._events
    
    def getObservers(self, eventName):
        '''
        Get the list of observer for an event
        @param eventName: the event
        @type eventName: string
        '''
        return self._observers[eventName]
    
    def cleanupObserver(self, observer):
        '''
        Remove an observer from all events where
        it's registered
        @param observer: the observer
        @type observer: L{Observer}
        '''
        for eventObs in self._observers.values():
            try:
                eventObs.remove(observer)
            except ValueError:
                pass
    
    def fire(self, event, *args, **kargs):
        '''
        Fire an event with custom args
        @param event: the event
        @type event: string
        '''
        try:
            observers = self._observers[event]
        except:
                myclips.logger.error("Invalid event %s \n\tfor %s",
                                            repr(event),
                                            repr(self))
        else:
            if len(observers) > 0:
                myclips.logger.debug("Firing %s.%s \n\twith %s \n\tto %s observer(s)",
                                           repr(self),
                                           repr(event),
                                           repr(args),
                                           str(len(observers)))
                for observer in observers:
                    observer.notify(event, *args, **kargs)
            
        