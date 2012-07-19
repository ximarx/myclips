'''
Created on 19/lug/2012

@author: Francesco Capozzo
'''
from myclips.Observer import Observer

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
            
    def unregisterObserver(self, eventName=None, observer=None):
        if eventName is None:
            self._observers = dict([(event, []) for event in self._events])
        else:
            try:
                if observer is None:
                    self._observers[eventName] = []
                else:
                    self._observers[eventName].remove(observer)
            except:
                # i don't care if the event is unknown or
                # the listner is not registered
                # it's like i've unregistered it 
                pass

    @property
    def events(self):
        return self._events
    
    def fire(self, event, *args, **kargs):
        for observer in self._observers[event]:
            observer.notify(event, *args, **kargs)
        