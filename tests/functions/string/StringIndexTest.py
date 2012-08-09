'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
import unittest
from functions.BaseFunctionTest import BaseFunctionTest
import myclips.parser.Types as types
from myclips.functions.Function import InvalidArgTypeError
from myclips.functions.string.StringIndex import StringIndex


class StringIndexTest(BaseFunctionTest):

    def setUp(self):
        BaseFunctionTest.setUp(self)
        self._functionSetup(StringIndex)


    def test_StringIndexFound(self):
        
        self.assertTrue(self.forInput(types.String("camm"), types.String("Nel mezzo del cammin di nostra vita"))
                        .expect(types.Integer(15)))


    def test_StringIndexFoundAlwaysTheFirstOne(self):
        
        self.assertTrue(self.forInput(types.String("e"), types.String("Nel mezzo del cammin di nostra vita"))
                        .expect(types.Integer(2)))

    def test_ReturnFalseIfNotFound(self):
        
        self.assertTrue(self.forInput(types.String("w"), types.String("Nel mezzo del cammin di nostra vita"))
                        .expect(types.Symbol("FALSE")))


    def test_ErrorOnInvalidInput(self):

        self.assertRaises(InvalidArgTypeError, 
                                self.theFunc.do, self.theEnv, types.Integer(2), types.String("blabla"))
        
        self.assertRaises(InvalidArgTypeError, 
                                self.theFunc.do, self.theEnv, types.String("blabla"), types.Float(2))

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()