'''
Created on 03/feb/2013

@author: Ximarx
'''
from myclips.facts.Fact import Fact, FactInvalidSlotName,\
    FactLengthNotComputableException

class TemplateFact(Fact):
    '''
    classdocs
    '''


    def __init__(self, templateName, values=None , moduleName="MAIN"):
        
        self._values = values if isinstance(values, dict) else {}
        self._templateName = templateName 
        super(TemplateFact, self).__init__(moduleName)
        
        
    @property
    def templateName(self):
        '''
        Get the template name for this fact (if any)
        or None for Ordered-Fact
        '''
        return self._templateName
    
    @templateName.setter
    def templateName(self, value):
        '''
        Set a new template name for this fact
        @param value: a template name
        @type value: string
        '''
        self._templateName = value
        
    @property
    def values(self):
        '''
        Get all values of this fact.
        @rtype: dict
        '''
        return self._values        
        
        
    def slots(self):
        '''
        Get the list of fact's slots
        @rtype: list of string
        @return: the list of slots names for a template-fact
        '''
        return self._values.keys()
        
        
    def __getitem__(self, item):
        """
        Override the [] operator
        to allow values to be accessed
        through [slotname]
        """
        try:
            return self._values[item]
        except KeyError:
            raise FactInvalidSlotName(str(item))
        
    def __setitem__(self, item, value):
        '''
        Override [] = setter operator
        to forward definition to Fact.values container
        @param item: slot name or index
        @type item: string|index
        @param value: the value to set
        @type value: mixed
        '''
        self._values[item] = value
        
    def __delitem__(self, item):
        '''
        Override del operator to remove
        Fact.values items
        @param item: item to remove
        @type item: string
        '''
        del self._values[item]
        
    def __str__(self):
        '''
        Return a string serialization of the fact.
            (MODULE_NAME::TEMPLATE_NAME (SLOT1 VAL) (SLOT2 VAL))
        '''
        return "(%s::%s %s)"%(self._moduleName, self._templateName,
                              " ".join(["(%s %s)"%(str(s),str(v) if not isinstance(v, list)
                                                            else " ".join([str(x) for x in v]) ) for (s,v) in self._values.items()]))
    
    def __hash__(self):
        prefix = [self.moduleName, self.templateName]
        toHash = prefix + [(key, value) if not isinstance(value, list)
                            else (key, tuple(value))
                                for (key,value) in self._values.items()]
            
        return hash(tuple(toHash))
        
    def __eq__(self, other):
        if isinstance(self, TemplateFact) \
            and self.moduleName == other.moduleName \
            and self.templateName == other.templateName \
            and self.values == other.values:
            
            return True
        else:
            return False
        
    def __neq__(self, other):
        return not self.__eq__(other)
    
    def __len__(self):
        '''
        Raise Error: template fact has not length
        '''
        raise FactLengthNotComputableException
    

