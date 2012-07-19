'''
Created on 19/lug/2012

@author: Francesco Capozzo
'''

class Observer(object):
    '''
    This class define an interface
    to allow an Observable object
    to notify an Observer object
    about an event
    '''
    def notify(self, eventName, *args, **kargs):
        pass

        