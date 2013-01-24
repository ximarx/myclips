'''
Created on 30/lug/2012

@author: Francesco Capozzo
'''
from myclips.Observable import Observable


class EventsManager(Observable):
    '''
    Manage events and listener
    '''
    
    # args: complete-main-rulename, complete-rulename, token linearized (no-None)
    E_RULE_FIRED = 'rule-fired'
    # args: complete-main-rulename, complete-rulename, token linearized (no-None)
    E_RULE_ACTIVATED = 'rule-activated'
    # args: complete-main-rulename, complete-rulename, token linearized (no-None)
    E_RULE_DEACTIVATED = 'rule-deactivated'
    # args: defruleconstruct, pnode
    E_RULE_ADDED = 'rule-added'
    # args: pnode
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
    E_FACT_RETRACTED = 'fact-retracted'
    
    # args: actionname, *args
    E_ACTION_PERFORMED = 'action-performed'
    
    # args: actionname, *args
    E_ACTION_RETURNVALUE = 'action-returnvalue'
    
    
    # args: oldfocus, newfocus
    E_FOCUS_CHANGED = 'focus-changed'
    
    E_STRATEGY_CHANGED = 'strategy-changed'

    E_DEBUG_OPTIONS_CHANGED = 'debug-options-changed'
    
    E_NETWORK_RESET_PRE = 'network-reset-pre'
    E_NETWORK_RESET_POST = 'network-reset-post'
    E_NETWORK_CLEAR_PRE = 'network-reset-pre'
    E_NETWORK_CLEAR_POST = 'network-reset-post'
    E_NETWORK_READY = 'network-ready'
    E_NETWORK_SHUTDOWN = 'network-shutdown'
    
    E_RUN_START = "run-start"
    E_RUN_STOP = "run-stop"
    E_RUN_PAUSE = "run-pause"
    E_RUN_RESUME = "run-resume"

    __EVENTS__ = []
    
    default = None
    
    def __init__(self, events=None):
        '''
        Create a new instance of EventsManager
        
        @param events: a list of custom events to add to standard ones
        @type events: list of string
        '''
        Observable.__init__(self, events=EventsManager.__EVENTS__ + (events if isinstance(events, list) else []))
    
    @classmethod
    def _registerMainEvents(cls):
        '''
        Register all E_xxx attributes as standard events
        
        @note this method is called on module initialization,
            before any instance could be created. Do not call
            this method manually (it's useless also)
        @param cls: this class type
        @type cls: type
        '''
        if len(cls.__EVENTS__) == 0:
            cls.__EVENTS__ = [getattr(cls, x) for x in dir(cls) if x[0:2] == "E_" and not callable(getattr(cls, x))]
    
    def __repr__(self, *args, **kwargs):
        return "<EventsManager%s>"%(": default=True" if self == EventsManager.default else "")
    
EventsManager._registerMainEvents()
EventsManager.default = EventsManager()
    
if __name__ == '__main__':
    
    import pprint
    
    em = EventsManager()
    print ", ".join(em.events)
        
    