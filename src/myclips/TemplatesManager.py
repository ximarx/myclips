'''
Created on 17/lug/2012

@author: Francesco Capozzo
'''
from myclips.Observable import Observable
from myclips.RestrictedManager import RestrictedManager, RestrictedDefinition
from myclips.Fact import FactInvalidSlotName


class TemplatesManager(RestrictedManager, Observable):
    '''
    Stores the list of allowed templates definitions for the scope
    '''
    instance = None
    EVENT_NEW_DEFINITION = "EVENT_TemplatesManager_NewDefinition"
    """Event sign used when new definition is added, observer will
    be notified with this sign!"""
    

    def __init__(self, scope):
        '''
        Create a new TemplatesManager for the scope

        @param scope: the scope owner of this manager
        @type scope: L{Scope}
        '''
        Observable.__init__(self, [
                TemplatesManager.EVENT_NEW_DEFINITION
            ])
        RestrictedManager.__init__(self, scope)
        
    def addDefinition(self, definition):
        '''
        Add a new definition and notify observers about this
        @param definition: a new function definition
        @type definition: L{TemplateDefinition}
        '''
        
        RestrictedManager.addDefinition(self, definition)
        
        # after i added the definition, i need to fire the event
        self.fire(self.__class__.EVENT_NEW_DEFINITION, definition)
        
        
class TemplateDefinition(RestrictedDefinition):
    '''
    Describes a template definition
    '''
    def __init__(self, moduleName, defName, linkedType, slots=None):
        '''
        Create a new definition from params
        @param moduleName: the owner module's name
        @type moduleName: string
        @param defName: the template name
        @type defName: string
        @param linkedType: the DefTemplateConstruct linked to this!
        @type linkedType: L{DefTemplateConstruct}
        @param slots: a list of slot definitions
        @type slots: list of L{SlotDefinition}
        '''
        RestrictedDefinition.__init__(self, moduleName, defName, "deftemplate", linkedType)
        self._slots = {} if slots is None else slots
        
    @property
    def slots(self):
        '''
        Get the list of slot definitions
        '''
        return self._slots
    
    def getSlot(self, slotName):
        '''
        Get a slot def by name
        @param slotName: the name of slot
        @type slotName: string
        '''
        return self._slots[slotName]
    
    def isValidFact(self, fact):
        '''
        Check if a Template-Fact is valid for this template,
        using templates definitions. Valid =
            - fact template name is the same for this def
            - fact has all slot values for required slots
            - fact has not slot not definited in this def
            - fact slots type is ok for this definition
            - values in fact slots are ok for this def
        @param fact: the fact to check
        @type fact: L{Fact}
        @rtype: boolean
        '''
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
                # if the default is ?NONE raise error (nil value is not admitted)
                # else use the default value or None
                
                if slotDef.hasSlotAttribute(Attribute_DefaultValue.attributeType):
                    defValue = slotDef.getSlotAttribute(Attribute_DefaultValue.attributeType).getDefaultValue()
                    #print defValue
                    
                    if defValue is None:
                        return "Slot %s requires a value because of its (default ?NONE) attribute"%slotName
                    else:
                        fact[slotName] = defValue
 
                else:
                    import myclips.parser.Types as types
                    # is not default attribute is used, default ?DERIVE is default (and it means nil for singleslot, [] for multislot)
                    if slotDef.getSlotType() == SlotDefinition.TYPE_MULTI:
                        fact[slotName] = []
                    else:
                        fact[slotName] = types.SPECIAL_VALUES['?DERIVE']
            
        # check if some slot in the fact has no definition
        for slotInFact in fact.slots():
            if not self._slots.has_key(slotInFact):
                return "Invalid slot %s not defined in corresponding deftemplate %s"%(slotInFact, self.name)
            
        return True
        
class SlotDefinition(object):
    '''
    Describes a slot definition
    '''
    TYPE_SINGLE = "single-slot"
    TYPE_MULTI = "multi-slot"
    
    def __init__(self, slotName, slotType, slotAttributes=None):
        '''
        Create the definition from params
        @param slotName: the slot key name
        @type slotName: string
        @param slotType: the slot type (single or multi?)
        @type slotType: "single-slot"|"multi-slot"
        @param slotAttributes: a list of attributes for the slots
        @type slotAttributes: list of L{Attribute}
        '''
        self._slotName = slotName
        '''store the name'''
        self._slotType = slotType
        '''store the type'''
        self._slotAttributes = dict([(attribute.attributeType, attribute) for attribute 
                                        in (slotAttributes 
                                                if isinstance(slotAttributes, list) 
                                            else [])]) if not isinstance(slotAttributes, dict) else slotAttributes
        '''store the attributes using a dict''' 
        
        
    def getSlotName(self):
        '''
        get the slot name
        '''
        return self._slotName
    
    def getSlotType(self):
        '''
        get the type
        '''
        return self._slotType
    
    def getSlotAttributes(self):
        '''
        Get all attributes
        '''
        return self._slotAttributes.values()
    
    def addSlotAttribute(self, attribute):
        '''
        Add a new attribute
        @param attribute: an attribute
        @type attribute: L{Attribute}
        '''
        self._slotAttributes[attribute.attributeType] = attribute
    
    def getSlotAttribute(self, attrName):
        '''
        Get an attribute by attribute type name
        @param attrName: the type
        @type attrName: string
        '''
        return self._slotAttributes[attrName]
    
    def hasSlotAttribute(self, attrName):
        '''
        Check if an attribute is already defined
        @param attrName: the name
        @type attrName: string
        '''
        return self._slotAttributes.has_key(attrName)
    
    @staticmethod
    def fromParserSlotDefinition(psl):
        '''
        Helper method: create a slot-definition
        from a parsed types.SlotDefinition, setting attributes
        and other magic things
        @param psl: a parsed types.SlotDefinition
        @type psl: L{myclips.parser.types.SlotDefinition}
        @rtype: L{SlotDefinition}
        '''
        import myclips.parser.Types as types
        
        sType = SlotDefinition.TYPE_SINGLE
        if isinstance(psl, types.MultiSlotDefinition):
            sType = SlotDefinition.TYPE_MULTI

        # add Default = Nil for every slot
        # if a definition of default value is
        # available, it will overwrite this default            
        attrs = {
            Attribute_DefaultValue.attributeType : Attribute_DefaultValue(types.SPECIAL_VALUES['?DERIVE'] if sType == SlotDefinition.TYPE_SINGLE else [])
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
    '''
    Base class for attributes
    '''
    attributeType = ""
    '''attribute type key'''
    pass

class Attribute_DefaultValue(Attribute):
    '''
    Descrive a default attribute for a slot
    '''
    attributeType = "default"
    
    def __init__(self, defaultValue):
        '''
        Setup the default type for a slot
        @param defaultValue: the default type
        @type defaultValue: L{BaseParsedType}
        '''
        self.defaultValue = defaultValue
        
    def getDefaultValue(self):
        '''
        Get the default type!
        '''
        return self.defaultValue

class Attribute_TypeConstraint(Attribute):
    '''
    Descrive a type attribute for a slot
    '''
    attributeType = "type"
    
    def __init__(self, allowedTypes):
        '''
        @param allowedTypes: a tuple of valid class types
        '''
        self.allowedTypes = allowedTypes
        
    def getAllowedTypes(self):
        '''
        Get valid types
        '''
        return self.allowedTypes
        
        