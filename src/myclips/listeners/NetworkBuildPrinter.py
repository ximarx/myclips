'''
Created on 30/lug/2012

@author: Francesco Capozzo
'''
from myclips.EventsManager import EventsManager
from myclips.listeners.EventsManagerListener import EventsManagerListener

class NetworkBuildPrinter(EventsManagerListener):
    '''
    Print network build debug info in a resource
    (stderr/stdout/file)
    '''


    def __init__(self, resource):
        '''
        Constructor
        '''
        self._resource = resource
        EventsManagerListener.__init__(self, {
                EventsManager.E_NODE_ADDED: self.onNodeAdded,
                EventsManager.E_NODE_REMOVED: self.onNodeRemoved,
                EventsManager.E_NODE_LINKED: self.onNodeLinked,
                EventsManager.E_NODE_UNLINKED: self.onNodeUnlinked
            })
        
        self._nodeMap = {}
        self._nodeCounter = 0
        
        
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
    
    
    