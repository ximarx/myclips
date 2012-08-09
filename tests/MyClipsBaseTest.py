'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
import unittest
import myclips


class MyClipsBaseTest(unittest.TestCase):


    def __init__(self, methodName='runTest'):
        #myclips.logger.root.handlers[0].stream = sys.stdout
        unittest.TestCase.__init__(self, methodName=methodName)
        
    def setUp(self):
        unittest.TestCase.setUp(self)
        
    def _turnOnLogger(self):
        myclips.logger.disabled = False

    def _turnOffLogger(self):
        myclips.logger.disabled = True
        
