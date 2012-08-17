'''
Created on 04/lug/2012

@author: Francesco Capozzo
'''
import collections

class Node(object):
    '''
    Rete Node baseclass
    '''


    def __init__(self, rightParent=None, leftParent=None):
        '''
        Constructor
        '''
        self._rightParent = rightParent
        self._leftParent = leftParent
        self._children = collections.deque()
        
    @property
    def rightParent(self):
        """
        Reference to right parent of node
        """
        return self._rightParent
    
    @rightParent.setter
    def rightParent(self, newP):
        self._rightParent = newP

    @property
    def leftParent(self):
        """
        Reference to left parent of node
        """
        return self._leftParent
    
    @leftParent.setter
    def leftParent(self, newP):
        self._leftParent = newP


    def isRoot(self):
        '''
        Check if node is root (both left and right)
        '''
        return (self.isLeftRoot() and self.isRightRoot())
    
    def isLeftRoot(self):
        """
        Check if node is left orphan
        """
        return (self.leftParent == None)

    def isRightRoot(self):
        """
        Check if node is left orphan
        """
        return (self.rightParent == None)

    @property
    def children(self):
        return self._children
    
    def removeChild(self, child):
        self.children.remove(child)
    
    def prependChild(self, child):
        self._children.appendleft(child)
        
    # alias for prependChild
    addChild = prependChild
        
    def appendChild(self, child):
        self._children.append(child)
        
    def isLeaf(self):
        return len(self.children) == 0
    
    def updateChild(self, child):
        """
        Propagate all partial instantiations
        available to this not to the child
        """
        raise NotImplementedError()
    
    def delete(self):
        """
        Execute standard operations for
        node removal from the network
        and notify listeners for node removal
        """
        
        if not self.isLeftRoot():
            #EventManager.trigger(EventManager.E_NODE_UNLINKED, self, self.leftRoot)
            self.leftParent.removeChild(self)
            # check if leftParent is still usefull
            # otherwise forward deletion to it
            if self.leftParent.isLeaf():
                self.leftParent.delete()
                
        if not self.isRightRoot():
            #EventManager.trigger(EventManager.E_NODE_UNLINKED, self, self.rightRoot)
            self.rightParent.removeChild(self)
            if self.rightParent.isLeaf():
                self.rightParent.delete()
        
        #EventManager.trigger(EventManager.E_NODE_REMOVED, self)
    
    def __str__(self, *args, **kwargs):
        return "<{0}: left={2}, right={3}, children={4}>".format(
                        self.__class__.__name__,
                        str(id(self)),
                        str(id(self.leftParent)) if not self.isLeftRoot() else "None",
                        str(id(self.rightParent)) if not self.isRightRoot() else "None",
                        len(self.children)
                    )
        
    def __repr__(self, *args, **kwargs):
        return self.__str__(*args, **kwargs).replace(self.__class__.__name__, self.__class__.__name__+"@"+str(id(self)), 1)

    
    
    