'''
Created on 30/lug/2012

@author: Francesco Capozzo
'''
from myclips.Observable import Observable


class EventsManager(Observable):
    
    E_RULE_FIRED = 'rule-fired'
    E_RULE_ACTIVATED = 'rule-activated'
    E_RULE_DEACTIVATED = 'rule-deactivated'
    E_RULE_ADDED = 'rule-added'
    E_RULE_REMOVED = 'rule-removed'
    
    E_NODE_ADDED = 'node-added'
    E_NODE_REMOVED = 'node-removed' 
    E_NODE_LINKED = 'node-linked'
    E_NODE_UNLINKED = 'node-unlinked'
    E_NODE_ACTIVATED = 'node-activated'
    E_NODE_ACTIVATED_LEFT = 'node-activated-left'
    E_NODE_ACTIVATED_RIGHT = 'node-activated-right'
    E_NODE_SHARED = 'node-shared'

    E_FACT_ASSERTED = 'fact-asserted'
    E_FACT_RETRACTD = 'fact-retracted'
    
    E_ACTION_PERFORMED = 'action-performed'
    
    E_STRATEGY_CHANGED = 'strategy-changed'

    E_DEBUG_OPTIONS_CHANGED = 'debug-options-changed'
    
    E_NETWORK_READY = 'network-ready'
    E_NETWORK_SHUTDOWN = 'network-shutdown'

    __EVENTS__ = []
    
    default = None
    
    def __init__(self, events=None):
        Observable.__init__(self, events=EventsManager.__EVENTS__ + (events if isinstance(events, list) else []))
    
    @classmethod
    def _registerMainEvents(cls):
        if len(cls.__EVENTS__) == 0:
            cls.__EVENTS__ = [getattr(cls, x) for x in dir(cls) if x[0:2] == "E_" and not callable(getattr(cls, x))]
    
    def __repr__(self, *args, **kwargs):
        return "<EventsManager%s>"%(": default=True" if self == EventsManager.default else "")
    
EventsManager._registerMainEvents()
EventsManager.default = EventsManager()
    
if __name__ == '__main__':
    
    import pprint
    
    em = EventsManager()
    pprint.pprint(em.events)
    