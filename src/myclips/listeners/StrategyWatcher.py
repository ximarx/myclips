'''
Created on 30/lug/2012

@author: Francesco Capozzo
'''
from myclips.EventsManager import EventsManager
from myclips.listeners.EventsManagerListener import EventsManagerListener

class StrategyWatcher(EventsManagerListener):
    '''
    Show a message when conflicts resolution strategy changes
    '''


    def __init__(self, resource):
        '''
        Constructor
        '''
        self._resource = resource
        EventsManagerListener.__init__(self, {
                EventsManager.E_STRATEGY_CHANGED: self.onStrategyChanged,
            })
        
        
    ######################
    #    Events SLOTS    #
    ######################
    
    def onStrategyChanged(self, theOld, theNew, *args, **kwargs):
        print >> self._resource, "Strategy changed: %s -> %s"%(theOld, theNew)

        
    

    