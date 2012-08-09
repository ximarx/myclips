'''
Created on 30/lug/2012

@author: Francesco Capozzo
'''
import unittest
from myclips.rete.Network import Network
from myclips.EventsManager import EventsManager
from myclips.listeners import NetworkPlotter
import myclips.parser.Types as types
from myclips.ModulesManager import ModulesManager
from unittest.case import skipIf
import os
import logging
from MyClipsBaseTest import MyClipsBaseTest

#logging.disable(logging.CRITICAL)

@skipIf(os.environ.get('_PLOTTER_', "False") == "False", "")
class NetworkPlotterTest(MyClipsBaseTest):


    def setUp(self):
        self.MM = ModulesManager()
        self.MM.addMainScope()
        self.network = Network(EventsManager())
        NetworkPlotter().install(self.network.eventsManager)

    def tearDown(self):
        self.network.eventsManager.unregisterObserver()

    def test_NetworkPlotting_AlphaAndDummyJoinOnly(self):
        
        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrderedPatternCE([
                        types.Symbol("A"),
                        types.Symbol("B"),
                        types.Symbol("C"),
                    ], self.MM)
            ]))
        
        # manually fire the network ready event
        self.network.eventsManager.fire(EventsManager.E_NETWORK_READY, self.network)
        self.network.eventsManager.fire(EventsManager.E_NETWORK_SHUTDOWN, self.network)

    def test_NetworkPlotting_TemplateAlphaAndDummyJoinOnly(self):
        
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
        
        # manually fire the network ready event
        self.network.eventsManager.fire(EventsManager.E_NETWORK_READY, self.network)
        self.network.eventsManager.fire(EventsManager.E_NETWORK_SHUTDOWN, self.network)

    def test_NetworkPlotting_WithVarBindings(self):
        
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
        
        # manually fire the network ready event
        self.network.eventsManager.fire(EventsManager.E_NETWORK_READY, self.network)
        self.network.eventsManager.fire(EventsManager.E_NETWORK_SHUTDOWN, self.network)


    def test_NetworkPlotting_DefRuleWithOrClause(self):
        
        self.network.addRule(types.DefRuleConstruct("A", self.MM, lhs=[
                types.OrPatternCE([
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
                ])
            ]))
        
        # manually fire the network ready event
        self.network.eventsManager.fire(EventsManager.E_NETWORK_READY, self.network)
        self.network.eventsManager.fire(EventsManager.E_NETWORK_SHUTDOWN, self.network)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    
    unittest.main()
    
