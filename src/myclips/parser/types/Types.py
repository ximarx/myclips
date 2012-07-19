from myclips.parser.Functions import FunctionsManager
import pyparsing
from myclips.parser.Templates import TemplatesManager, TemplateDefinition, SlotDefinition as TemplateSlotDefinition,\
    Attribute_TypeConstraint
from myclips.parser.Globals import GlobalsManager

FuncNames = [
    # FUNCTIONS
    "+", "-", "/", "*", "div", "mod",
    "max", "min", "abs",
    "float", "integer"
    "str-cat", "str-index", "str-length", "sub-string",
    # ACTIONS
    "assert", "retract", "modify", "duplicate",
    "bind",
    "printout",
    "read",
    "set-strategy", "refresh"
    # CUSTOM-ACTIONS
    "trace-rule", "trace-wme", "trigger-event",
    # PREDICATES
    "eq", "neq", "=", "<>", ">", ">=", "<", "<=",
    "evenp", "oddp", "integerp", "floatp", "numberp", "stringp", "symbolp", "lexemep"
]

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
        return "<{0}:{1},converted={2}:{3}>".format(self.__class__.__name__, 
                                                        self.content, 
                                                        evaluated.__class__.__name__, 
                                                        evaluated )

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
        return "<{0}:{1},converted={2}:{3}>".format(self.__class__.__name__,
                                                        self.content, 
                                                        self.content.__class__.__name__, 
                                                        self.content )
    
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
    def __init__(self, content, globalsManager=None):
        Variable.__init__(self, content)
        self.globalsManager = (GlobalsManager.instance 
                                    if not isinstance(globalsManager, GlobalsManager)
                                    else globalsManager)
        self.checked=False
        

class FunctionCall(ParsedType):
    def __init__(self, funcName, funcArgs=None, funcManager=None):
        ParsedType.__init__(self, funcName)
        self.funcManager = (FunctionsManager.instance 
                                if funcManager is None or not isinstance(funcManager, FunctionsManager)
                                    else funcManager)
        
        self.funcName = funcName.evaluate()
        self.funcArgs = funcArgs if funcArgs != None else []
        self.funcDefinition = None
        try:
            self.funcDefinition = self.funcManager.getFuncDefinition(self.funcName)
            checkResult, errMsg = self.funcDefinition.isValidCall(self.funcArgs)
            if not checkResult:
                raise pyparsing.ParseFatalException("Function {0} {1}".format(self.funcName, errMsg))
        except KeyError:
            raise pyparsing.ParseException("Missing function declaration for {0}".format(self.funcName))
            
        # TODO
        #checkResult, errMsg = FuncNames[self.funcName].isValidCall(funcArgs)
        #if not checkResult:
        #    import pyparsing
        #    raise pyparsing.ParseFatalException(errMsg)
            
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},args={2}>".format(self.__class__.__name__,
                                        self.funcName,
                                        self.funcArgs )

class DefFactsConstruct(ParsedType):
    def __init__(self, deffactsName, deffactsComment=None, rhs=None):
        ParsedType.__init__(self, deffactsName)
        self.deffactsName = deffactsName.evaluate()
        self.deffactsComment = deffactsComment.evaluate().strip('"') if deffactsComment != None else None
        self.rhs = rhs if rhs != None else []
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},comment={2},rhs={3}>".format(self.__class__.__name__,
                                        self.deffactsName,
                                        self.deffactsComment,
                                        self.rhs )

class OrderedRhsPattern(ParsedType):
    #converter = lambda self, t: [x.evaluate() if isinstance(x, ParsedType) else x for x in t]
    def __repr__(self, *args, **kwargs):
        return "<{0},values={1}>".format(self.__class__.__name__,
                                        str(self.content).replace("[", "{").replace("}", "]")) #better formatting with pretty print

class TemplateRhsPattern(ParsedType):
    def __init__(self, templateName, templateSlots=None):
        ParsedType.__init__(self, templateName)
        self.templateName = templateName.evaluate() if isinstance(templateName, ParsedType) else templateName
        self.templateSlots =  templateSlots if templateName != None else []
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},slots={2}>".format(self.__class__.__name__,
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
        return "<{0}:{1},values={2}>".format(self.__class__.__name__,
                                        self.slotName,
                                        self.slotValue)

