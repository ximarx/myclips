'''
Created on 30/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.Node import Node
from myclips.rete.BetaInput import BetaInput
from myclips.rete.Memory import Memory
import myclips

class PNode(Node, BetaInput, Memory):
    '''
    classdocs
    '''


    def __init__(self, ruleName, leftParent, network, orClauseCount=None, rhs=None, properties=None):
        '''
        Constructor
        '''
        self._ruleName = ruleName + (("~"+str(orClauseCount)) if orClauseCount is not None else "")
        self._isMain = (orClauseCount is None)
        self._network = network
        self._rhs = rhs
        self._linkedPNode = []
        self._properties = {"salience": 0, "auto-focus": False} if properties is None or not isinstance(properties, dict) else properties

        Node.__init__(self, leftParent=leftParent)
        Memory.__init__(self)


    def leftActivation(self, token, wme):
        myclips.logger.debug("FIXME: PNode left activation NIY. token=%s, wme=%s", token, wme)
        
    def delete(self):
        if self.isMain:
            for linkedNode in self._linkedPNode:
                linkedNode.delete()
                
            self._linkedPNode = []
            
        Memory.delete(self)
        Node.delete(self)

    def linkOrClause(self, pnode):
        self._linkedPNode.append(pnode)

    @property
    def isMain(self):
        return self._isMain
    
    @property
    def ruleName(self):
        return self._ruleName
    
    @property
    def mainRuleName(self):
        return self.ruleName.rsplit("~", 2)[0]
    
    def __hash__(self):
        return hash(self.ruleName)
    
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.ruleName == other.ruleName and
                self.isMain == other.isMain and
                self.mainRuleName == other.mainRuleName and
                self.getSalience() == other.getSalience() and
                self.isAutoFocus() == other.isAutoFocus() and
                self.leftParent == other.leftParent and
                self.rhs == other.rhs)
        
    def __neq__(self, other):
        return not self.__eq__(other)
    
    def getSalience(self):
        return int(self.getProperty("salience", 0))
    
    def isAutoFocus(self):
        return bool(self.getProperty("auto-focus", False))
    
    def getProperty(self, propName, defaultValue):
        return self._properties.get(propName, defaultValue)
    
    def __str__(self, *args, **kwargs):
        return "<PNode: %s>"%self.ruleName
    
    def __repr__(self, *args, **kwargs):
        return self.__str__()
    