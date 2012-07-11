'''
Created on 11/lug/2012

@author: Francesco Capozzo
'''
import unittest
from Parser import SymbolParser
from myclips.parser.types import Symbol

class SymbolTest(unittest.TestCase):


    def testObjectIsOneSymbol(self):
        parser = SymbolParser()
        res = parser.parseString("""
        ciao
        """).asList()         
        
        self.assertIsInstance(res, list, "Il risultato non e' una lista")
        self.assertEqual(len(res), 1, "La lunghezza non e' 1")
        
    def testSymbolContentIsCoerent(self):
        parser = SymbolParser()
        res = parser.parseString("""
        ciao
        """).asList()   
        
        self.assertIsInstance(res[0], Symbol, "Parsato non e' Symbol")
        self.assertEqual(res[0].content, "ciao", "Il contenuto non e' coerente")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testObjectIsSymbol']
    unittest.main()