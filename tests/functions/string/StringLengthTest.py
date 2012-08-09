'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
import unittest
from functions.BaseFunctionTest import BaseFunctionTest
import myclips.parser.Types as types
from myclips.functions.Function import InvalidArgTypeError
from myclips.functions.string.StringLength import StringLength


class StringIndexTest(BaseFunctionTest):

    def setUp(self):
        BaseFunctionTest.setUp(self)
        self._functionSetup(StringLength)


    def test_StringLength(self):
        
        self.assertTrue(self.forInput(types.String("12345678"))
                        .expect(types.Integer(8)))


    def test_ZeroLength(self):
        
        self.assertTrue(self.forInput(types.String(""))
                        .expect(types.Integer(0)))


    def test_ErrorOnInvalidInput(self):

        self.assertRaises(InvalidArgTypeError, 
                                self.theFunc.do, self.theEnv, types.Integer(2))
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()