class SingleFieldRhsSlot(FieldRhsSlot):
    def __init__(self, slotName, slotValue):
        FieldRhsSlot.__init__(self, slotName)
        self.slotName = slotName.evaluate() if isinstance(slotName, ParsedType) else slotName 
        self.slotValue = slotValue

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},value={2}>".format(self.__class__.__name__,
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
        return "<{0}:{1},comment={2},declarations={3},lhs={4},rhs={5}>".format(self.__class__.__name__,
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
    def __init__(self, templateName, templateSlots=None, templatesManager=None):
        PatternCE.__init__(self, templateName)
        self.templateName = templateName.evaluate() if isinstance(templateName, ParsedType) else templateName
        self.templateSlots = templateSlots if templateSlots != None else []
        self.templatesManager = (TemplatesManager.instance 
                                    if not isinstance(templatesManager, TemplatesManager)
                                    else templatesManager)
        self.templateDefinition = None
        try:
            self.templateDefinition = self.templatesManager.getTemplateDefinition(self.templateName)
        except KeyError:
            raise pyparsing.ParseException("Missing declaration for template {0}".format(self.templateName))
        
        try:
            for (index, field) in enumerate(self.templateSlots):
                slotDef = self.templateDefinition.getSlotDefinition(field.slotName)
                
                # need to check:
                    # 1: if slot type is correct (single/multi)
                        # 1.a: if slot is multi, but parsed as single (case len = 1)
                        #    cast multi -> single
                        # 1.b: if slot is single, but parsed as multi (case len = 0)
                        #    case single -> multi
                    # 2: check if type constraints are valid for submitted type
                
                if slotDef.getSlotType() == TemplateSlotDefinition.TYPE_SINGLE \
                    and isinstance(field, MultiFieldLhsSlot):
                    
                    # cast to single
                    field = SingleFieldLhsSlot(field.slotName, field.slotValue[0] if len(field.slotValue) == 1 else NullValue())
                    self.templateSlots[index] = field
                    # TODO maybe add a check for value type not list
                    
                    
                elif slotDef.getSlotType() == TemplateSlotDefinition.TYPE_MULTI \
                    and isinstance(field, SingleFieldLhsSlot):
                    
                    # cast to multi
                    field = MultiFieldLhsSlot(field.slotName, [field.slotValue])
                    self.templateSlots[index] = field
                    # TODO maybe add a converstion list(slotValue) -> slotValue
                    
                for sAttr in slotDef.getSlotAttributes():
                    # default value attribute has not to be checked now, only on mock generation
                    if isinstance(sAttr, Attribute_TypeConstraint):
                        # check vs types
                        allowedTypes = sAttr.getAllowedTypes()
                    
                        # field.slotValue = Constraint
                        #                        '- Positive|NegativeTerm
                        #                                '- BaseParsedType|Variable|FunctionCall
                        # OR
                        #
                        # field.slotValue = ConnectedConstraint
                        #                        '- Positive|NegativeTerm
                        #                                '- BaseParsedType|Variable|FunctionCall
                        #                        '- Constraint
                        #                                '- Positive|NegativeTerm
                        #                                        '- BaseParsedType|Variable|FunctionCall
                        #
                        #
                        # 1: first go deep inside the SingleFieldLhsSlot
                        #
                        valuesToCheck = []
                        valuesToScan = []
                        if isinstance(field, SingleFieldLhsSlot):
                            valuesToScan.append(field.slotValue) 
                        elif isinstance(field, MultiFieldLhsSlot):
                            valuesToScan = field.slotValue

                        for toScan in valuesToScan:
                            valuesToCheck.append(toScan.constraint.term)
                            if isinstance(toScan, ConnectedConstraint):
                                valuesToCheck += [x[1].term for x in toScan.connectedConstraints]

                        # check if ANY of the array is True:
                        #    True = term is not an allowedType or term (function call) return value is not an allowedType
                        checkForInvalid = [False if isinstance(term, (Variable, NullValue))
                                                else not any([issubclass(retType, allowedTypes) for retType in term.funcDefinition.getReturnTypes()]) if isinstance(term, FunctionCall) 
                                                    else not isinstance(term, allowedTypes)
                                            for term in valuesToCheck]
                        
                        if any(checkForInvalid):
                            errorArg = valuesToCheck[checkForInvalid.index(True)]
                            raise pyparsing.ParseFatalException("A {2} value found doesn't match the allowed types {3} for slot {0} of template {1}".format(
                                        field.slotName,
                                        self.templateName,
                                        "function {0} return".format(errorArg.funcName) if isinstance(errorArg, FunctionCall) else errorArg.__class__.__name__,
                                        tuple([t.__name__ for t in allowedTypes])
                                    ))
                                
            
        except KeyError:
            raise pyparsing.ParseFatalException("Invalid slot {0} not defined in corresponding deftemplate {1}".format(
                                                        field.slotName,
                                                        self.templateName
                                                    ))
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},slots={2}>".format(self.__class__.__name__,
                                    self.templateName,
                                    self.templateSlots
                                    )
        
class AssignedPatternCE(PatternCE):
    def __init__(self, variable, pattern):
        PatternCE.__init__(self, variable)
        self.variable = variable
        self.pattern = pattern
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},variable={2}>".format(self.__class__.__name__,
                                    self.variable,
                                    self.pattern
                                    )
    

class NotPatternCE(PatternCE):
    def __init__(self, pattern):
        if isinstance(pattern, AssignedPatternCE):
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
        # connectedConstraint is [#CONNECTIVE, Constraint]
        #     OR
        # connectedConstraint is [#CONNECTIVE, ConnectedConstraint]
        # i need to linearize all ConnectedConstraint as a single ConnectedConstraint
        # with self.constraints = [#CONNECTIVE, Constraint]
        connective, subconstraints = connectedConstraints
        self.connectedConstraints = [[connective, subconstraints.constraint]]
        if isinstance(subconstraints, ConnectedConstraint):
            # need to linearize it
            self.connectedConstraints += subconstraints.connectedConstraints

        # now i need to sort it!
        # priority: ~,&,|
        #TODO sort function / nested connected handling 
            
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},connected={2}>".format(self.__class__.__name__,
                                    self.constraint,
                                    self.connectedConstraints
                                    )
    
