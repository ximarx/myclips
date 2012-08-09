'''
Created on 28/lug/2012

@author: Francesco Capozzo
'''
import unittest
from myclips.rete.tests.locations import VariableLocation, VariableReference
from MyClipsBaseTest import MyClipsBaseTest



class VariableReferenceTest(MyClipsBaseTest):


    def test_ComparisonEqual(self):
        
        varLoc = VariableLocation("bla", 0, "aSlot", True, 0)
        bindLoc = VariableLocation("bla", patternIndex=0, slotName="aSlot", fromBegin=True, beginIndex=0)
        
        ref1 = VariableReference(relPatternIndex=-2)
        ref2 = VariableReference(relPatternIndex=-2)
        varLoc.toVarReference(ref1)
        varLoc.toVarReference(ref2)
        ref1.reference = bindLoc
        ref2.reference = bindLoc
        
        self.assertEqual(ref1, ref2)
        
    def test_ComparisonNotEqual_RelPatternIndex(self):
        
        varLoc = VariableLocation("bla", 0, "aSlot", True, 0)
        bindLoc = VariableLocation("bla", patternIndex=0, slotName="aSlot", fromBegin=True, beginIndex=0)
        
        ref1 = VariableReference(relPatternIndex=-2)
        ref2 = VariableReference(relPatternIndex=0)
        varLoc.toVarReference(ref1)
        varLoc.toVarReference(ref2)
        ref1.reference = bindLoc
        ref2.reference = bindLoc
        
        self.assertNotEqual(ref1, ref2)
        

    def test_ComparisonNotEqual_Reference(self):
        
        varLoc = VariableLocation("bla", 0, "aSlot", True, 0)
        bindLoc1 = VariableLocation("bla", patternIndex=0, slotName="aSlot", fromBegin=True, beginIndex=0)
        bindLoc2 = VariableLocation("bla", patternIndex=0, slotName="aSlot", fromBegin=True, beginIndex=1)
        
        ref1 = VariableReference(relPatternIndex=-2)
        ref2 = VariableReference(relPatternIndex=0)
        varLoc.toVarReference(ref1)
        varLoc.toVarReference(ref2)
        ref1.reference = bindLoc1
        ref2.reference = bindLoc2
        
        self.assertNotEqual(ref1, ref2)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testComparisonEqual']
    unittest.main()