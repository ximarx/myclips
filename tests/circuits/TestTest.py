'''
Created on 29/ago/2012

@author: Ximarx
'''
import unittest
from circuits.BaseCircuitTest import BaseCircuitTest


class Test(BaseCircuitTest):


    def test_PatternIndexWithMultipleNot(self):
        
        self.assertEqual(self.forCircuits(
            """(defrule cautious
                    (R ?r1)
                    (R_ ?r3)
                    (C ?c1)
                    (C_ ?c3)
                    (G ?g1)
                    (G_ ?g3)
                    (test (or (= ?r1 ?r3) (= ?c1 ?c3) (= ?g1 ?g3)))
                => (trigger-event test-succeeded))""",
            """(assert 
                    (R 1) (R_ 1)
                    (C 2) (C_ 2)
                    (G 3) (G_ 3))"""
            ).succeeded(), 1)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()