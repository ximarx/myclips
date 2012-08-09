'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
import unittest
from functions.BaseFunctionTest import BaseFunctionTest
import myclips.parser.Types as types
from myclips.functions.Function import InvalidArgTypeError
from myclips.functions.string.StringConcat import StringConcat
from myclips.rete.WME import WME
from myclips.Fact import Fact


class StringConcatTest(BaseFunctionTest):

    def setUp(self):
        BaseFunctionTest.setUp(self)
        self._functionSetup(StringConcat)


    def test_Concatenation(self):
        
        theWme = WME(1, Fact([]))
        
        self.assertTrue(self.forInput(types.Symbol("ciao"), types.String("mucca"), types.Integer(1), types.Float(1.5), theWme)
                        .expect(types.String("ciaomucca11.5"+str(theWme))))


    def test_ErrorOnInvalidInput(self):

        self.assertRaises(InvalidArgTypeError, 
                                self.theFunc.do, self.theEnv, [1,2,3])
        

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()