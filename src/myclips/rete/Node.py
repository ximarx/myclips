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
        return self._parent
    
    @rightParent.setter
    def rightParent(self, newP):
        self._parent = newP

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
    
    def prependChild(self, child):
        self._children.leftAppend(child)
        
    def appendChild(self, child):
        self._children.append(child)
        
    def childrenIterator(self):
        yield self._children

    def isLeaf(self):
        return len(self.children) == 0
    
    def __repr__(self, *args, **kwargs):
        if self.isRoot():
            return "<RootNode>"
        elif self.isLeftRoot():
            return "<DummyNode>"
        else:
            return "<Node>"
    
    
    