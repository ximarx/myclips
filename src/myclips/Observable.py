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
        self._events = tuple(events) if isinstance(events, (list, tuple)) else ()
        self._observers = dict([(event, []) for event in self._events])
        
    def registerObserver(self, eventName, observer):
        if isinstance(observer, Observer):
            self._observers[eventName].append(observer)

            myclips.logger.debug("Registering new observer %s\n\tfor event %s.%s",
                                        repr(observer),
                                        repr(self),
                                        eventName)
            
    def unregisterObserver(self, eventName=None, observer=None):
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
        return self._events
    
    def getObservers(self, eventName):
        return self._observers[eventName]
    
    def cleanupObserver(self, observer):
        for eventObs in self._observers.values():
            try:
                eventObs.remove(observer)
            except ValueError:
                pass
    
    def fire(self, event, *args, **kargs):
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
            
        