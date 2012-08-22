'''
Created on 30/lug/2012

@author: Francesco Capozzo
'''
from myclips.EventsManager import EventsManager
from myclips.listeners.EventsManagerListener import EventsManagerListener

class FocusWatcher(EventsManagerListener):
    '''
    Show a message when current focus changes
    '''


    def __init__(self, resource):
        '''
        Constructor
        '''
        self._resource = resource
        EventsManagerListener.__init__(self, {
                EventsManager.E_FOCUS_CHANGED: self.onFocusChanged,
            })
        
        
    ######################
    #    Events SLOTS    #
    ######################
    
    def onFocusChanged(self, theOldFocus, theNewFocus, *args, **kwargs):
        print >> self._resource, "Focus changed: %s -> %s"%(theOldFocus, theNewFocus)

        
    

    