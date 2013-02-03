'''
Created on 03/feb/2013

@author: Ximarx
'''
from myclips.facts.Fact import Fact, FactInvalidIndex

class OrderedFact(Fact):
    '''
    Rappresents an fact in ordered representation. Fact's values
    are store as a list (array to be more precise) and can be accessed
    using vector-like methods (access by index)
    '''


    def __init__(self, values=None, moduleName="MAIN"):
        '''
        Constructor
        '''
        self._values = values if isinstance(values, list) else []
        super(OrderedFact, self).__init__(moduleName)
        
    @property
    def values(self):
        '''
        Get all values of this fact.
        @rtype: list
        '''
        return self._values        
        
    def __str__(self):
        '''
        Return a string serialization of the fact.
            MODULE_NAME::(VAL1 VAL2 VAL3)
        '''
        return "%s::(%s)"%(self._moduleName, " ".join([str(x) for x in self._values]))
    
    def __hash__(self):
        '''
        Give a static, numeric hash for this object using moduleName and values as seed
        '''
        return hash(tuple([self.moduleName] + self._values))
        
    def __eq__(self, other):
        '''
        Override equality operator:
            OrderedFact are equals if they have same moduleName
            and values
        '''
        if isinstance(other, OrderedFact) \
            and self.moduleName == other.moduleName \
            and self.values == other.values:
            return True;
        else:
            return False;
        
    def __neq__(self, other):
        return not self.__eq__(other)
    
    def __len__(self):
        '''
        Length of an ordered fact is equal to the length of its values vector
        '''
        return len(self.values)
    
    def __getitem__(self, item):
        """
        Override the [] operator
        to allow values to be accessed
        through [index]
        """
        try:
            return self._values[item]
        except KeyError:
            raise FactInvalidIndex(str(item))
            


