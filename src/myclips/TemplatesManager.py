'''
Created on 17/lug/2012

@author: Francesco Capozzo
'''
from myclips.Observable import Observable
from myclips.RestrictedManager import RestrictedManager, RestrictedDefinition


class TemplatesManager(RestrictedManager, Observable):
    '''
    Stores the list of allowed globals definitions for the scope
    '''
    instance = None
    EVENT_NEW_DEFINITION = "EVENT_TemplatesManager_NewDefinition"

    def __init__(self, scope):
        '''
        Constructor
        '''
        Observable.__init__(self, [
                TemplatesManager.EVENT_NEW_DEFINITION
            ])
        RestrictedManager.__init__(self, scope)
        
        
class TemplateDefinition(RestrictedDefinition):
    def __init__(self, moduleName, defName, linkedType, slots=None):
        RestrictedDefinition.__init__(self, moduleName, defName, "deftemplate", linkedType)
        self._slots = {} if slots is None else slots
        
    @property
    def slots(self):
        return self._slots
    
    def getSlot(self, slotName):
        return self._slots[slotName]
    
        
class SlotDefinition(object):
    TYPE_SINGLE = "single-slot"
    TYPE_MULTI = "multi-slot"
    
    def __init__(self, slotName, slotType, slotAttributes=None):
        self._slotName = slotName
        self._slotType = slotType
        self._slotAttributes = dict([(attribute.attributeType, attribute) for attribute 
                                        in (slotAttributes 
                                                if isinstance(slotAttributes, list) 
                                            else [])]) if not isinstance(slotAttributes, dict) else slotAttributes 
        
        
    def getSlotName(self):
        return self._slotName
    
    def getSlotType(self):
        return self._slotType
    
    def getSlotAttributes(self):
        return self._slotAttributes.values()
    
    def addSlotAttribute(self, attribute):
        self._slotAttributes[attribute.attributeType] = attribute
    
    def getSlotAttribute(self, attrName):
        return self._slotAttributes[attrName]
    
    def hasSlotAttribute(self, attrName):
        return self._slotAttributes.has_key(attrName)
    
    @staticmethod
    def fromParserSlotDefinition(psl):
        import myclips.parser.Types as types
        
        sType = SlotDefinition.TYPE_SINGLE
        if isinstance(psl, types.MultiSlotDefinition):
            sType = SlotDefinition.TYPE_MULTI

        # add Default = Nil for every slot
        # if a definition of default value is
        # available, it will overwrite this default            
        attrs = {
            Attribute_DefaultValue.attributeType : Attribute_DefaultValue(types.NullValue())
        }
        
        for sattr in psl.attributes:
            if isinstance(sattr, types.DefaultAttribute):
                attrs[Attribute_DefaultValue.attributeType] = Attribute_DefaultValue(sattr.defaultValue)
            elif isinstance(sattr, types.TypeAttribute):
                attrs[Attribute_TypeConstraint.attributeType] = Attribute_TypeConstraint(sattr.allowedTypes)
            # else unknown slot attribute type
            # (like carinality, range or allowed-constant that are unsupported)
            # so i just ignore it
        
        return SlotDefinition(psl.slotName, sType, attrs)

class Attribute(object):
    attributeType = ""
    pass

class Attribute_DefaultValue(Attribute):
    attributeType = "default"
    
    def __init__(self, defaultValue):
        self.defaultValue = defaultValue
        
    def getDefaultValue(self):
        return self.defaultValue

class Attribute_TypeConstraint(Attribute):
    attributeType = "type"
    
    def __init__(self, allowedTypes):
        '''
        @param allowedTypes: a tuple of valid class types
        '''
        self.allowedTypes = allowedTypes
        
    def getAllowedTypes(self):
        return self.allowedTypes
        
        