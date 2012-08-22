'''
Created on 30/lug/2012

@author: Francesco Capozzo
'''
from myclips.EventsManager import EventsManager
from myclips.listeners.EventsManagerListener import EventsManagerListener

class FactsWatcher(EventsManagerListener):
    '''
    Show a message on new fact asserted or retracted
    or on re-assertion of asserted facts 
    '''


    def __init__(self, resource):
        '''
        Constructor
        '''
        self._resource = resource
        EventsManagerListener.__init__(self, {
                EventsManager.E_FACT_ASSERTED: self.onAssertFact,
                EventsManager.E_FACT_RETRACTED: self.onRetractFact,
            })
        
        
    ######################
    #    Events SLOTS    #
    ######################
    
    def onAssertFact(self, theWme, isNew=True):
        print >> self._resource, "%sFact %s"%('+' if isNew else '#', theWme)

    def onRetractFact(self, theWme):
        print >> self._resource, "-Fact %s"%theWme
        
    

    