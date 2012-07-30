'''
Created on 30/lug/2012

@author: Francesco Capozzo
'''
import unittest
import myclips.parser.Types as types
import myclips.rete.analysis as analysis

class Test(unittest.TestCase):


    def test_SimpleAndOrReversion(self):
        
        lhs = [types.AndPatternCE([
                    types.OrPatternCE(["A", "B"]),
                    "C"
            ])]
        
        lhs = analysis.normalizeLHS(lhs)
        
        self.assertIsInstance(lhs, types.OrPatternCE)
        self.assertIsInstance(lhs.patterns[0], types.AndPatternCE)
        self.assertIsInstance(lhs.patterns[1], types.AndPatternCE)
        self.assertEqual(lhs.patterns[0].patterns, ["A", "C"])
        self.assertEqual(lhs.patterns[1].patterns, ["B", "C"])
        

    def test_NestedAndOrReversion(self):
        
        lhs = [types.AndPatternCE([
                    types.OrPatternCE(["A", "B"]),
                    types.OrPatternCE(["C", "D",
                        types.AndPatternCE(["Z",
                                types.OrPatternCE(["W", "X"]) 
                            ])
                        ])
            ])]

        lhs = analysis.normalizeLHS(lhs)
        
        self.assertIsInstance(lhs, types.OrPatternCE)
        permutations = []
        for i in range(0,8):
            self.assertIsInstance(lhs.patterns[i], types.AndPatternCE)
            permutations.append(lhs.patterns[i].patterns)
            
        permutationExpected = [["A", "C"], ["B", "C"], ["A", "D"], ["B", "D"],  
                               ["A", "Z", "W"], ["A", "Z", "X"], ["B", "Z", "W"], ["B", "Z", "X"]]
        
        self.assertEqual(permutations, permutationExpected)
        
    def test_SimpleNotOrReversion(self):


        lhs = [types.NotPatternCE(
                    types.OrPatternCE(["C", "D"])
            )]

        lhs = analysis.normalizeLHS(lhs)

        self.assertIsInstance(lhs, types.OrPatternCE)
        
        permutations = []
        for i in range(0,2):
            self.assertIsInstance(lhs.patterns[i], types.AndPatternCE)
            self.assertIsInstance(lhs.patterns[i].patterns[0], types.NotPatternCE)
            permutations.append(lhs.patterns[i].patterns[0].pattern)
            
        permutationExpected = ["C", "D"]
        
        self.assertEqual(permutations, permutationExpected)


    def test_NestedNotOrReversion(self):


        lhs = [types.NotPatternCE(
                    types.OrPatternCE(["C", "D",
                        types.AndPatternCE(["Z",
                                types.NotPatternCE(
                                    types.OrPatternCE(["W", "X"])
                                ) 
                            ])
                        ])
            )]

        lhs = analysis.normalizeLHS(lhs)

        self.assertIsInstance(lhs, types.OrPatternCE)
        
        permutations = []
        for i in range(0,4):
            self.assertIsInstance(lhs.patterns[i], types.AndPatternCE)
            self.assertIsInstance(lhs.patterns[i].patterns[0], types.NotPatternCE)
            if isinstance(lhs.patterns[i].patterns[0].pattern, types.AndPatternCE):
                permutations.append("~({0})".format(" ".join([t if not isinstance(t, types.NotPatternCE) else "~"+t.pattern 
                                     for t in lhs.patterns[i].patterns[0].pattern.patterns])))
            else:
                permutations.append("~"+lhs.patterns[i].patterns[0].pattern)
            
        permutationExpected = ["~C", "~D", "~(Z ~W)", "~(Z ~X)"]
        
        self.assertEqual(permutations, permutationExpected)
        
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_SimpleAndOrReversion']
    unittest.main()