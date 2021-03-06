'''
Created on 09/ago/2012

@author: Francesco Capozzo
'''
import unittest
from myclips.functions import FunctionEnv
from myclips.rete.Network import Network
import myclips
from MyClipsBaseTest import MyClipsBaseTest
from myclips.listeners.EventsManagerListener import EventsManagerListener
from myclips.shell.Interpreter import Interpreter

class CircuitExpect(object):
    def __init__(self, aTrap):
        self.theTrap = aTrap
    
    def hasSuccess(self):
        return self.theTrap.isSucceeded > 0
    
    def hasFailure(self):
        return self.theTrap.isFailed > 0
    
    def succeeded(self):
        return self.theTrap.isSucceeded
    
    def failed(self):
        return self.theTrap.isFailed

    
    def both(self):
        return (self.theTrap.isSucceeded, self.theTrap.isFailed)
            

class EventTrap(EventsManagerListener):
    def __init__(self):
        self.isFailed = 0
        self.isSucceeded = 0
        EventsManagerListener.__init__(self, {'test-failed': self.failed, 'test-succeeded': self.succeeded})
        
    def failed(self, *args, **kargs):
        self.isFailed += 1
        
    def succeeded(self, *args, **kargs):
        self.isSucceeded += 1
    

class BaseCircuitTest(MyClipsBaseTest):

    def setUp(self):
        self.network = Network()
        self.interpreter = Interpreter(self.network, None)
        MyClipsBaseTest.setUp(self)
        
    def _turnOnLogger(self):
        myclips.logger.disabled = False

    def _turnOffLogger(self):
        myclips.logger.disabled = True

    def forCircuits(self, *circuits):
        
        for s in circuits:
            self.interpreter.evaluate(s)
        
        aTrap = EventTrap().install(self.network.eventsManager)
        cExpect = CircuitExpect(aTrap)
        
        self.network.run()
        
        return cExpect
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()