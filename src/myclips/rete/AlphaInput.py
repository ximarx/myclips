'''
Created on 22/lug/2012

@author: Francesco Capozzo
'''

class AlphaInput(object):
    '''
    An interface for nodes right-activable
    '''

    def rightActivation(self, wme):
        raise NotImplementedError()
