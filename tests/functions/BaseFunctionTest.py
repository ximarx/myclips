'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
import unittest
from myclips.functions import FunctionEnv
from myclips.rete.Network import Network
import myclips
from MyClipsBaseTest import MyClipsBaseTest

class ResultExpect(object):
    def __init__(self, theFunc, theEnv, theInputs):
        self.theInputs = theInputs
        self.theFunc = theFunc
        self.theEnv = theEnv
    
    def expect(self, theValue):
        return self.theFunc.do(self.theEnv, *self.theInputs) == theValue
    
    def expectType(self, theType):
        return isinstance(self.theFunc.do(self.theEnv, *self.theInputs), theType)
    
    def expectException(self, theException=None):
        try:
            self.theFunc.do(self.theEnv, *self.theInputs)
        except Exception, e:
            if theException is not None:
                return theException == e.__class__
            else:
                return e
            
    def do(self):
        return self.theFunc.do(self.theEnv, *self.theInputs)

class BaseFunctionTest(MyClipsBaseTest):

    def setUp(self):
        self.theEnv = None
        self.theFunc = None
        MyClipsBaseTest.setUp(self)
        
    def _turnOnLogger(self):
        myclips.logger.disabled = False

    def _turnOffLogger(self):
        myclips.logger.disabled = True
        
    def _functionSetup(self, theClass):
        network = Network()
        self.theEnv = FunctionEnv({}, network, network.modulesManager, network.resources)
        self.theFunc = theClass()
        return self.theFunc
    
    def forInput(self, *args):
        """
        @return: ResultExpect
        @rtype: ResultExpect
        """
        
        return ResultExpect(self.theFunc, self.theEnv, args)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()