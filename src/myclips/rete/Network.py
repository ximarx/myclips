'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.Agenda import Agenda
import myclips.parser.Types as types
import myclips
from myclips.MyClipsException import MyClipsBugException
from myclips.rete.nodes.PropertyTestNode import PropertyTestNode
from myclips.rete.tests.ScopeTest import ScopeTest
from myclips.rete.tests.ConstantValueAtIndexTest import ConstantValueAtIndexTest
from myclips.rete.tests.NegativeAlphaTest import NegativeAlphaTest
from myclips.rete.nodes.AlphaMemory import AlphaMemory
from myclips.rete.nodes.RootNode import RootNode
from myclips.rete.WME import WME
from myclips.rete.nodes.BetaMemory import BetaMemory

class Network(object):
    '''
    Rete network main object
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._root = RootNode(self)
        self._agenda = Agenda()
        self._rules = {}
        self._facts = {}
        
        
    def assertFact(self, fact):
        self._root.rightActivation(WME(0, fact))
        
    def retractFact(self, fact):
        pass
    
    def addRule(self, defrule):
        lastNode = self._makeNetwork(None, defrule.lhs, None, None)
        return lastNode
        #pnode = PNode(lastNode)
    
    def removeRule(self, pnode):
        pass
    
    def reset(self):
        pass
    
    def clear(self):
        pass
    
    @property
    def agenda(self):
        return self._agenda
        
    @property
    def facts(self):
        return self._facts

    @property
    def rules(self):
        return self._rules


    def _makeNetwork(self, node, patterns, prevPatterns=None, variables=None, testsQueue=None):
        
        variables = {} if variables is None else variables
        prevPatterns = [] if prevPatterns is None else prevPatterns
        testsQueue = [] if testsQueue is None else testsQueue 
        
        for (pIndex, patternCE) in enumerate(patterns):
            
            # get the pattern type:
            if isinstance(patternCE, (types.TemplatePatternCE, 
                                      types.AssignedPatternCE, 
                                      types.OrderedPatternCE)):
                
                # if patternCE is assigned, i need to propagate
                # alpha creation with the inner pattern,
                # not with the main assigned.
                # i use the assigned only to store info about variable
                # use old way to store variables coordinates, waiting for a new one
                if isinstance(patternCE, types.AssignedPatternCE):
                    variables[patternCE.variable.evaluate()] = (pIndex, None)
                    patternCE = patternCE.pattern
                
                # requires a simple alpha circuit,
                # then a join + beta node if needed (beta join circuit)
                alphaMemory = self._makeAlphaCircuit(patternCE, testsQueue)
                node = self._makeBetaJoinCircuit(node, alphaMemory, patternCE, prevPatterns, variables)
                
                
            elif isinstance(patternCE, types.NotPatternCE):
                # need to check inside the pattern
                # if inside a not-ce there is a and-ce
                # i need to build a ncc
                
                if isinstance(patternCE.pattern, types.AndPatternCE):
                    # that's it: ncc required
                    pass
                
                else:
                    # a simple negative join node is required
                    pass
                
            elif isinstance(patternCE, types.TestPatternCE):
                # a special filter must be applied to
                # the circuit
                pass
                
            #elif isinstance(patternCE, types.OrPatternCE):
                # need to add support for orCE
                # pass
        
            #elif isinstance(patternCE, types.AndPatternCE):
                # need to add support for andCE
                # pass  
            
            prevPatterns.append(patternCE)
            
        return node
            
    def _makeAlphaCircuit(self, patternCE, testQueue):
            
            # first i need to check the type of the patternCE
            # to create the correct list of tests
            
            lastCircuitNode = self._root
            
            if isinstance(patternCE, types.TemplatePatternCE):
                pass
            elif isinstance(patternCE, types.OrderedPatternCE):
                
                # first thing to do is add a filter per-module
                # ordered facts are visible only in the module
                # who assert them
                lastCircuitNode = self._shareNode_PropertyTestNode(lastCircuitNode, [ScopeTest(patternCE.scope.moduleName)])
                
                # this is easy to do:
                # first field is a symbol for parser constraints, but manually
                # submitted rules could have any types of value as first
                for (fieldIndex, fieldConstraint) in enumerate(patternCE.constraints):
                    
                    # ordered fact constraint could be:
                    #    BaseParsedType: (usually the first field is always a Symbol if rule is parsed)
                    #    Constraint<Term<BaseParsedType>
                    #    ConnectedConstraints<Term<BaseParsedType>, [[#connective, <Term>]*]>
                    # 
                    # Strategy is to check if is constraints first. If it is,
                    # replace fieldConstraints value with constraint value and continue
                    #
                    # then check for Term (Positive/Negative) and change tests for it
                    
                    isPositive = True
                    
                    if isinstance(fieldConstraint, types.Constraint):
                        # reduce Constraint to his content
                        fieldConstraint = fieldConstraint.constraint
                        
                    if isinstance(fieldConstraint, types.ConnectedConstraint):
                        # reduce ConnectedConstraint to his main constraint
                        myclips.logger.error("FIXME: Connected contraints alternative values ignored: %s", fieldConstraint.connectedConstraints)
                        fieldConstraint = fieldConstraint.constraint
                        
                    if isinstance(fieldConstraint, types.PositiveTerm):
                        fieldConstraint = fieldConstraint.term
                    
                    if isinstance(fieldConstraint, types.NegativeTerm):
                        isPositive = False
                        fieldConstraint = fieldConstraint.term
                        
                    # not fieldConstraint is a BaseParsedType | Variable
                    # only check for BaseParsedType, variables ignored
                    if isinstance(fieldConstraint, types.BaseParsedType):
                        # share or create a property test node for each type/value at index
                        tests = [ConstantValueAtIndexTest(fieldIndex, fieldConstraint)]
                        
                        # if this is a NegativeTest, i need to reverse all tests
                        if not isPositive:
                            tests = [NegativeAlphaTest(t) for t in tests]
                            
                        lastCircuitNode = self._shareNode_PropertyTestNode(lastCircuitNode, tests)
                        
            else:
                myclips.logger.critical("Unknown patternCE type: %s", patternCE.__class__.__name__)
                raise MyClipsBugException("Unknown patternCE type: %s"%patternCE.__class__.__name__)
            
            # Here i've built all property test node
            # it's time to link an alpha memory at the end of them
            
            lastCircuitNode = self._shareNode_AlphaMemoryNode(lastCircuitNode)
            
            return lastCircuitNode
        
    def _makeBetaJoinCircuit(self, lastBetaCircuitNode, alphaMemory, patternCE, prevPatterns, variables):
        
        if lastBetaCircuitNode != None:
            lastBetaCircuitNode = self._shareNode_BetaMemory(lastBetaCircuitNode)
            
        # build tests for join node
        

    def _shareNode_AlphaMemoryNode(self, lastCircuitNode):
        """
        Try to share an AlphaMemoryNode available in the circuite
        if possible, otherwise create a new one and add it
        in the network
        
        @param lastCircuitNode: the node where the alpha memory should be linked
        @type lastCircuitNode: PropertyTestNode
        @return: a shared or a new AlphaMemory
        @rtype: AlphaMemory
        """
        
        assert isinstance(lastCircuitNode, PropertyTestNode)

        # if the last node has already a memory linked,
        # just use it        
        if lastCircuitNode.hasMemory():
            return lastCircuitNode.memory
        
        # otherwise create a new one and return it
        memory = AlphaMemory(lastCircuitNode)
        lastCircuitNode.memory = memory
        
        myclips.logger.info("New node: %s", memory)
        myclips.logger.info("Linked node: %s to %s", memory, lastCircuitNode)
        
        # update the node
        lastCircuitNode.updateChild(memory)
        
        return memory

            
    def _shareNode_PropertyTestNode(self, lastCircuitNode, tests):
        
        if lastCircuitNode != None:
            for child in lastCircuitNode.children:
                if isinstance(child, PropertyTestNode)\
                    and child.tests == tests:
                    # found a node with same contraints
                    # i can share it
                    return child
        
        # if a checked all children and found nothing
        # i need to create a new node for it
        newChild = PropertyTestNode(lastCircuitNode, tests)
        # maybe i could move this code inside the constructor
        lastCircuitNode.addChild(newChild)
        
        myclips.logger.info("New node: %s", newChild)
        myclips.logger.info("Linked node: %s to %s", newChild, lastCircuitNode)
        
        return newChild
    
    def _shareNode_BetaMemory(self, lastCircuitNode):
        
        # beta node are needed only if there is a parent node
        # otherwise dummy node only
        if lastCircuitNode is None:
            return lastCircuitNode
        
        # try to share the beta if possible    
        for child in lastCircuitNode.children:
            if isinstance(child, BetaMemory):
                return child
            
         
        # otherwise make a new one
        newChild = BetaMemory(lastCircuitNode)
        lastCircuitNode.prependChild(newChild)    
            
        myclips.logger.info("New node: %s", newChild)
        myclips.logger.info("Linked node: %s to %s", newChild, lastCircuitNode)
        
        return newChild
            