class Term(ParsedType):
    def __init__(self, term):
        ParsedType.__init__(self, term)
        self.term = term
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                    self.term,
                                    )

class PositiveTerm(Term):
    def __init__(self, term, isNot=None):
        Term.__init__(self, term)
        if isNot is not None:
            raise ValueError()

        
class NegativeTerm(Term):
    def __init__(self, term, isNot=None):
        Term.__init__(self, term)
        if isNot is None:
            raise ValueError()
    
    
class FieldLhsSlot(ParsedType):
    def __init__(self, slotName):
        ParsedType.__init__(self, slotName)
        self.slotName = slotName.evaluate() if isinstance(slotName, BaseParsedType) else slotName

class MultiFieldLhsSlot(FieldLhsSlot):
    def __init__(self, slotName, slotValue=None):
        FieldLhsSlot.__init__(self, slotName)
        self.slotValue = slotValue if slotValue != None else []

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},value={2}>".format(self.__class__.__name__,
                                        self.slotName,
                                        self.slotValue)

class SingleFieldLhsSlot(FieldLhsSlot):
    def __init__(self, slotName, slotValue):
        FieldLhsSlot.__init__(self, slotName)
        self.slotValue = slotValue

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},value={2}>".format(self.__class__.__name__,
                                        self.slotName,
                                        self.slotValue)    

class SlotDefinition(ParsedType):
    def __init__(self, slotName, attributes=None):
        ParsedType.__init__(self, slotName)
        self.slotName = slotName.evaluate() if isinstance(slotName, BaseParsedType) else slotName
        self.attributes = attributes if attributes != None else []
        if len(self.attributes) != len(set([x.__class__ for x in self.attributes])):
            raise pyparsing.ParseFatalException("Multiple definition for same type of attribute")

class SingleSlotDefinition(SlotDefinition):

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},attributes={2}>".format(self.__class__.__name__,
                                        self.slotName,
                                        self.attributes)    

class MultiSlotDefinition(SlotDefinition):

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},attributes={2}>".format(self.__class__.__name__,
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
        self.allowedTypes = tuple([TYPES[x] for x in allowedTypes]) if isinstance(allowedTypes, list) else tuple([TYPES["?VARIABLE"]])
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                        self.allowedTypes)    

class DefTemplateConstruct(ParsedType):
    def __init__(self, templateName, templateComment=None, slots=None, templatesManager=None):
        ParsedType.__init__(self, templateName)
        self.templateName = templateName.evaluate() if isinstance(templateName, BaseParsedType) else templateName
        self.templateComment = templateComment.evaluate().strip('"') if isinstance(templateComment, BaseParsedType) else None
        self.slots = slots if slots != None else []
        if len(self.slots) != len(set([x.slotName for x in self.slots])):
            raise pyparsing.ParseFatalException("Multiple definition for same slot name")
        
        
        self.templatesManager = (TemplatesManager.instance 
                                    if not isinstance(templatesManager, TemplatesManager)
                                    else templatesManager)
        
        # check if a template with the same name is already available
        try:
            self.templatesManager.getTemplateDefinition(self.templateName)
            raise pyparsing.ParseFatalException("Multiple definition for template {0}".format(self.templateName))
        except KeyError:
            # create slot template definitions
            tslots = dict([(sd.getSlotName(), sd) for sd 
                                in [TemplateSlotDefinition.fromParserSlotDefinition(slot) 
                                        for slot in self.slots]])
            # create a template definition instance
            tdef = TemplateDefinition(self.templateName, tslots)
            # push new template definition to the manager
            self.templatesManager.registerTemplate(tdef)
            
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},comment='{2}',slots={3}>".format(self.__class__.__name__,
                                        self.templateName,
                                        self.templateComment,
                                        self.slots)
        
class DefGlobalConstruct(ParsedType):
    def __init__(self, assignments=None, moduleName=None, globalsManager=None):
        ParsedType.__init__(self, assignments)
        self.moduleName = moduleName.evaluate() if isinstance(moduleName, BaseParsedType) else moduleName
        self.assignments = assignments if assignments != None else []
        self.globalsManager = (GlobalsManager.instance 
                                    if not isinstance(globalsManager, GlobalsManager)
                                    else globalsManager)
        for ass in self.assignments:
            self.globalsManager.addGlobal(ass.variable.evaluate(), ass.value, self.moduleName)
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},module={2}>".format(self.__class__.__name__,
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
    
class NullValue(BaseParsedType):
    
    def __init__(self):
        BaseParsedType.__init__(self, None)

SPECIAL_VALUES = {
    "?NONE" 
        : None,     # FORCE value specification in template slot
    "?DERIVE"
        : NullValue(),   # Same as default=None
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
            elif not isinstance(v, (str, unicode, int)):
                targs[k] = v
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
    
