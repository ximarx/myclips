'''
Created on 30/lug/2012

@author: Francesco Capozzo
'''
from myclips.EventsManager import EventsManager
from myclips.listeners.EventsManagerListener import EventsManagerListener

class ActivationsWatcher(EventsManagerListener):
    '''
    Show a message when an activation is added or removed
    '''


    def __init__(self, resource):
        '''
        Constructor
        '''
        self._resource = resource
        EventsManagerListener.__init__(self, {
                EventsManager.E_RULE_ACTIVATED: self.onRuleActivated,
                EventsManager.E_RULE_DEACTIVATED: self.onRuleDeactivated,
            })
        
        
    ######################
    #    Events SLOTS    #
    ######################
    
    def onRuleActivated(self, theMainRuleName, theRuleName, theWmes, *args, **kwargs):
        print >> self._resource, "+Activation: %s, %s"%(theMainRuleName, str([x.factId for x in theWmes]))

    def onRuleDeactivated(self, theMainRuleName, theRuleName, theWmes, *args, **kwargs):
        print >> self._resource, "-Activation: %s, %s"%(theMainRuleName, str([x.factId for x in theWmes]))
        
    

    