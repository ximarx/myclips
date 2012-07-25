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
from myclips.rete.tests.VariableBindingTest import VariableBindingTest
from myclips.rete.nodes.JoinNode import JoinNode

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
                    variables[patternCE.variable.evaluate()] = {"patternIndex": pIndex,
                                                                "positionIndex": []}
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
                myclips.logger.error("FIXME: TemplatePatternCE ignored: %s", patternCE)
                
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
        tests = []
        
        if isinstance(patternCE, types.TemplatePatternCE):
            iterateOver = [(lhsSlot.slotName, lhsSlot.slotValue) for lhsSlot in patternCE.templateSlots]
            
        elif isinstance(patternCE, types.OrderedPatternCE):
            iterateOver = enumerate(patternCE.constraints)
        
        for (index, value) in iterateOver:
            
            # special case: multifield
            if isinstance(value, list):
                pass
            else:
                if isinstance(value, types.Constraint):
                    value = value.constraint
                
                if isinstance(value, types.ConnectedConstraint):
                    myclips.logger.error("FIXME: Connected contraints alternative values ignored in join tests: %s", value.connectedConstraints)
                    value = value.constraint
                    
                if isinstance(value, types.Term):
                    myclips.logger.error("FIXME: Possible Negative term ignored in join tests: %s")
                    value = value.term

                # unnamed variables doesn't need join test constraints
                # they are used only as anonymous placeholder
                # to force the existence of an item at an index
                # not to make consistency binding
                if isinstance(value, (types.SingleFieldVariable, types.MultiFieldVariable) ):
                    # found variable
                    # check if a binding test is needed
                    if variables.has_key(value.evaluate()):
                        # i've already found this variable earlier
                        # to i need to create a test to make sure that
                        # values are valid for both variable places
                        patternIndex = variables[value.evaluate()]["patternIndex"]
                        positionIndex = variables[value.evaluate()]["positionIndex"]
                        
                        test = VariableBindingTest(wmePositionIndex=[index],
                                                            tokenRelativeIndex=len(prevPatterns) - patternIndex,
                                                            tokenPositionIndex=positionIndex)
                        
                        tests.append(test)
                    else:
                        # i never found this variable before
                        # so i need to create a new definition
                        # and set the location where
                        # i found it
                        variables[value.evaluate()] = {"patternIndex": len(prevPatterns), # this is the position of the pattern in the lhs
                                                       "positionIndex": [index]} # this is the position in the pattern of the slot/index
         
        return self._shareNode_JoinNode(lastBetaCircuitNode, alphaMemory, tests )           
        
        

    def _shareNode_AlphaMemoryNode(self, lastCircuitNode):
        """
        Try to share an AlphaMemoryNode available in the circuit
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
        
        # update the node to synch the beta memory
        # status to the network status
        lastCircuitNode.updateChild(newChild)   
            
        myclips.logger.info("New node: %s", newChild)
        myclips.logger.info("Linked node: %s to %s", newChild, lastCircuitNode)
        
        return newChild
    
    def _shareNode_JoinNode(self, lastCircuitNode, alphaMemory, tests):
            
        # check if i can share looking at beta network first
        if lastCircuitNode is not None:
            
            for child in lastCircuitNode.children:
                
                # i can't use isinstance, child must be exactly a JoinNode
                # otherwise negative node could be shared and this is a problem
                if (child.__class__ == JoinNode
                    # is a join node
                    and child.rightParent == alphaMemory
                        # alpha memory is the same
                        and child.tests == tests):
                            # tests are the same too
                    
                    # i can share the node
                    return child
        
        else:
            # try to share node looking at the alphaMemory
            # this could allow to share dummy join nodes
            for child in alphaMemory.children:
                # i can't use isinstance, child must be exactly a JoinNode
                # otherwise negative node could be shared and this is a problem
                if (child.__class__ == JoinNode
                    # is a join node
                    and child.isLeftRoot()
                        # like the node i will create, this one is left dummy
                        and child.tests == tests):
                            # tests are the same too
                    
                    # i can share the node
                    return child
            
        # i can't share an old node
        # it's time to create a new one
        
        newChild = JoinNode(rightParent=alphaMemory, leftParent=lastCircuitNode, tests=tests)
        # link the new join to the right alpha memory
        alphaMemory.prependChild(newChild)
        
        if lastCircuitNode is not None:
            # link the join node to the parent
            lastCircuitNode.prependChild(newChild)
            # it's useless to update a leaf join node
            # even if it find matches
            # it has no children to propage the activation
        
        
        myclips.logger.info("New node: %s", newChild)
        myclips.logger.info("Right-linked node: %s to %s", newChild, alphaMemory)
        myclips.logger.info("Left-linked node: %s to %s", newChild, lastCircuitNode)
        
        
        return newChild