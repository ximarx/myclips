'''
Created on 03/feb/2013

@author: Francesco Capozzo
'''
import unittest
import logging
from MyClipsBaseTest import MyClipsBaseTest
from myclips.facts.OrderedFact import OrderedFact
from myclips.facts.TemplateFact import TemplateFact
from myclips.facts.Fact import FactLengthNotComputableException

# disable all logging from modules
#logging.disable(logging.CRITICAL)

class FactsTest(MyClipsBaseTest):

    def test_OrderedFact_Creation(self):
        
        fact = OrderedFact([1,2,3], "MAIN")
        self.assertIsInstance(fact, OrderedFact)

    def test_OrderedFact_WrongValuesTypeIsTheSameOfEmptyList(self):
        
        fact1 = OrderedFact({}, "MAIN")
        fact2 = OrderedFact("STRING", "MAIN")
        fact3 = OrderedFact([], "MAIN")
        
        self.assertEqual(fact1, fact3)
        self.assertEqual(fact2, fact3)
        self.assertEqual(fact1, fact2)


    def test_OrderedFact_SameInfosIsSameFact(self):
        
        fact1 = OrderedFact([1,2,3], "MAIN")
        fact2 = OrderedFact([1,2,3], "MAIN")
        
        self.assertEqual(fact1, fact2)
        
    def test_OrderedFact_SameInfoButModuleIsNotSameFact(self):
        
        fact1 = OrderedFact([1,2,3], "MAIN")
        fact2 = OrderedFact([1,2,3], "NOT-MAIN")
        
        self.assertNotEqual(fact1, fact2)


    def test_OrderedFact_SameInfoButAListValueIsNotSameFact_1(self):
        
        fact1 = OrderedFact([1,2,3], "MAIN")
        fact2 = OrderedFact([1,2,3,4], "MAIN")
        
        self.assertNotEqual(fact1, fact2)

    def test_OrderedFact_SameInfoButAListValueIsNotSameFact_2(self):
        
        fact1 = OrderedFact([1,2,3,4], "MAIN")
        fact2 = OrderedFact([1,2,3], "MAIN")
        
        self.assertNotEqual(fact1, fact2)

    def test_OrderedFact_VectorAccessor(self):
        fact = OrderedFact([1,2,3])

        self.assertTrue(fact.values[0] == fact[0])
        self.assertTrue(fact.values[1] == fact[1])
        self.assertTrue(fact.values[2] == fact[2])

    def test_OrderedFact_FactLenghtIsTheLenghtOfValuesArray(self):
        fact = OrderedFact([1,2,3])

        self.assertEqual(len(fact), len(fact.values))
        

    def test_TemplateFact_Creation(self):
        
        fact = TemplateFact("A", {"a":0, "b":1}, "MAIN")
        self.assertIsInstance(fact, TemplateFact)

    def test_TemplateFact_WrongValuesTypeIsTheSameOfEmptyDict(self):
        
        fact1 = TemplateFact("A", {}, "MAIN")
        fact2 = TemplateFact("A", "STRING", "MAIN")
        fact3 = TemplateFact("A", [], "MAIN")
        
        self.assertEqual(fact1, fact3)
        self.assertEqual(fact2, fact3)
        self.assertEqual(fact1, fact2)

    def test_TemplateFact_SameInfosIsSameFact(self):
        
        fact1 = TemplateFact("A", {"a":0, "b":1}, "MAIN")
        fact2 = TemplateFact("A", {"a":0, "b":1}, "MAIN")
        
        self.assertEqual(fact1, fact2)
        
    def test_TemplateFact_SameInfoButModuleIsNotSameFact(self):
        
        fact1 = TemplateFact("A", {"a":0, "b":1}, "MAIN")
        fact2 = TemplateFact("A", {"a":0, "b":1}, "NOT-MAIN")
        
        self.assertNotEqual(fact1, fact2)

    def test_TemplateFact_SameInfoButTemplateNameIsNotSameFact(self):
        
        fact1 = TemplateFact("A", {"a":0, "b":1}, "MAIN")
        fact2 = TemplateFact("B", {"a":0, "b":1}, "MAIN")
        
        self.assertNotEqual(fact1, fact2)


    def test_TemplateFact_SameInfoButADictValueIsNotSameFact_1(self):
        
        fact1 = TemplateFact("A", {"a":0, "b":1}, "MAIN")
        fact2 = TemplateFact("A", {"a":0, "b":2}, "MAIN")
        
        self.assertNotEqual(fact1, fact2)
        
    def test_TemplateFact_SameInfoButADictValueIsNotSameFact_2(self):
        
        fact1 = TemplateFact("A", {"a":0, "b":2}, "MAIN")
        fact2 = TemplateFact("A", {"a":0, "b":1}, "MAIN")
        
        self.assertNotEqual(fact1, fact2)
        

    def test_TemplateFact_SameInfoButADictKeyIsNotSameFact_1(self):
        
        fact1 = TemplateFact("A", {"a":0, "b":1}, "MAIN")
        fact2 = TemplateFact("A", {"c":0, "b":2}, "MAIN")
        
        self.assertNotEqual(fact1, fact2)


    def test_TemplateFact_SameInfoButADictKeyIsNotSameFact_2(self):
        
        fact1 = TemplateFact("A", {"a":0, "b":1}, "MAIN")
        fact2 = TemplateFact("A", {"c":0, "b":1, "c": 2}, "MAIN")
        
        self.assertNotEqual(fact1, fact2)


    def test_TemplateFact_VectorAccessor(self):
        fact = TemplateFact("A", {"a":0, "b":1}, "MAIN")

        self.assertTrue(fact.values["a"] == fact["a"])
        self.assertTrue(fact.values["b"] == fact["b"])

    def test_TemplateFact_FactLenghtNotComputable(self):
        fact = TemplateFact("A", {"a":0, "b":1}, "MAIN")

        self.assertRaises(FactLengthNotComputableException, (lambda f:len(f)), fact)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()