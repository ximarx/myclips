'''
Created on 30/lug/2012

@author: Francesco Capozzo
'''
from myclips.EventsManager import EventsManager
from myclips.listeners.EventsManagerListener import EventsManagerListener
import time
import myclips

class StatisticsWatcher(EventsManagerListener):
    '''
    Show statistics after run ends (rules fired and total time)
    '''


    def __init__(self, resource, network):
        '''
        Create a new watcher
        
        @param resource: a file resource where output will be redirected
        @param network: the Network instance watched
        '''
        
        
        self._resource = resource
        self._network = network
        self._stats = {"rules"          : 0,
                       "timer-start"    : 0,
                       "buffer"         : 0}
        EventsManagerListener.__init__(self, {
                EventsManager.E_RULE_FIRED: self.onRuleFired,
                EventsManager.E_RUN_START: self.onRunStart,
                EventsManager.E_RUN_STOP: self.onRunStop
            })
        
    ######################
    #    Events SLOTS    #
    ######################
    
    def onRuleFired(self, theMainRuleName, theRuleName, theWmes, *args, **kwargs):
        #print >> self._resource, "Rule fired: %s, %s"%(theMainRuleName, str([x.factId for x in theWmes]))
        
        self._stats["rules"] += 1
        
    def onRunStart(self, *args, **kwargs):
        #self._stats["cumulative"] = self._stats["timer-end"] - self._stats["timer-start"]
        self._stats["timer-start"] = time.time()
        
    def onRunStop(self, *args, **kwargs):
        total_time = self._stats["buffer"] + ( time.time() - self._stats["timer-start"] )
        print >> self._resource, "%d rules fired        Run time is %.3f seconds."%(self._stats['rules'], total_time)
