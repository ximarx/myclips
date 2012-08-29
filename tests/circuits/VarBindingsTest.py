'''
Created on 29/ago/2012

@author: Ximarx
'''
import unittest
from circuits.BaseCircuitTest import BaseCircuitTest


class Test(BaseCircuitTest):


    def test_DummyJoinJoin(self):
        
        self.assertTrue(self.forCircuits(
            "(defrule R (A B ?c) (A ?c B) => (trigger-event test-succeeded ?c))",
            #"(draw-circuit R)",
            "(assert (A B C) (A C B))"
            ).success())
        

    def test_PatternIndexWithMultipleNot(self):
        
        self.assertTrue(self.forCircuits(
            """(defrule R
                    (phase match)
                    (rank ?P process-yes)
                    (technique aName ?P)
                    (possible ?V ?G ?ID)
                    (not (possible ~?V ?G ?ID))
                    (possible ?V ?G ?ID2&~?ID)
                    (not (impossible ?ID2 ?V ?P))
                => (trigger-event test-succeeded))""",
            "(draw-circuit R)",
            """(assert 
                    (phase match)
                    (rank P process-yes)
                    (technique aName P)
                    (possible V G ID)
                    (possible V G ID2))"""
            ).success())



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()