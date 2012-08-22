'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
import unittest
from functions.BaseFunctionTest import BaseFunctionTest
import myclips.parser.Types as types
from myclips.Scope import Scope
from myclips.functions.Function import InvalidArgValueError
from unittest.case import skipIf
import myclips
from myclips.functions.command.Watch import Watch


class WatchTest(BaseFunctionTest):

    def setUp(self):
        BaseFunctionTest.setUp(self)
        self._functionSetup(Watch)


    def test_WatchAll(self):
        
        self.forInput(types.Symbol('all')).do()

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()