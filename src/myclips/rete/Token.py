'''
Created on 23/lug/2012

@author: Francesco Capozzo
'''
import collections

class Token(object):
    '''
    classdocs
    '''


    def __init__(self, node, parentToken = None, wme = None):
        '''
        Constructor
        '''
        
        self._node = node # node is the token maker who creates this token
        self._parent = parentToken # the parent token of this one (or None if root)
        self._wme = wme # the wme that combine with parent token to create a new match
        
        # use hashString as an id for the token. All wmes in the token (and parents)
        #     gave a contribute for hash creation
        # hashString = parentHashString,wmeFactId if parent != None and wme != None
        #    else    = parentHashString,, if wme == None
        #    else    = wmeFactId if parent == None
        #    else    = "" if both parent and wme == None
        self._hashString = (",".join([parentToken.hashString, str(wme.factId) if wme is not None else ""]) if not self.isRoot()
                                else str(wme.factId) if wme is not None else "")
        
        # for faster child removal
        # i can use a dict, using token.hash for index 
        self._children = {}
        
        
        # IF THIS ISN'T A ROOT TOKEN
        # at the end of token creation, i have to 
        # take care of references creation
        # between:
        #    1) this ---> parent (self._parent) [DONE]
        #    2) parent ---> this (parent._children) [TO BE DONE]
        if not self.isRoot():
            self._parent._children[self] = self
        
        # for tree-based token/wme removal, i need to store a reference
        # to this token in the wme that has a part in token creation
        if wme is not None:
            wme.linkToken(self)
            
        
        
    def isRoot(self):
        """
        Check if the token has no parent
        @rtype: Boolean
        """
        return (self.parent == None)
    
    @property
    def parent(self):
        return self._parent
    
    def linearize(self, includeNone=True):
        current = self
        wmes = collections.deque()
        while not current.isRoot:
            if includeNone or current.wme != None:
                wmes.appendLeft(current.wme)
            current = current.parent
        
        return list(wmes)
        
    @property
    def wme(self):
        return self.wme
    
    @property
    def hashString(self):
        return self._hashString

    def __hash__(self, *args, **kwargs):
        return hash(self.hashString)
    
    def __eq__(self, other):
        return (isinstance(other, Token) and self.hashString == other.hashString)
    
    def __neq__(self, other):
        return not self.__eq__(other) 
    
#    @wme.setter
#    def wme(self, newWME):
#        self._wme = newWME

#    @parent.setter
#    def parent(self, newParent):
#        self._parent = newParent
