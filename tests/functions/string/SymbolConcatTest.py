'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
import unittest
from functions.BaseFunctionTest import BaseFunctionTest
import myclips.parser.Types as types
from myclips.functions.Function import InvalidArgTypeError
from myclips.rete.WME import WME
from myclips.functions.string.SymbolConcat import SymbolConcat
from myclips.facts.OrderedFact import OrderedFact


class SymbolConcatTest(BaseFunctionTest):

    def setUp(self):
        BaseFunctionTest.setUp(self)
        self._functionSetup(SymbolConcat)


    def test_Concatenation(self):
        
        theWme = WME(1, OrderedFact([]))
        
        self.assertTrue(self.forInput(types.Symbol("ciao"), types.String("mucca albero"), types.Integer(1), types.Float(1.5), theWme)
                        .expect(types.Symbol("ciaomucca albero11.5"+str(theWme))))


    def test_ErrorOnInvalidInput(self):

        self.assertRaises(InvalidArgTypeError, 
                                self.theFunc.do, self.theEnv, [1,2,3])
        

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()