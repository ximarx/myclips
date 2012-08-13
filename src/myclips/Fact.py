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
        Constructor
        '''
        self._templateName = templateName
        self._moduleName = moduleName
        # normalize values to [] (if ordered fact) or to {} (if template)
        values = values if values is not None else [] if templateName is None else {}
        self._values = values
        
    def __str__(self):
        if self._templateName is not None:
            return "(%s::%s %s)"%(self._moduleName, self._templateName, " ".join(["(%s %s)"%(str(s),str(v)) for (s,v) in self._values.items()]))
        else:
            return "%s::(%s)"%(self._moduleName, " ".join([str(x) for x in self._values]))
    
    def __hash__(self):
        try:
            prefix = [self.moduleName, self.templateName]
            if self.isTemplateFact():
                toHash = prefix + [(key, value) if not isinstance(value, list)
                                    else (key, tuple(value))
                                        for (key,value) in self._values.items()]
            else:
                toHash = prefix + self._values
                
            return hash(tuple(toHash))
        except Exception, e:
            print "WTFFFFFFFF: ", e
            raise
        
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
        return (self.templateName is not None)
    
    def slots(self):
        if self.isTemplateFact():
            return self._values.keys()
        else:
            raise FactSlotsNotComputableException()
        
    @property
    def templateName(self):
        return self._templateName
    
    @templateName.setter
    def templateName(self, value):
        self._templateName = value
        
    @property
    def moduleName(self):
        return self._moduleName
    
    @moduleName.setter
    def moduleName(self, value):
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
        if not self.isTemplateFact():
            raise FactSlotValueCannotBeSetException()
        
        self._values[item] = value
        
    def __delitem__(self, item):
        if not self.isTemplateFact():
            raise FactSlotValueCannotBeSetException()
        
        del self._values[item]
    
class FactLengthNotComputableException(MyClipsException):
    pass

class FactSlotValueCannotBeSetException(MyClipsException):
    pass

class FactSlotsNotComputableException(MyClipsException):
    pass

class FactInvalidIndex(MyClipsException):
    pass

class FactInvalidSlotName(MyClipsException):
    pass