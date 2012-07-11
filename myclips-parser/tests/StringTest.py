'''
Created on 11/lug/2012

@author: Francesco Capozzo
'''
import unittest
from Parser import StringParser
from myclips.parser.types import String

class StringTest(unittest.TestCase):


    def testObjectIsOneString(self):
        parser = StringParser()
        res = parser.parseString("""
        "ciao"
        """).asList()         
        
        self.assertIsInstance(res, list, "Il risultato non e' una lista")
        self.assertEqual(len(res), 1, "La lunghezza non e' 1")
        
    def testStringContentIsCoerent(self):
        parser = StringParser()
        res = parser.parseString("""
        "ciao"
        """).asList()   
        
        self.assertIsInstance(res[0], String, "Parsato non e' String")
        self.assertEqual(res[0].content, "ciao", "Il contenuto non e' coerente")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testObjectIsSymbol']
    unittest.main()