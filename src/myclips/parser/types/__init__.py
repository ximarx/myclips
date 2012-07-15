

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
    
class Number(BaseParsedType):
    pass

class Lexeme(BaseParsedType):
    pass

class Integer(Number):
    converter = lambda self, t: int(t)
    pass

class Symbol(Lexeme):
    pass

class String(Lexeme):
    converter = lambda self, t: '"'+str(t)+'"'
    pass

class Float(Number):
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

class UnnamedSingleFieldVariable(Variable):
    converter = lambda self, t: "?"
    pass

class UnnamedMultiFieldVariable(Variable):
    converter = lambda self, t: "?$"
    pass

class GlobalVariable(Variable):
    converter = lambda self, t: "?*"+self.content.evaluate()+"*"
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
    #converter = lambda self, t: [x.evaluate() if isinstance(x, ParsedType) else x for x in t]
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
        FieldRhsSlot.__init__(self, slotName)
        self.slotName = slotName.evaluate() if isinstance(slotName, ParsedType) else slotName 
        self.slotValue = slotValue if slotValue != None else []

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}, {2}>".format(self.__class__.__name__,
                                        self.slotName,
                                        self.slotValue)

class SingleFieldRhsSlot(FieldRhsSlot):
    def __init__(self, slotName, slotValue):
        FieldRhsSlot.__init__(self, slotName)
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

class PatternCE(ParsedType):
    pass

class OrderedPatternCE(PatternCE):
    def __init__(self, content):
        PatternCE.__init__(self, content)
        self.constraints = content
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                    self.constraints
                                    )

class TemplatePatternCE(PatternCE):
    def __init__(self, templateName, templateSlots=None):
        PatternCE.__init__(self, templateName)
        self.templateName = templateName.evaluate() if isinstance(templateName, ParsedType) else templateName
        self.templateSlots = templateSlots if templateSlots != None else []
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}, {2}>".format(self.__class__.__name__,
                                    self.templateName,
                                    self.templateSlots
                                    )
        
class AssignedPatternCE(PatternCE):
    def __init__(self, variable, pattern):
        PatternCE.__init__(self, variable)
        self.variable = variable
        self.pattern = pattern
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1} <- {2}>".format(self.__class__.__name__,
                                    self.variable,
                                    self.pattern
                                    )
    

class NotPatternCE(PatternCE):
    def __init__(self, pattern):
        if isinstance(pattern, AssignedPatternCE):
            import pyparsing
            raise pyparsing.ParseFatalException("A pattern CE cannot be bound to a pattern-address within a not CE")
        PatternCE.__init__(self, pattern)
        self.pattern = pattern
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                    self.pattern
                                    )

class AndPatternCE(PatternCE):
    def __init__(self, patterns):
        if len(patterns) > 0 and isinstance(patterns[0], AssignedPatternCE):
            import pyparsing
            raise pyparsing.ParseFatalException("Syntax Error:  Check appropriate syntax for the first field of a pattern.")
        PatternCE.__init__(self, patterns)
        self.patterns = patterns
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                    self.patterns
                                    )

class TestPatternCE(PatternCE):
    def __init__(self, function):
        PatternCE.__init__(self, function)
        self.function = function
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                    self.function,
                                    )

 
class Constraint(ParsedType):
    def __init__(self, constraint, connectedConstraints=None):
        ParsedType.__init__(self, constraint)
        self.constraint = constraint
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                    self.constraint
                                    )

class ConnectedConstraint(ParsedType):
    def __init__(self, constraint, connectedConstraints=None):
        if connectedConstraints is None:
            raise ValueError()
        ParsedType.__init__(self, constraint)
        # constraint is Constraint for sure
        self.constraint = constraint
        self.connectedConstraints = [] # define it here first
        # connectedConstraint is [#CONNECTIVE, Constraint]
        #     OR
        # connectedConstraint is [#CONNECTIVE, ConnectedConstraint]
        # i need to linearize all ConnectedConstraint as a single ConnectedConstraint
        # with self.constraints = [#CONNECTIVE, Constraint]
        connective, subconstraints = connectedConstraints
        if isinstance(subconstraints, ConnectedConstraint):
            # need to linearize it
            self.connectedConstraints = [[connective, subconstraints.constraint]] + subconstraints.connectedConstraints
            # now i need to sort it!
            # priority: ~,&,|
            #TODO sort function / nested connnected handling 
        else:
            self.connectedConstraints = [connectedConstraints]
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},{2}>".format(self.__class__.__name__,
                                    self.constraint,
                                    self.connectedConstraints
                                    )
    
class Term(ParsedType):
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                    self.term,
                                    )

class PositiveTerm(Term):
    def __init__(self, term, isNot=None):
        if isNot is not None:
            raise ValueError()
        Term.__init__(self, term)
        self.term = term

        
class NegativeTerm(Term):
    def __init__(self, term, isNot=None):
        if isNot is None:
            raise ValueError()
        Term.__init__(self, term)
        self.term = term
    
    
