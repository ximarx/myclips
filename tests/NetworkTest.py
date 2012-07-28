'''
Created on 25/lug/2012

@author: Francesco Capozzo
'''
import unittest
from myclips.rete.Network import Network
import myclips.parser.Types as types
from myclips.ModulesManager import ModulesManager
from myclips.rete.WME import WME
from myclips.rete.nodes.PropertyTestNode import PropertyTestNode
from myclips.rete.nodes.RootNode import RootNode
from myclips.rete.nodes.AlphaMemory import AlphaMemory
import logging
from myclips.rete.nodes.JoinNode import JoinNode
from myclips.rete.AlphaInput import AlphaInput
from myclips.rete.BetaInput import BetaInput

# disable all logging from modules
logging.disable(logging.INFO)

class fact(object):
    def __init__(self, v):
        self._fact = v
        self.moduleName = "MAIN"
    def __getitem__(self, attr, *argv, **argks):
        return self._fact[attr]
    def values(self):
        return self._fact
    

class activationCatcher(AlphaInput, BetaInput):
    def __init__(self):
        self.leftCatch = False
        self.rightCatch = False
        
    def rightActivation(self, wme):
        self.rightCatch = True
        
    def leftActivation(self, token, wme):
        self.leftCatch = True
    
    

class Test(unittest.TestCase):


    def setUp(self):
        self.network = Network()
        self.MM = ModulesManager()
        self.MM.addMainScope()


    def test_AlphaCircuitCompilation(self):

        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.Symbol("A"),
                        types.Symbol("B"),
                        types.Symbol("C"),
                    ], self.MM)
            ]))
        
        self.assertIsInstance(self.network._root, RootNode)
        self.assertIsInstance(self.network._root.children[0], PropertyTestNode)
        self.assertIsInstance(self.network._root.children[0].children[0], PropertyTestNode)
        self.assertIsInstance(self.network._root.children[0].children[0].children[0], PropertyTestNode)
        self.assertIsInstance(self.network._root.children[0].children[0].children[0].children[0], PropertyTestNode)
        self.assertIsInstance(self.network._root.children[0].children[0].children[0].children[0].children[0], PropertyTestNode)
        self.assertIsInstance(self.network._root.children[0].children[0].children[0].children[0].children[0].memory, AlphaMemory)
        self.assertIsInstance(self.network._root.children[0].children[0].children[0].children[0].children[0].memory.children[0], JoinNode)

    def test_DummyJoinNodeCreationAfterFirstPatternCE(self):

        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.Symbol("A"),
                        types.Symbol("B"),
                        types.Symbol("C"),
                    ], self.MM)
            ]))
        
        self.assertIsInstance(self.network._root.children[0].children[0].children[0].children[0].children[0].memory.children[0], JoinNode)
        self.assertTrue(self.network._root.children[0].children[0].children[0].children[0].children[0].memory.children[0].isLeftRoot())



    def test_AssertFact(self):

        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.Symbol("A"),
                        types.Symbol("B"),
                        types.Symbol("C"),
                    ], self.MM)
            ]))

        self.network.assertFact(fact([types.Symbol("A"), types.Symbol("B"), types.Symbol("C")]))

        self.assertEqual(len(self.network._root.children[0].children[0].children[0].children[0].children[0].memory.items), 1)
        self.assertIsInstance(self.network._root.children[0].children[0].children[0].children[0].children[0].memory.items[0], WME)
        self.assertIsInstance(self.network._root.children[0].children[0].children[0].children[0].children[0].memory.items[0].fact, fact)
        self.assertIsInstance(self.network._root.children[0].children[0].children[0].children[0].children[0].memory.items[0].fact[0], types.Symbol)


    def test_DummyJoinNodePropagation(self):
        
        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.Symbol("A"),
                        types.Symbol("B"),
                        types.Symbol("C"),
                    ], self.MM)
            ]))
        
        self.assertIsInstance(self.network._root.children[0].children[0].children[0].children[0].children[0].memory.children[0], JoinNode)
        
        trap = activationCatcher()
        
        self.network._root.children[0].children[0].children[0].children[0].children[0].memory.children[0].appendChild(trap)
        
        self.network.assertFact(fact([types.Symbol("A"), types.Symbol("B"), types.Symbol("C")]))
        
        self.assertTrue(trap.leftCatch)
        
        
    def test_AlphaMemoryPropagation(self):
        
        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.Symbol("A"),
                        types.Symbol("B"),
                        types.Symbol("C"),
                    ], self.MM)
            ]))
        
        self.assertIsInstance(self.network._root.children[0].children[0].children[0].children[0].children[0].memory.children[0], JoinNode)
        
        trap = activationCatcher()
        
        self.network._root.children[0].children[0].children[0].children[0].children[0].memory.appendChild(trap)
        
        
        self.network.assertFact(fact([types.Symbol("A"), types.Symbol("B"), types.Symbol("C")]))
        
        self.assertTrue(trap.rightCatch)
        

    def test_JoinNodeVarBindingOnOrderedPatternCE(self):
        
        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.Symbol("A"),
                        types.SingleFieldVariable(types.Symbol("varA")),
                        types.Symbol("C"),
                    ], self.MM),
                types.OrderedPatternCE([
                        types.SingleFieldVariable(types.Symbol("varA")),
                        types.Symbol("A"),
                        types.Symbol("C"),
                    ], self.MM)
            ]))
        
        self.assertIsInstance(self.network._root.children[0].children[0].children[0].children[0].memory.children[0], JoinNode)
        
        self.assertFalse(self.network._root.children[0].children[0].children[0].children[0].memory.children[0].isLeftRoot())
        
        trap = activationCatcher()
        
        self.network._root.children[0].children[0].children[0].children[0].memory.children[0].appendChild(trap)
        
        self.network.assertFact(fact([types.Symbol("A"), types.Symbol("B"), types.Symbol("C")]))

        f = fact([types.Symbol("B"), types.Symbol("A"), types.Symbol("C")])        
        self.network.assertFact(f)

       
        self.assertTrue(trap.leftCatch)
        

    def test_JoinNodeVarBindingOnOrderedPatternCEWithNegativeTermOverVariable(self):
        
        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.Symbol("A"),
                        types.SingleFieldVariable(types.Symbol("varA")),
                        types.Symbol("C"),
                    ], self.MM),
                types.OrderedPatternCE([
                        types.NegativeTerm(types.SingleFieldVariable(types.Symbol("varA")), True),
                        types.UnnamedSingleFieldVariable(),
                        types.Symbol("C"),
                    ], self.MM)
            ]))
        
        self.assertIsInstance(self.network._root.children[0].children[0].children[0].memory.children[0], JoinNode)
        
        self.assertFalse(self.network._root.children[0].children[0].children[0].memory.children[0].isLeftRoot())
        
        trap = activationCatcher()
        
        self.network._root.children[0].children[0].children[0].memory.children[0].appendChild(trap)
        
        f = fact([types.Symbol("A"), types.Symbol("B"), types.Symbol("C")])
                
        self.network.assertFact(f)
       
        self.assertTrue(trap.leftCatch)
        

    def test_JoinNodeIntraElementVarBindingTestInBetaNetwork(self):
        
        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.SingleFieldVariable(types.Symbol("varA")),
                        types.SingleFieldVariable(types.Symbol("varA")),
                        types.Symbol("C"),
                    ], self.MM)
            ]))
        
        self.assertIsInstance(self.network._root.children[0].children[0].children[0].memory.children[0], JoinNode)
        
        self.assertTrue(self.network._root.children[0].children[0].children[0].memory.children[0].isLeftRoot())
        
        trap = activationCatcher()
        
        self.network._root.children[0].children[0].children[0].memory.children[0].appendChild(trap)
        
        f = fact([types.Symbol("A"), types.Symbol("B"), types.Symbol("C")])
        self.network.assertFact(f)
        
        self.assertFalse(trap.leftCatch)

        f = fact([types.Symbol("A"), types.Symbol("A"), types.Symbol("C")])
        self.network.assertFact(f)
        
        self.assertTrue(trap.leftCatch)
        
        
    def test_AlphaCircuitWithMultifield(self):
        
        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.Symbol("A"),
                        types.MultiFieldVariable(types.Symbol("varB")),
                        types.Symbol("C"),
                    ], self.MM)
            ]))
        
        self.assertIsInstance(self.network._root.children[0].children[0].children[0].memory, AlphaMemory)
        
        #self.assertTrue(self.network._root.children[0].children[0].memory.children[0].isLeftRoot())
        
        trap = activationCatcher()
        
        self.network._root.children[0].children[0].children[0].memory.prependChild(trap)
        
        f = fact([types.Symbol("A"), types.Symbol("B"), types.Symbol("B2"), types.Symbol("C")])
        self.network.assertFact(f)
       
        self.assertNotEqual(len(self.network._root.children[0].children[0].children[0].memory.items), 0)
        
        self.assertTrue(trap.rightCatch)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()