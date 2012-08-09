'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
import unittest
from functions.BaseFunctionTest import BaseFunctionTest
from myclips.functions.agenda.Halt import Halt
from myclips.functions.Function import HaltException


class HaltTest(BaseFunctionTest):

    def setUp(self):
        BaseFunctionTest.setUp(self)
        self._functionSetup(Halt)


    def test_ErrorOnPushInvalid(self):
        
        self.assertRaises(HaltException, self.forInput().do)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()