class FieldLhsSlot(ParsedType):
    pass

class MultiFieldLhsSlot(FieldLhsSlot):
    def __init__(self, slotName, slotValue=None):
        FieldLhsSlot.__init__(self, slotName)
        self.slotName = slotName.evaluate() if isinstance(slotName, ParsedType) else slotName 
        self.slotValue = slotValue if slotValue != None else []

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}, {2}>".format(self.__class__.__name__,
                                        self.slotName,
                                        self.slotValue)

class SingleFieldLhsSlot(FieldLhsSlot):
    def __init__(self, slotName, slotValue):
        FieldLhsSlot.__init__(self, slotName)
        self.slotName = slotName.evaluate() if isinstance(slotName, ParsedType) else slotName 
        self.slotValue = slotValue

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}, {2}>".format(self.__class__.__name__,
                                        self.slotName,
                                        self.slotValue)    

class SlotDefinition(ParsedType):
    def __init__(self, content, attributes):
        ParsedType.__init__(self, content)
        self.attributes = attributes if attributes != None else []
        if len(self.attributes) != len(set([x.__class__ for x in self.attributes])):
            import pyparsing
            raise pyparsing.ParseFatalException("Multiple definition for same type of attribute")
    pass

class SingleSlotDefinition(SlotDefinition):
    def __init__(self, slotName, attributes=None):
        SlotDefinition.__init__(self, slotName, attributes)
        self.slotName = slotName.evaluate() if isinstance(slotName, ParsedType) else slotName 
        #self.attributes = attributes if attributes != None else []

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}, {2}>".format(self.__class__.__name__,
                                        self.slotName,
                                        self.attributes)    

class MultiSlotDefinition(SlotDefinition):
    def __init__(self, slotName, attributes=None):
        SlotDefinition.__init__(self, slotName, attributes)
        self.slotName = slotName.evaluate() if isinstance(slotName, ParsedType) else slotName 
        #self.attributes = attributes if attributes != None else []

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}, {2}>".format(self.__class__.__name__,
                                        self.slotName,
                                        self.attributes)    

class Attribute(ParsedType):
    pass

class DefaultAttribute(Attribute):
    def __init__(self, defaultValue):
        Attribute.__init__(self, defaultValue)
        self.defaultValue = defaultValue if isinstance(defaultValue, ParsedType) else SPECIAL_VALUES[defaultValue]
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                        self.defaultValue)    

class TypeAttribute(Attribute):
    def __init__(self, allowedTypes=None):
        Attribute.__init__(self, allowedTypes)
        self.allowedTypes = [TYPES[x] for x in allowedTypes] if isinstance(allowedTypes, list) else [TYPES["?VARIABLE"]]
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                        self.allowedTypes)    

class DefTemplateConstruct(ParsedType):
    def __init__(self, templateName, templateComment=None, slots=None):
        ParsedType.__init__(self, templateName)
        self.templateName = templateName.evaluate() if isinstance(templateName, BaseParsedType) else templateName
        self.templateComment = templateComment.evaluate().strip('"') if isinstance(templateComment, BaseParsedType) else None
        self.slots = slots if slots != None else []
        if len(self.slots) != len(set([x.slotName for x in self.slots])):
            import pyparsing
            raise pyparsing.ParseFatalException("Multiple definition for same slot name")
        
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}, {2}, {3}>".format(self.__class__.__name__,
                                        self.templateName,
                                        self.templateComment,
                                        self.slots)
        
class DefGlobalConstruct(ParsedType):
    def __init__(self, assignments=None, moduleName=None):
        ParsedType.__init__(self, assignments)
        self.moduleName = moduleName.evaluate() if isinstance(moduleName, BaseParsedType) else moduleName
        self.assignments = assignments if assignments != None else []
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1} -> {2}>".format(self.__class__.__name__,
                                        self.assignments,
                                        self.moduleName)
        
class GlobalAssignment(ParsedType):
    def __init__(self, variable, value):
        ParsedType.__init__(self, variable)
        self.variable = variable
        self.value = value
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1} = {2}>".format(self.__class__.__name__,
                                        self.variable,
                                        self.value)
    

SPECIAL_VALUES = {
    "?NONE" 
        : None,     # FORCE value specification in template slot
    "?DERIVE"
        : object(),   # Same as default=None
}
    
TYPES = {
    "?VARIABLE"
        : object,   # check isinstance vs ?VARIABLE = TRUE
    "SYMBOL"
        : Symbol,
    "STRING"
        : String,
    "LEXEME"
        : Lexeme,
    "INTEGER"
        : Integer,
    "FLOAT"
        : Float,
    "NUMBER"
        : Number
}

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
        if isinstance(position, dict):
            makeImpl = makeInstanceDict
        else:
            makeImpl = makeInstance
        try:
            return makeImpl(cls1, position)(s,l,t)
        except:
            return makeImpl(cls2, position)(s,l,t)
            
    return tryMakeAction
    
