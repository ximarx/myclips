'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.MyClipsException import MyClipsException

class Fact(object):
    '''
    A Fact: regroup a sequence of myclips's base types
    or a dict of key-value couple of myclips's base types
    to rappresent a fact in a wme of the working memory  
    '''


    def __init__(self, values=None, templateName=None, moduleName="MAIN"):
        '''
        Create a new fact, wit scope moduleName using values
        
        @param values: a list or a dict of values
        @type values: list|dict
        @param templateName: a template name for template-facts
        @type templateName: string
        @param moduleName: name of the module owning this fact
        @type moduleName: string
        '''
        
        self._templateName = templateName
        self._moduleName = moduleName
        # normalize values to [] (if ordered fact) or to {} (if template)
        values = values if values is not None else [] if templateName is None else {}
        self._values = values
        
    def __str__(self):
        '''
        Return a string serialization of the fact.
        For ordered-fact:
            MODULE_NAME::(VAL1 VAL2 VAL3)
        for template-fact:
            (MODULE_NAME::TEMPLATE_NAME (SLOT1 VAL) (SLOT2 VAL))
        '''
        if self._templateName is not None:
            return "(%s::%s %s)"%(self._moduleName, self._templateName,
                                  " ".join(["(%s %s)"%(str(s),str(v) if not isinstance(v, list)
                                                                else " ".join([str(x) for x in v]) ) for (s,v) in self._values.items()]))
        else:
            return "%s::(%s)"%(self._moduleName, " ".join([str(x) for x in self._values]))
    
    def __hash__(self):
        prefix = [self.moduleName, self.templateName]
        if self.isTemplateFact():
            toHash = prefix + [(key, value) if not isinstance(value, list)
                                else (key, tuple(value))
                                    for (key,value) in self._values.items()]
        else:
            toHash = prefix + self._values
            
        return hash(tuple(toHash))
        
    def __eq__(self, other):
        try:
            return self.__class__ == other.__class__ \
                    and self.moduleName == other.moduleName \
                    and self.templateName == other.templateName \
                    and self._values == other._values
        except:
            # any error? return false
            return False
        
    def __neq__(self, other):
        return not self.__eq__(other)
    
    def __len__(self):
        if not self.isTemplateFact():
            return len(self._values)
        else:
            raise FactLengthNotComputableException()
        
    def isTemplateFact(self):
        '''
        Check if fact is a Template-Fact one
        @rtype: boolean 
        '''
        return (self.templateName is not None)
    
    def slots(self):
        '''
        Get the list of fact's slots
        @rtype: list of string
        @return: the list of slots names for a template-fact
        @raise FactSlotsNotComputableException: if fact isn't a template-fact 
        '''
        if self.isTemplateFact():
            return self._values.keys()
        else:
            raise FactSlotsNotComputableException()
        
    @property
    def values(self):
        '''
        Get all values of this fact.
        Use Fact.isTemplateFact to know
        if is list or dict :)
        @rtype: list|dict
        '''
        return self._values
        
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
    def moduleName(self):
        '''
        Get the module name for the owner of this fact
        @rtype: string
        '''
        return self._moduleName
    
    @moduleName.setter
    def moduleName(self, value):
        '''
        Set a module name as owner of this fact
        @param value: the module name
        @type value: string
        '''
        self._moduleName = value
    
    def __getitem__(self, item):
        """
        Override the [] operator
        to allow values to be accessed
        through [index] or [slotname]
        """
        try:
            return self._values[item]
        except KeyError:
            if self.isTemplateFact():
                raise FactInvalidSlotName(str(item))
            else:
                raise FactInvalidIndex(str(item))
            
    
    def __setitem__(self, item, value):
        '''
        Override [] = setter operator
        to forward definition to Fact.values container
        @param item: slot name or index
        @type item: string|index
        @param value: the value to set
        @type value: mixed
        @raise FactSlotValueCannotBeSetException: if fact is not Template-Fact
        '''
        if not self.isTemplateFact():
            raise FactSlotValueCannotBeSetException()
        
        self._values[item] = value
        
    def __delitem__(self, item):
        '''
        Override del operator to remove
        Fact.values items
        @param item: item to remove
        @type item: string
        @raise FactSlotValueCannotBeSetException: if fact is not Template-Fact
        '''
        if not self.isTemplateFact():
            raise FactSlotValueCannotBeSetException()
        
        del self._values[item]
    
class FactLengthNotComputableException(MyClipsException):
    '''
    Trying to compute len of a Template-Fact? You'll get this!
    '''

class FactSlotValueCannotBeSetException(MyClipsException):
    '''
    Trying to set a slot for an Ordered-Fact? You'll get this!
    '''
    

class FactSlotsNotComputableException(MyClipsException):
    '''
    Trying to get slots list for an Ordered-Fact? You'll get this!
    '''

class FactInvalidIndex(MyClipsException):
    '''
    Trying to get an invalid index for a Ordered-Fact? You'll get this!
    '''

class FactInvalidSlotName(MyClipsException):
    '''
    Trying to get an invalid slot for a Template-Fact? You'll get this!
    '''
