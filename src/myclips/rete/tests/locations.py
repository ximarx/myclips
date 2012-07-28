'''
Created on 27/lug/2012

@author: Francesco Capozzo
'''


class AtomLocation(object):
    '''
    Describes a variable location inside a pattern
    '''

    def __init__(self,
                 patternIndex=None, slotName=None, fromBegin=None, 
                 beginIndex=None, fromEnd=None, endIndex=None, 
                 isMultiField=False, fullFact=None, fullSlot=None):

        self._patternIndex = patternIndex
        self._slotName = slotName
        self._fromBegin = fromBegin
        self._beginIndex = beginIndex
        self._fromEnd = fromEnd
        self._endIndex = endIndex
        self._isMultiField = isMultiField
        self._fullFact = fullFact
        self._fullSlot = fullSlot

    @property
    def patternIndex(self):
        return self._patternIndex
        
    @patternIndex.setter
    def patternIndex(self, value):
        self._patternIndex = value

    @property
    def slotName(self):
        return self._slotName
        
    @slotName.setter
    def slotName(self, value):
        self._slotName = value

    @property
    def fromBegin(self):
        return self._fromBegin
        
    @fromBegin.setter
    def fromBegin(self, value):
        self._fromBegin = value

    @property
    def beginIndex(self):
        return self._beginIndex
        
    @beginIndex.setter
    def beginIndex(self, value):
        self._beginIndex = value

    @property
    def fromEnd(self):
        return self._fromEnd
        
    @fromEnd.setter
    def fromEnd(self, value):
        self._fromEnd = value

    @property
    def endIndex(self):
        return self._endIndex
        
    @endIndex.setter
    def endIndex(self, value):
        self._endIndex = value

    @property
    def isMultiField(self):
        return self._isMultiField
        
    @isMultiField.setter
    def isMultiField(self, value):
        self._isMultiField = value

    @property
    def fullFact(self):
        return self._fullFact
        
    @fullFact.setter
    def fullFact(self, value):
        self._fullFact = value

    @property
    def fullSlot(self):
        return self._fullSlot
        
    @fullSlot.setter
    def fullSlot(self, value):
        self._fullSlot = value

        
    def __str__(self, *args, **kwargs):
        return ", ".join([x+"="+str(getattr(self, x)) for x in dir(self.__class__) if not callable(getattr(self, x))
                                                                                        and hasattr(self, "_"+x)
                                                                                        and getattr(self, x) is not None
                                                                                        ])


class VariableLocation(AtomLocation):
    
    def __init__(self, name, patternIndex=None, slotName=None, fromBegin=None, beginIndex=None, fromEnd=None, endIndex=None, isMultiField=False, fullFact=None, fullSlot=None):
        AtomLocation.__init__(self, patternIndex=patternIndex, slotName=slotName, 
                                    fromBegin=fromBegin, beginIndex=beginIndex, fromEnd=fromEnd, 
                                    endIndex=endIndex, isMultiField=isMultiField,
                                    fullFact=fullFact, fullSlot=fullSlot)
        self._name = name

    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, value):
        self._name = value

    def __str__(self, *args, **kwargs):
        return "<VariableLocation:{0},{1}>".format(
                self.name,
                super(VariableLocation, self).__str__()
            )
        
    def __repr__(self, *args, **kwargs):
        return self.__str__()
    
    def toVarReference(self, reference=None):
        reference = VariableReference() if reference is None else reference
        for key in [x for x in dir(self) if not callable(getattr(self, x)) and hasattr(self, "_"+x) and getattr(self, x) is not None]:
            setattr(reference, key, getattr(self, key))
        return reference
                
class VariableReference(AtomLocation):
    def __init__(self, name=None, reference=None, patternIndex=None,
                        slotName=None, fromBegin=None, beginIndex=None, 
                        fromEnd=None, endIndex=None, isMultiField=None, 
                        relPatternIndex=None, fullFact=None, fullSlot=None,
                        isNegative=False):

        AtomLocation.__init__(self, patternIndex, slotName, fromBegin, beginIndex, fromEnd, endIndex, isMultiField, fullFact, fullSlot)

        self._name = name
        self._reference = reference
        self._relPatternIndex = relPatternIndex
        self._isNegative = isNegative

    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def reference(self):
        return self._reference
        
    @reference.setter
    def reference(self, value):
        self._reference = value

    @property
    def relPatternIndex(self):
        return self._relPatternIndex
        
    @relPatternIndex.setter
    def relPatternIndex(self, value):
        self._relPatternIndex = value

    @property
    def isNegative(self):
        return self._isNegative
        
    @isNegative.setter
    def isNegative(self, value):
        self._isNegative = value

        
    def __str__(self, *args, **kwargs):
        return "<VariableReference:{0},{1}>".format(
                self.name,
                super(VariableReference, self).__str__()
            )        
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        toTestItems = ['__class__', 'relPatternIndex', 'isNegative', 'isMultiField',
                       'reference.slotName', 'reference.fromBegin', 'reference.fromEnd', 
                       'reference.beginIndex', 'reference.endIndex', 'reference.fullSlot',
                       'reference.fullFact', 'reference.isMultiField']
        try:
            for test in toTestItems:
                # try to split for the inner reference comparison
                splitted = test.split(".", 2)
                if len(splitted) == 2:
                    objRefThis = getattr(self, splitted[0])
                    objRefOther = getattr(other, splitted[0])
                    attribute = splitted[1]
                else:
                    objRefThis = self
                    objRefOther = other
                    attribute = splitted[0]
                    
                if getattr(objRefThis, attribute) != getattr(objRefOther, attribute):
                    return False
                
            # everything is the same
            return True
        except:
            # error? -> not equal
            return False
    
if __name__ == '__main__':
    
    props = ["fullFact", "fullSlot"]
    
    initHeader = """
    
    def __init__(self, {0}):
"""
    initPattern = "        self._{0} = {0}"
    propPattern = \
"""    @property
    def {0}(self):
        return self._{0}
        
    @{0}.setter
    def {0}(self, value):
        self._{0} = value
"""
    
    print initHeader.format(", ".join([x+"=None" for x in props]))
    for p in props:
        print initPattern.format(p)    

    print    
    for p in props:
        print propPattern.format(p)