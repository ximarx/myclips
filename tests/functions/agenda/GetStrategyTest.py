'''
Created on 10/ago/2012

@author: Francesco Capozzo
'''
import unittest
from functions.BaseFunctionTest import BaseFunctionTest
import myclips.parser.Types as types
from myclips.functions.agenda.GetStrategy import GetStrategy
from myclips import strategies


class GetStrategyTest(BaseFunctionTest):

    def setUp(self):
        BaseFunctionTest.setUp(self)
        self._functionSetup(GetStrategy)


    def test_DefaultStrategyIsDepth(self):
        
        self.assertTrue(self.forInput()
                        .expect(types.Symbol("depth")))

    def test_StrategyChanged(self):
        
        self.theEnv.network.agenda.changeStrategy(strategies.factory.newInstance("breadth"))

        self.assertTrue(self.forInput()
                        .expect(types.Symbol("breadth")))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()