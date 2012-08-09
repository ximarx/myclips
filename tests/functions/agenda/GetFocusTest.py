'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
import unittest
from functions.BaseFunctionTest import BaseFunctionTest
import myclips.parser.Types as types
from myclips.functions.Function import InvalidArgTypeError
from myclips.functions.agenda.GetFocus import GetFocus


class GetFocusTest(BaseFunctionTest):

    def setUp(self):
        BaseFunctionTest.setUp(self)
        self._functionSetup(GetFocus)


    def test_GetFocus(self):
        
        self.assertTrue(self.forInput()
                        .expect(types.Symbol("MAIN")))

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()