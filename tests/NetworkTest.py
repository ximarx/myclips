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
from myclips.rete.nodes.NegativeJoinNode import NegativeJoinNode
from myclips.rete.nodes.NccNode import NccNode
from myclips.rete.nodes.NccPartnerNode import NccPartnerNode
from myclips.EventsManager import EventsManager
from myclips.Fact import Fact
#from myclips.TemplatesManager import TemplateDefinition, SlotDefinition

# disable all logging from modules
logging.disable(logging.INFO)

fact = Fact

#class fact(object):
#    def __init__(self, v, template=None):
#        self._fact = v
#        self.moduleName = "MAIN"
#        self.templateName = template
#    def __getitem__(self, attr, *argv, **argks):
#        return self._fact[attr]
#    def values(self):
#        return self._fact
    

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
        self.MM = ModulesManager()
        self.MM.addMainScope()
        self.network = Network(eventsManager=EventsManager(),modulesManager=self.MM)
        
#        import sys
#        from myclips.listeners.NetworkBuildPrinter import NetworkBuildPrinter
#        NetworkBuildPrinter(sys.stderr).install(self.network.eventsManager)
        
        
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        #self.printer.uninstall()
        self.network.eventsManager.unregisterObserver()


    def test_AlphaCircuitCompilationOrdered(self):

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


    def test_AlphaCircuitCompilationTemplate(self):

        types.DefTemplateConstruct("aTemplate", self.MM, None, [
                types.SingleSlotDefinition("A"),
                types.SingleSlotDefinition("B"),
                types.SingleSlotDefinition("C")
            ])

        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.TemplatePatternCE("aTemplate", self.MM, [
                        types.SingleFieldLhsSlot("A", types.Symbol("A")),
                        types.SingleFieldLhsSlot("B", types.Symbol("B")),
                        types.SingleFieldLhsSlot("C", types.Symbol("C"))
                    ])
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
        
        
    def test_AlphaMemoryPropagationOrdered(self):
        
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
        

    def test_AlphaMemoryPropagationTemplate(self):
        
        types.DefTemplateConstruct("aTemplate", self.MM, None, [
                types.SingleSlotDefinition("A"),
                types.SingleSlotDefinition("B"),
                types.SingleSlotDefinition("C")
            ])

        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.TemplatePatternCE("aTemplate", self.MM, [
                        types.SingleFieldLhsSlot("A", types.Symbol("A")),
                        types.SingleFieldLhsSlot("B", types.Symbol("B")),
                        types.SingleFieldLhsSlot("C", types.Symbol("C"))
                    ])
            ]))
                
        self.assertIsInstance(self.network._root.children[0].children[0].children[0].children[0].children[0].memory.children[0], JoinNode)
        
        trap = activationCatcher()
        
        self.network._root.children[0].children[0].children[0].children[0].children[0].memory.appendChild(trap)
        
        
        self.network.assertFact(fact({"A": types.Symbol("A"), "B": types.Symbol("B"), "C": types.Symbol("C")}, "aTemplate"))
        
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
        

    def test_NegativeJoinBetaCircuitCompilation(self):
        
        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.Symbol("A"),
                        types.Symbol("B"),
                        types.Symbol("C"),
                    ], self.MM),
                types.NotPatternCE(
                    types.OrderedPatternCE([
                            types.Symbol("C"),
                            types.Symbol("B"),
                            types.Symbol("A"),
                        ], self.MM))
            ]))

        self.assertIsInstance(self.network._root
                                .children[0] #MAIN
                                .children[0] #C
                                .children[0] #B
                                .children[0] #A
                                .children[0] #LEN
                                .memory #AM
                                .children[0], NegativeJoinNode)

    def test_NegativeJoinBetaCircuitTrueCondition(self):
        
        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.Symbol("A"),
                        types.Symbol("B"),
                        types.Symbol("C"),
                    ], self.MM),
                types.NotPatternCE(
                    types.OrderedPatternCE([
                            types.Symbol("C"),
                            types.Symbol("B"),
                            types.Symbol("A"),
                        ], self.MM))
            ]))
        
        trap = activationCatcher()
        
        (self.network._root.children[0] #MAIN
                        .children[0]    #C
                        .children[0]    #B
                        .children[0]    #A
                        .children[0]    #LEN
                        .memory         #AM
                        .children[0]).prependChild(trap)

        self.network.assertFact(fact([types.Symbol("A"), types.Symbol("B"), types.Symbol("C")]))
        
        self.assertTrue(trap.leftCatch)


        
    def test_NegativeJoinBetaCircuitFalseCondition(self):
        
        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.Symbol("A"),
                        types.Symbol("B"),
                        types.Symbol("C"),
                    ], self.MM),
                types.NotPatternCE(
                    types.OrderedPatternCE([
                            types.Symbol("C"),
                            types.Symbol("B"),
                            types.Symbol("A"),
                        ], self.MM))
            ]))

        
        trap = activationCatcher()
        
        (self.network._root.children[0] #MAIN
                        .children[0]    #C
                        .children[0]    #B
                        .children[0]    #A
                        .children[0]    #LEN
                        .memory         #AM
                        .children[0]).prependChild(trap)

        self.network.assertFact(fact([types.Symbol("C"), types.Symbol("B"), types.Symbol("A")]))
        
        self.assertFalse(trap.leftCatch)
        
        self.network.assertFact(fact([types.Symbol("A"), types.Symbol("B"), types.Symbol("C")]))
        
        self.assertFalse(trap.leftCatch)



    def test_NccBetaCircuitCompilation(self):
        
        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.Symbol("A"),
                        types.Symbol("B"),
                        types.Symbol("C"),
                    ], self.MM),
                types.NotPatternCE(
                    types.AndPatternCE([
                        types.OrderedPatternCE([
                                types.Symbol("Z"),
                                types.Symbol("Z"),
                                types.Symbol("Z"),
                            ], self.MM),
                        types.OrderedPatternCE([
                                types.Symbol("W"),
                                types.Symbol("W"),
                                types.Symbol("W"),
                            ], self.MM)
                        ]))
            ]))

        # check main branch
        self.assertIsInstance(self.network._root
                                .children[0] #MAIN
                                .children[-1] #A
                                .children[-1] #B
                                .children[-1] #C
                                .children[-1] #LEN 3
                                .memory #AM
                                .children[-1] #DUMMYJOIN
                                .children[-1] #NCC
                                , NccNode)        

        # check partner branch
        self.assertIsInstance(self.network._root
                                .children[0] #MAIN
                                .children[-2] #Z
                                .children[-1] #Z
                                .children[-1] #Z
                                .children[-1] #LEN 3
                                .memory #AM
                                .children[-1] #DUMMYJOIN
                                .children[-1] #BETA
                                .children[-1] #JOIN
                                .children[-1]
                                , NccPartnerNode)        

        # check if nccPartner is linked to nccNode
        self.assertEqual(self.network._root
                                .children[0] #MAIN
                                .children[-2] #Z
                                .children[-1] #Z
                                .children[-1] #Z
                                .children[-1] #LEN 3
                                .memory #AM
                                .children[-1] #DUMMYJOIN
                                .children[-1] #BETA
                                .children[-1] #JOIN
                                .children[-1].nccNode
                                ,
                        self.network._root
                                .children[0] #MAIN
                                .children[-1] #A
                                .children[-1] #B
                                .children[-1] #C
                                .children[-1] #LEN 3
                                .memory #AM
                                .children[-1] #DUMMYJOIN
                                .children[-1] #NCC
                        )        

        # check if NccNode is linked to NccPartner
        self.assertEqual(self.network._root
                                .children[0] #MAIN
                                .children[-2] #Z
                                .children[-1] #Z
                                .children[-1] #Z
                                .children[-1] #LEN 3
                                .memory #AM
                                .children[-1] #DUMMYJOIN
                                .children[-1] #BETA
                                .children[-1] #JOIN
                                .children[-1]
                                ,
                        self.network._root
                                .children[0] #MAIN
                                .children[-1] #A
                                .children[-1] #B
                                .children[-1] #C
                                .children[-1] #LEN 3
                                .memory #AM
                                .children[-1] #DUMMYJOIN
                                .children[-1].partner
                        )        


    def test_NccBetaCircuitPropagationBothSubMissing(self):
        
        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.Symbol("A"),
                        types.Symbol("B"),
                        types.Symbol("C"),
                    ], self.MM),
                types.NotPatternCE(
                    types.AndPatternCE([
                        types.OrderedPatternCE([
                                types.Symbol("Z"),
                                types.Symbol("Z"),
                                types.Symbol("Z"),
                            ], self.MM),
                        types.OrderedPatternCE([
                                types.Symbol("W"),
                                types.Symbol("W"),
                                types.Symbol("W"),
                            ], self.MM)
                        ]))
            ]))

        trap = activationCatcher()
        
        (self.network._root.children[0] #MAIN
                            .children[-1] #A
                            .children[-1] #B
                            .children[-1] #C
                            .children[-1] #LEN 3
                            .memory #AM
                            .children[-1] #DUMMYJOIN
                            .children[-1] #NCC
                            ).prependChild(trap)

        self.network.assertFact(fact([types.Symbol("A"), types.Symbol("B"), types.Symbol("C")]))
        
        self.assertTrue(trap.leftCatch)
        

    def test_NccBetaCircuitPropagationSecondSubMissing(self):
        
        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.Symbol("A"),
                        types.Symbol("B"),
                        types.Symbol("C"),
                    ], self.MM),
                types.NotPatternCE(
                    types.AndPatternCE([
                        types.OrderedPatternCE([
                                types.Symbol("Z"),
                                types.Symbol("Z"),
                                types.Symbol("Z"),
                            ], self.MM),
                        types.OrderedPatternCE([
                                types.Symbol("W"),
                                types.Symbol("W"),
                                types.Symbol("W"),
                            ], self.MM)
                        ]))
            ]))

        trap = activationCatcher()
        
        (self.network._root.children[0] #MAIN
                            .children[-1] #A
                            .children[-1] #B
                            .children[-1] #C
                            .children[-1] #LEN 3
                            .memory #AM
                            .children[-1] #DUMMYJOIN
                            .children[-1] #NCC
                            ).prependChild(trap)

        self.network.assertFact(fact([types.Symbol("Z"), types.Symbol("Z"), types.Symbol("Z")]))

        self.network.assertFact(fact([types.Symbol("A"), types.Symbol("B"), types.Symbol("C")]))
        
        self.assertTrue(trap.leftCatch)
        
    def test_NccBetaCircuitPropagationFirstSubMissing(self):
        
        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.Symbol("A"),
                        types.Symbol("B"),
                        types.Symbol("C"),
                    ], self.MM),
                types.NotPatternCE(
                    types.AndPatternCE([
                        types.OrderedPatternCE([
                                types.Symbol("Z"),
                                types.Symbol("Z"),
                                types.Symbol("Z"),
                            ], self.MM),
                        types.OrderedPatternCE([
                                types.Symbol("W"),
                                types.Symbol("W"),
                                types.Symbol("W"),
                            ], self.MM)
                        ]))
            ]))

        trap = activationCatcher()
        
        (self.network._root.children[0] #MAIN
                            .children[-1] #A
                            .children[-1] #B
                            .children[-1] #C
                            .children[-1] #LEN 3
                            .memory #AM
                            .children[-1] #DUMMYJOIN
                            .children[-1] #NCC
                            ).prependChild(trap)

        self.network.assertFact(fact([types.Symbol("W"), types.Symbol("W"), types.Symbol("W")]))

        self.network.assertFact(fact([types.Symbol("A"), types.Symbol("B"), types.Symbol("C")]))
        
        self.assertTrue(trap.leftCatch)
        
    def test_NccBetaCircuitNotPropagation(self):
        
        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.Symbol("A"),
                        types.Symbol("B"),
                        types.Symbol("C"),
                    ], self.MM),
                types.NotPatternCE(
                    types.AndPatternCE([
                        types.OrderedPatternCE([
                                types.Symbol("Z"),
                                types.Symbol("Z"),
                                types.Symbol("Z"),
                            ], self.MM),
                        types.OrderedPatternCE([
                                types.Symbol("W"),
                                types.Symbol("W"),
                                types.Symbol("W"),
                            ], self.MM)
                        ]))
            ]))

        trap = activationCatcher()
        
        (self.network._root.children[0] #MAIN
                            .children[-1] #A
                            .children[-1] #B
                            .children[-1] #C
                            .children[-1] #LEN 3
                            .memory #AM
                            .children[-1] #DUMMYJOIN
                            .children[-1] #NCC
                            ).prependChild(trap)

        self.network.assertFact(fact([types.Symbol("Z"), types.Symbol("Z"), types.Symbol("Z")]))

        self.network.assertFact(fact([types.Symbol("W"), types.Symbol("W"), types.Symbol("W")]))

        self.network.assertFact(fact([types.Symbol("A"), types.Symbol("B"), types.Symbol("C")]))
        
        self.assertFalse(trap.leftCatch)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()