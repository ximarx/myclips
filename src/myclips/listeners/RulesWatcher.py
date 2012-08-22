'''
Created on 30/lug/2012

@author: Francesco Capozzo
'''
from myclips.EventsManager import EventsManager
from myclips.listeners.EventsManagerListener import EventsManagerListener

class RulesWatcher(EventsManagerListener):
    '''
    Show a message when rules are fired
    '''


    def __init__(self, resource):
        '''
        Constructor
        '''
        self._resource = resource
        EventsManagerListener.__init__(self, {
                EventsManager.E_RULE_FIRED: self.onRuleFired,
            })
        
        
    ######################
    #    Events SLOTS    #
    ######################
    
    def onRuleFired(self, theMainRuleName, theRuleName, theWmes, *args, **kwargs):
        print >> self._resource, "Rule fired: %s, %s"%(theMainRuleName, str([x.factId for x in theWmes]))

        
    

    