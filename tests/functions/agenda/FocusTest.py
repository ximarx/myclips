'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
import unittest
from functions.BaseFunctionTest import BaseFunctionTest
import myclips.parser.Types as types
from myclips.functions.agenda.Focus import Focus
from myclips.Scope import Scope
from myclips.functions.Function import InvalidArgValueError
from unittest.case import skipIf
import myclips


class FocusTest(BaseFunctionTest):

    def setUp(self):
        BaseFunctionTest.setUp(self)
        self._functionSetup(Focus)


    def test_PushOne(self):
        
        Scope("A", self.theEnv.modulesManager)
        self.theEnv.modulesManager.changeCurrentScope("MAIN")
        
        self.assertTrue(self.forInput(types.Symbol("A"))
                        .expect(types.Symbol("TRUE")))
        
        self.assertEqual(self.theEnv.network.agenda.focusStack[-1], "A")


    def test_PushMore(self):
        
        Scope("A", self.theEnv.modulesManager)
        Scope("B", self.theEnv.modulesManager)
        Scope("C", self.theEnv.modulesManager)
        self.theEnv.modulesManager.changeCurrentScope("MAIN")
        
        self.assertTrue(self.forInput(types.Symbol("A"), types.Symbol("B"), types.Symbol("C"))
                        .expect(types.Symbol("TRUE")))
        
        self.assertEqual(self.theEnv.network.agenda.focusStack, ["MAIN", "C", "B", "A"])

    @skipIf(myclips.STRICT_MODE, "In strict mode return FALSE on error")
    def test_ErrorOnPushInvalid(self):
        
        self.assertRaises(InvalidArgValueError, self.forInput(types.Symbol("A")).do)
        
    @skipIf(not myclips.STRICT_MODE, "In non-strict mode raise error")
    def test_ReturnFalseOnInvalid(self):

        self.assertTrue(self.forInput(types.Symbol("A"))
                        .expect(types.Symbol("FALSE")))
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()