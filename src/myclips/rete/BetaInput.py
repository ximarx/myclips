'''
Created on 22/lug/2012

@author: Francesco Capozzo
'''

class BetaInput(object):
    '''
    An interface for nodes right-activable
    '''

    def leftActivation(self, token):
        raise NotImplementedError()
