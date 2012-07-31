'''
Created on 17/lug/2012

@author: Francesco Capozzo
'''
from myclips.Observable import Observable
from myclips.RestrictedManager import RestrictedManager, RestrictedDefinition
from myclips.Fact import FactInvalidSlotName


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
        
    def addDefinition(self, definition):
        RestrictedManager.addDefinition(self, definition)
        
        # after i added the definition, i need to fire the event
        self.fire(self.__class__.EVENT_NEW_DEFINITION, definition)
        
        
class TemplateDefinition(RestrictedDefinition):
    def __init__(self, moduleName, defName, linkedType, slots=None):
        RestrictedDefinition.__init__(self, moduleName, defName, "deftemplate", linkedType)
        self._slots = {} if slots is None else slots
        
    @property
    def slots(self):
        return self._slots
    
    def getSlot(self, slotName):
        return self._slots[slotName]
    
    def isValidFact(self, fact):
        from myclips.Fact import Fact
        
        assert isinstance(fact, Fact)
        
        # fast check first
        if not fact.isTemplateFact() \
            or fact.templateName != self.name \
            or fact.moduleName != self.moduleName:
            
            return False
    
        # go deeper in slot configurations
        for slotName, slotDef in self.slots.items():
            
            try:
            
                # if slot is a single-field and value is a multi-field is an error for sure
                if slotDef.getSlotType() == SlotDefinition.TYPE_SINGLE \
                    and isinstance(fact[slotName], list):
                    
                    return "DefTemplate {0} slot definition {1} requires a single value. Multifield value found: {2}".format(self.name, 
                                                                                                                             slotName, 
                                                                                                                             fact[slotName])
                
                # if slot is a multi-field and value is single, i can cast it to a multi-field
                # to avoid errors
                elif slotDef.getSlotType() == SlotDefinition.TYPE_MULTI \
                    and not isinstance(fact[slotName], list):
                    
                    fact[slotName] = [fact[slotName]]
                    
                
                # now check slot attributes
                for sAttr in slotDef.getSlotAttributes():
            
                    if isinstance(sAttr, Attribute_TypeConstraint):
                        # check vs types
                        
                        valuesToCheck = []
                        if slotDef.getSlotType() == SlotDefinition.TYPE_SINGLE:
                            valuesToCheck.append(fact[slotName])
                        else:
                            valuesToCheck = fact[slotName]
                            
                        for singleValue in valuesToCheck:
                        
                            if not isinstance(singleValue, sAttr.getAllowedTypes()):
                                
                                return "A {2} value found doesn't match the allowed types {3} for slot {0} of template {4}::{1}".format(
                                            slotName,
                                            self.name,
                                            singleValue.__class__.__name__,
                                            tuple([t.__name__ for t in sAttr.getAllowedTypes()]),
                                            self.moduleName
                                        )
                                        
            except FactInvalidSlotName:
                # the slotName is not set in the fact
                # check if a default attr is available for the slot
                # if the default is ?NONE raise error (not nil value admitted)
                # else use the default value or None
                
                if slotDef.hasSlotAttribute(Attribute_DefaultValue.attributeType):
                    defValue = slotDef.getSlotAttribute(Attribute_DefaultValue.attributeType)
                    
                    if defValue is None:
                        return "Slot %s requires a value because of its (default ?NONE) attribute"%slotName
                    else:
                        fact[slotName] = defValue
 
                else:
                    import myclips.parser.Types as types
                    # is not default attribute is used, default ?DERIVE is default (and it means None)
                    fact[slotName] = types.SPECIAL_VALUES['?DERIVE']
            
        # check if some slot in the fact has no definition
        for slotInFact in fact.slots():
            if not self._slots.has_key(slotInFact):
                return "Invalid slot %s not defined in corresponding deftemplate %s"%(slotInFact, self.name)
            
        return True
        
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
        
        