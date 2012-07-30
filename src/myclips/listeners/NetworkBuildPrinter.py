'''
Created on 30/lug/2012

@author: Francesco Capozzo
'''
from myclips.Observer import Observer
from myclips.EventsManager import EventsManager

class NetworkBuildPrinter(Observer):
    '''
    Print network build debug info in a resource
    (stderr/stdout/file)
    '''


    def __init__(self, resource):
        '''
        Constructor
        '''
        self._resource = resource
        self._EM = None
        Observer.__init__(self, {
                EventsManager.E_NODE_ADDED: self.onNodeAdded,
                EventsManager.E_NODE_REMOVED: self.onNodeRemoved,
                EventsManager.E_NODE_LINKED: self.onNodeLinked,
                EventsManager.E_NODE_UNLINKED: self.onNodeUnlinked
            })
        
        self._nodeMap = {}
        self._nodeCounter = 0
        
    def install(self, eventsManager=None):
        if eventsManager is None:
            eventsManager = EventsManager.default
        
        # uninstall this object
        # from old eventsmanager (if any)
        self.uninstall()
        
        self._EM = eventsManager
        self._installImpl()
        
        
    def _installImpl(self):
        EM = self._EM
        assert isinstance(EM, EventsManager)
        
        EM.registerObserver(EventsManager.E_NODE_ADDED, self)
        EM.registerObserver(EventsManager.E_NODE_LINKED, self)
        EM.registerObserver(EventsManager.E_NODE_UNLINKED, self)
        EM.registerObserver(EventsManager.E_NODE_REMOVED, self)
        
        
    def uninstall(self):
        if self._EM is None:
            return
        
        self._EM.unregisterObserver(EventsManager.E_NODE_ADDED, self)
        self._EM.unregisterObserver(EventsManager.E_NODE_LINKED, self)
        self._EM.unregisterObserver(EventsManager.E_NODE_UNLINKED, self)
        self._EM.unregisterObserver(EventsManager.E_NODE_REMOVED, self)
        
        
    ######################
    #    Events SLOTS    #
    ######################
    
    def onNodeAdded(self, theNode):
        print >> self._resource, "+Node %d: %s"%(self._nodeCounter, str(theNode))
        self._nodeMap[theNode] = self._nodeCounter
        self._nodeCounter += 1
        
    
    def onNodeRemoved(self, theNode):
        try:
            print >> self._resource, "-Node %d: %s"%(self._nodeMap[theNode], str(theNode))
            del self._nodeMap[theNode]
        except:
            print >> "-Node #UNK: %s"%str(theNode)
    
    def onNodeLinked(self, theParent, theNode, linkType=0):
        try:
            theParentSign = self._nodeMap[theParent]
        except:
            theParentSign = "#UNK %s"%str(theParent)

        try:
            theNodeSign = self._nodeMap[theNode]
        except:
            theNodeSign = "#UNK %s"%str(theNode)

            
        print >> self._resource, "+Link: %s --%s--> %s"%(theParentSign,
                                                         ["L", "-", "R"][linkType+1],
                                                         theNodeSign)
    
    def onNodeUnlinked(self, theParent, theNode):
        
        try:
            theParentSign = self._nodeMap[theParent]
        except:
            theParentSign = "#UNK %s"%str(theParent)

        try:
            theNodeSign = self._nodeMap[theNode]
        except:
            theNodeSign = "#UNK %s"%str(theNode)
        
        print >> self._resource, "-Link: %s -----> %s"%(theParentSign,
                                                         theNodeSign)
    
    
    