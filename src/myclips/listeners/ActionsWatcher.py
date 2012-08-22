'''
Created on 30/lug/2012

@author: Francesco Capozzo
'''
from myclips.EventsManager import EventsManager
from myclips.listeners.EventsManagerListener import EventsManagerListener

class ActionsWatcher(EventsManagerListener):
    '''
    Show a message when an action is executed
    '''


    def __init__(self, resource):
        '''
        Constructor
        '''
        self._resource = resource
        EventsManagerListener.__init__(self, {
                EventsManager.E_ACTION_PERFORMED: self.onActionPerformed,
                EventsManager.E_ACTION_RETURNVALUE: self.onActionReturnValue,
            })
        
        
    ######################
    #    Events SLOTS    #
    ######################
    
    def onActionPerformed(self, theActionName, theArgs, *args, **kwargs):
        print >> self._resource, "Action performed: %s -> %s"%(theActionName, str([str(x) for x in theArgs]))

    def onActionReturnValue(self, theResult, *args, **kwargs):
        print >> self._resource, "Action return: %s"%repr(theResult)
        
    

    