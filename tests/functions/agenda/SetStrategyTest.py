'''
Created on 10/ago/2012

@author: Francesco Capozzo
'''
import unittest
from functions.BaseFunctionTest import BaseFunctionTest
import myclips.parser.Types as types
from myclips.Scope import Scope
from myclips.functions.Function import InvalidArgValueError
from myclips.functions.agenda.SetStrategy import SetStrategy


class SetStrategyTest(BaseFunctionTest):

    def setUp(self):
        BaseFunctionTest.setUp(self)
        self._functionSetup(SetStrategy)


    def test_DefaultStrategyIsDepth(self):
        
        self.assertTrue(self.forInput(types.Symbol("breadth"))
                        .expect(types.Symbol("depth")))
        
        #self.assertEqual(self.theEnv.network.agenda.strategy, "breadth")

    def test_StrategyChanged(self):
        
        self.forInput(types.Symbol("breadth")).do()
        
        self.assertEqual(self.theEnv.network.agenda.strategy, "breadth")


    def test_ErrorOnInvalidStrategy(self):
        
        self.assertRaises(InvalidArgValueError, self.forInput(types.Symbol("invalid-strategy")).do)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()