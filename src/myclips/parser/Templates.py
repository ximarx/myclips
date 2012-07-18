'''
Created on 17/lug/2012

@author: Francesco Capozzo
'''

class TemplatesManager(object):
    '''
    Stores the list of allowed functions
    '''
    instance = None

    def __init__(self, templates = None):
        '''
        Constructor
        '''
        self._templates = templates if isinstance(templates, dict) else {}
        
    def registerTemplate(self, tmplDefinition):
        if not isinstance(tmplDefinition, TemplateDefinition):
            raise ValueError("TemplateDefinition required")
        self._templates[tmplDefinition.getTemplateName()] = tmplDefinition

    def getTemplatesNames(self):
        return self._templates.keys()
    
    def getTemplateDefinition(self, templateName):
        return self._templates[templateName]
    
    def getTemplates(self):
        '''TemplatesManager().getTemplates() -> list of registered templates (templateName, TemplateDefinition) pairs, as 2-tuples'''
        return self._templates.items()
    
    def reset(self):
        self._templates = {}
        
class TemplateDefinition(object):
    '''
    Collect definition information about a registered function
    '''
    def __init__(self, templateName, slotsDefinitions=None):
        self._templateName = templateName
        self._slots = (slotsDefinitions if isinstance(slotsDefinitions, dict) 
                        else {})
        
    def getTemplateName(self):
        return self._templateName
    
    def getSlotsDefinitions(self):
        return self._slots
    
    def getSlotDefinition(self, slotName):
        return self._slots[slotName]
        
    def newMock(self):
        return (True,None)
    
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
        import myclips.parser.types.Types as types
        
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

# Standard instance
TemplatesManager.instance = TemplatesManager()


def _SampleTemplatesInit():
    pass