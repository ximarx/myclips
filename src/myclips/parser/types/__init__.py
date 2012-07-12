

class ParsedType(object):
    '''
    Base class for all parsed types
    Conversion to native type is delegated
    to evaluate() call
    '''
    def __init__(self, content):
        self.content = content

    def evaluate(self):
        if hasattr(self, 'converter'):
            return self.converter(self.content)
        else:
            return self.content
        
    def __repr__(self, *args, **kwargs):
        evaluated = self.evaluate()
        return "<{0}:{1}, {2}:{3}>".format(self.__class__.__name__, self.content, evaluated.__class__.__name__, evaluated )

class BaseParsedType(ParsedType):
    '''
    Base class for all 1:1 native mappable types
    Conversion to native type is done as soon as possible
    and never done again
    '''
    def __init__(self, content):
        ParsedType.__init__(self, content)
        if hasattr(self, 'converter'):
            self.content = self.converter(self.content)
        
    def evaluate(self):
        return self.content

    def __repr__(self, *args, **kwargs):
        return "<{0}, {1}:{2}>".format(self.__class__.__name__, self.content.__class__.__name__, self.content )
    

class Integer(BaseParsedType):
    converter = lambda self, t: int(t)
    pass

class Symbol(BaseParsedType):
    pass

class String(BaseParsedType):
    converter = lambda self, t: '"'+str(t)+'"'
    pass

class Float(BaseParsedType):
    converter = float
    pass

class InstanceName(BaseParsedType):
    pass

class Variable(ParsedType):
    pass

class SingleFieldVariable(Variable):
    converter = lambda self, t: "?"+self.content.evaluate()
    pass

class MultiFieldVariable(Variable):
    converter = lambda self, t: "?$"+self.content.evaluate()
    pass

class GlobalVariable(Variable):
    converter = lambda self, t: "?*"+self.content.evaluate()
    pass

class FunctionCall(ParsedType):
    def __init__(self, funcName, funcArgs=None):
        ParsedType.__init__(self, funcName)
        self.funcName = funcName.evaluate()
        self.funcArgs = funcArgs if funcArgs != None else []
        
    def __repr__(self, *args, **kwargs):
        return "<{0}, {1}, {2}>".format(self.__class__.__name__,
                                        self.funcName,
                                        self.funcArgs )

class DefFactsConstruct(ParsedType):
    def __init__(self, deffactsName, deffactsComment=None, rhs=None):
        ParsedType.__init__(self, deffactsName)
        self.deffactsName = deffactsName.evaluate()
        self.deffactsComment = deffactsComment.evaluate().strip('"') if deffactsComment != None else None
        self.rhs = rhs if rhs != None else []
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}, {2}, {3}>".format(self.__class__.__name__,
                                        self.deffactsName,
                                        self.deffactsComment,
                                        self.rhs )

class OrderedRhsPattern(ParsedType):
    converter = lambda self, t: [x.evaluate() if isinstance(x, ParsedType) else x for x in t]
    pass

class TemplateRhsPattern(ParsedType):
    def __init__(self, templateName, templateSlots=None):
        ParsedType.__init__(self, templateName)
        self.templateName = templateName.evaluate() if isinstance(templateName, ParsedType) else templateName
        self.templateSlots =  templateSlots if templateName != None else []
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}, {2}>".format(self.__class__.__name__,
                                        self.templateName,
                                        self.templateSlots)
    
class FieldRhsSlot(ParsedType):
    pass

class MultiFieldRhsSlot(FieldRhsSlot):
    def __init__(self, slotName, slotValue=None):
        ParsedType.__init__(self, slotName)
        self.slotName = slotName.evaluate() if isinstance(slotName, ParsedType) else slotName 
        self.slotValue = slotValue if slotValue != None else []

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}, {2}>".format(self.__class__.__name__,
                                        self.slotName,
                                        self.slotValue)

class SingleFieldRhsSlot(FieldRhsSlot):
    def __init__(self, slotName, slotValue):
        ParsedType.__init__(self, slotName)
        self.slotName = slotName.evaluate() if isinstance(slotName, ParsedType) else slotName 
        self.slotValue = slotValue

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}, {2}>".format(self.__class__.__name__,
                                        self.slotName,
                                        self.slotValue)


class DefRuleConstruct(ParsedType):
    def __init__(self, defruleName, defruleComment=None, defruleDeclaration=None, lhs=None, rhs=None):
        ParsedType.__init__(self, defruleName)
        self.defruleName = defruleName.evaluate() if isinstance(defruleName, ParsedType) else defruleName
        self.defruleComment = defruleComment.evaluate().strip('"') if isinstance(defruleComment, ParsedType) else None
        self.defruleDeclaration = defruleDeclaration if defruleDeclaration != None else []
        self.lhs = lhs if lhs != None else [] 
        self.rhs = rhs if rhs != None else []
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}, {2}, {3}, {4} => {5}>".format(self.__class__.__name__,
                                        self.defruleName,
                                        self.defruleComment,
                                        self.defruleDeclaration,
                                        self.lhs,
                                        self.rhs )
        
class RuleProperty(ParsedType):
    def __init__(self, propertyName, propertyValue):
        ParsedType.__init__(self, propertyName)
        self.propertyName = propertyName.evaluate() if isinstance(propertyName, ParsedType) else propertyName
        self.propertyValue = propertyValue.evaluate() if isinstance(propertyValue, ParsedType) else propertyValue
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1} = {2}>".format(self.__class__.__name__,
                                        self.propertyName,
                                        self.propertyValue )

def makeInstance(cls, position=0):
    def makeAction(s,l,t):
        if position != None:
            try:
                return cls(t[position].asList())
            except:
                return cls(t[position])
        else:
            try:
                return cls(t.asList())
            except:
                return cls(t)
            
    return makeAction

def makeInstanceDict(cls, args):
    def makeDictAction(s,l,t):
        targs = {}
        for (k,v) in args.items():
            if isinstance(v, tuple) and len(v) == 2:
                try:
                    targs[k] = t.asList()[v[0]:v[1]]
                except:
                    targs[k] = t[v[0]:v[1]]
            else: 
                try:
                    targs[k] = t[v].asList()
                except:
                    try:
                        targs[k] = t[v]
                    except:
                        if isinstance(k, int):
                            raise
        return cls(**targs)
        
    return makeDictAction

def tryInstance(cls1, cls2, position=0):
    def tryMakeAction(s,l,t):
        try:
            return makeInstance(cls1, position)(s,l,t)
        except:
            return makeInstance(cls2, position)(s,l,t)
            
    return tryMakeAction
    
