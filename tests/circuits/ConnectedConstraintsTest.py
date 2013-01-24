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
                   (light ?color&yellow|blinking-yellow)
                => (trigger-event test-succeeded))""",
            """(assert 
                    (light yellow)
                    (light blinking-yellow))"""
            ).succeeded(), 2)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()