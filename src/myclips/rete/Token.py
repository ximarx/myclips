'''
Created on 23/lug/2012

@author: Francesco Capozzo
'''
import collections
import myclips

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
        
        self._negativeJoinResults = []
        self._nccResults = {}
        self._nccOwner = None
        
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
        
    def delete(self):
        """
        Delete this token and all children
        (without a parent token, all children are
        invalidated)
        """
        self.deleteChildren()    
        
        # remove reference to this token
        # from the creator node
        # (could fail delete isn't called
        # from a parent token invalidation)
        
        # In old version there was an undocumented
        #if not isinstance(self._node, NccPartnerNode):
        myclips.logger.debug("FIXME: add check for NccPartnerNode")
        self._node.removeItem()
        
        # wme could be None if match comes
        # from negative/ncc nodes
        if self.wme is not None:
            self.wme.unlinkToken(self)
            
        # remove reference to the child 
        # from the parent
        if not self.isRoot():
            del self._children[self]
            
        myclips.logger.debug("FIXME: add check for other special cases in token::delete()")
        
    def deleteChildren(self):
        
        # call delete of all children
        # while loop is required (and values must be revalutated
        # everytime because child token reference removal from parent dict
        # must be required by the child token
        # children list is updated at every call
        while len(self._children.values()) > 0:
            self._children.values()[0].delete()
        
    def hasNegativeJoinResults(self):
        return len(self._negativeJoinResults) > 0
        
    def linkNegativeJoinResults(self, njr):
        self._negativeJoinResults.append(njr)
        
    def unlinkNegativeJoinResults(self, njr):
        self._negativeJoinResults.remove(njr)
        
    def hasNccResults(self):
        return (len(self._nccResults) > 0)
        
    def linkNccResult(self, token):
        self._nccResults[token] = token
        token.nccOnwer = self
        
    def unlinkNccResult(self, token):
        del self._nccResults[token]
        token.nccOwner = None
        
    @property
    def nccOwner(self):
        return self._nccOwner
    
    @nccOwner.setter
    def nccOwner(self, owner):
        self._nccOwner = owner
        
    def hasNccOwner(self):
        return (self._nccOwner is not None)
        
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
