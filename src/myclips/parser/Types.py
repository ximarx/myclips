#import pyparsing
import myclips
from myclips.TemplatesManager import SlotDefinition as TemplateSlotDefinition,\
    Attribute_TypeConstraint, TemplateDefinition
from myclips.GlobalsManager import GlobalVarDefinition
from myclips.Scope import Scope, ScopeImport, ScopeExport
from myclips.MyClipsException import MyClipsException
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_ExactArgsLength, Constraint_MinArgsLength
from myclips.rete.WME import WME


class ParsedType(object):
    '''
    Base class for all parsed types
    Conversion to native type is delegated
    to evaluate() call
    '''
    
    __FIELDS__=[]
    
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
    def toClipsStr(self):
        return str(self)


class BaseParsedType(ParsedType):
    '''
    Base class for all 1:1 native mappable types
    Conversion to native type is done as soon as possible
    and never done again
    '''
    
    __FIELDS__=['content']
    
    def __init__(self, content):
        ParsedType.__init__(self, content)
        if hasattr(self, 'converter'):
            self.content = self.converter(self.content)
        
    def evaluate(self):
        return self.content
    
    def toClipsStr(self):
        return str(self.content)
    
    def pyEqual(self, value):
        return self.content == value

    def __eq__(self, other):
        return self.__class__ == other.__class__ \
                and self.evaluate() == other.evaluate()
                
    def __neq__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash(self.content)

    def __str__(self):
        return str(self.evaluate())

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                  self.content)
    
class HasScope(object):
    def __init__(self, modulesManager):
        self._scope = modulesManager.currentScope
    
    @property
    def scope(self):
        return self._scope
    
    @staticmethod
    def cleanName(constructName):
        """ 
        split the name and return last segment
            MODULE::NAME -> NAME
            MODULE::NAME::NAME -> NAME::NAME
            NAME -> NAME
        """
        return constructName.split("::", 2)[-1]
    
class Number(BaseParsedType):
    pass

class Lexeme(BaseParsedType):
    pass

class Integer(Number):
    converter = lambda self, t: int(t)
    def pyEqual(self, value):
        return value.__class__ == int and self.evaluate() == value
    pass

class Symbol(Lexeme):
    def pyEqual(self, value):
        return isinstance(value, (str, unicode)) and self.evaluate() == value
    pass

class String(Lexeme):
    converter = lambda self, t: '"'+str(t)+'"'
    def pyEqual(self, value):
        return isinstance(value, (str, unicode)) and self.evaluate() == value
    pass

class Float(Number):
    converter = float
    def pyEqual(self, value):
        return value.__class__ == float and self.evaluate() == value
    pass

class InstanceName(BaseParsedType):
    pass

class Variable(ParsedType):
    __FIELDS__=['content']
    def __init__(self, content):
        ParsedType.__init__(self, content)
    def toClipsStr(self):
        return self.evaluate()
        

class SingleFieldVariable(Variable):
    converter = lambda self, t: "?"+self.content.evaluate()
    def __init__(self, content):
        Variable.__init__(self, content)

class MultiFieldVariable(Variable):
    converter = lambda self, t: "$?"+self.content.evaluate()
    def __init__(self, content):
        Variable.__init__(self, content)

class UnnamedSingleFieldVariable(Variable):
    converter = lambda self, t: "?"
    def __init__(self, *args, **kargs):
        Variable.__init__(self, None)

class UnnamedMultiFieldVariable(Variable):
    converter = lambda self, t: "$?"
    def __init__(self, *args, **kargs):
        Variable.__init__(self, None)

class GlobalVariable(Variable, HasScope):
    converter = lambda self, t: "?*"+self.content.evaluate()+"*"
    def __init__(self, content, modulesManager, ignoreCheck=False):
        Variable.__init__(self, content)
        HasScope.__init__(self, modulesManager)
        if not ignoreCheck:
            if not self.scope.globalsvars.has(self.evaluate()):
                # this variable is undefined in this scope
                # need to raise exception
                myclips.logger.error("Global variable %s non definita!", self.evaluate())
                raise TypeInstanceCreationError("Global variable {0} was referenced, but is not defined.".format(
                                self.evaluate()
                            ))
        

class FunctionCall(ParsedType, HasScope):
    __FIELDS__=['funcName','funcArgs']
    def __init__(self, funcName, modulesManager, funcArgs=None):
        ParsedType.__init__(self, funcName)
        HasScope.__init__(self, modulesManager)
        
        self.funcName = funcName.evaluate() if isinstance(funcName, BaseParsedType) else funcName
        self.funcArgs = funcArgs if funcArgs != None else []
        self.funcDefinition = None
        try:
            self.funcDefinition = self.scope.functions.getDefinition(self.funcName)
        except KeyError:
            raise TypeRecoverableInstanceCreationError("Missing function declaration for {0}".format(self.funcName))
        else:
            checkResult, errMsg = self.funcDefinition.isValidCall(self.funcArgs)
            if not checkResult:
                raise TypeInstanceCreationError("Function {0} {1}".format(self.funcName, errMsg))
            
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},args={2}>".format(self.__class__.__name__,
                                        self.funcName,
                                        repr(self.funcArgs) )
        
    def toClipsStr(self):
        return "(%s %s)"%(self.funcName," ".join([x.toClipsStr() for x in self.funcArgs]))

class DefFactsConstruct(ParsedType, HasScope):
    __FIELDS__=['deffactsName','deffactsComment','rhs']
    def __init__(self, deffactsName, modulesManager, deffactsComment=None, rhs=None):
        ParsedType.__init__(self, deffactsName)
        HasScope.__init__(self, modulesManager)
        deffactsName = deffactsName.evaluate() if isinstance(deffactsName, BaseParsedType) else deffactsName
        self.deffactsName = HasScope.cleanName(deffactsName)
        self.deffactsComment = deffactsComment.evaluate().strip('"') if deffactsComment != None else None
        self.rhs = rhs if rhs != None else []
        
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{4}::{1},comment={2},rhs={3}>".format(self.__class__.__name__,
                                        self.deffactsName,
                                        self.deffactsComment,
                                        self.rhs,
                                        self.scope.moduleName
                                        )
    

class OrderedRhsPattern(ParsedType):
    #converter = lambda self, t: [x.evaluate() if isinstance(x, ParsedType) else x for x in t]
    __FIELDS__=['values']
    def __init__(self, values):
        ParsedType.__init__(self, values)
        self.values = values
    
    def __repr__(self, *args, **kwargs):
        return "<{0},values={1}>".format(self.__class__.__name__,
                                        str(self.values).replace("[", "{").replace("}", "]")) #better formatting with pretty print

class TemplateRhsPattern(ParsedType, HasScope):
    __FIELDS__=['templateName', 'templateSlots']
    def __init__(self, templateName, modulesManager, templateSlots=None):
        ParsedType.__init__(self, templateName)
        HasScope.__init__(self, modulesManager)
        self.templateName = templateName.evaluate() if isinstance(templateName, ParsedType) else templateName
        self.templateSlots =  templateSlots if templateName != None else []
        try:
            self.templateDefinition = self.scope.templates.getDefinition(self.templateName)
        except:
            raise TypeRecoverableInstanceCreationError("Missing template declaration for {0}".format(
                        self.templateName
                    ))
        # TODO
        # CHECK slots VS templateDefinition
        myclips.logger.debug("TODO: add check TemplateRhsPattern slots vs TemplateDefinition")
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{3}::{1},slots={2}>".format(self.__class__.__name__,
                                        self.templateName,
                                        self.templateSlots,
                                        self.templateDefinition.moduleName
                                        )
    
class FieldRhsSlot(ParsedType):
    __FIELDS__=['slotName', 'slotValue']    
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


class DefRuleConstruct(ParsedType, HasScope):
    __FIELDS__=['defruleName', 'defruleComment', "defruleDeclaration", "lhs", "rhs"]    
    def __init__(self, defruleName, modulesManager, defruleComment=None, defruleDeclaration=None, lhs=None, rhs=None):
        ParsedType.__init__(self, defruleName)
        HasScope.__init__(self, modulesManager)
        
        # evaluate and clean rulename
        defruleName = defruleName.evaluate() if isinstance(defruleName, ParsedType) else defruleName
        self.defruleName = HasScope.cleanName(defruleName)
         
        self.defruleComment = defruleComment.evaluate().strip('"') if isinstance(defruleComment, ParsedType) else None
        self.defruleDeclaration = defruleDeclaration if defruleDeclaration != None else []
        self.lhs = lhs if lhs != None else [] 
        self.rhs = rhs if rhs != None else []
        
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{6}::{1},comment={2},declarations={3},lhs={4},rhs={5}>".format(self.__class__.__name__,
                                        self.defruleName,
                                        self.defruleComment,
                                        self.defruleDeclaration,
                                        self.lhs,
                                        self.rhs,
                                        self.scope.moduleName
                                        )
        
class RuleProperty(ParsedType):
    __FIELDS__=['propertyName', 'propertyValue']
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

class OrderedPatternCE(PatternCE, HasScope):
    __FIELDS__=['constraints']
    def __init__(self, constraints, modulesManager):
        PatternCE.__init__(self, constraints)
        HasScope.__init__(self, modulesManager)
        self.constraints = constraints
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:constraints={1},module={2}>".format(
                                        self.__class__.__name__,
                                        self.constraints,
                                        self.scope.moduleName
                                    )

class TemplatePatternCE(PatternCE, HasScope):
    __FIELDS__=['templateName', 'templateSlots']
    def __init__(self, templateName, modulesManager, templateSlots=None):
        PatternCE.__init__(self, templateName)
        HasScope.__init__(self, modulesManager)
        
        templateName = templateName.evaluate() if isinstance(templateName, ParsedType) else templateName
        self.templateName = HasScope.cleanName(templateName)
        
        self.templateSlots = templateSlots if templateSlots != None else []
        
        self.templateDefinition = None
        try:
            self.templateDefinition = self.scope.templates.getDefinition(self.templateName)
        except KeyError:
            raise TypeRecoverableInstanceCreationError("Missing declaration for template {0}".format(self.templateName))
        
        try:
            for (index, field) in enumerate(self.templateSlots):
                slotDef = self.templateDefinition.getSlot(field.slotName)
                
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
                                                else not any([issubclass(retType, allowedTypes) for retType in term.funcDefinition.returnTypes]) if isinstance(term, FunctionCall) 
                                                    else not isinstance(term, allowedTypes)
                                            for term in valuesToCheck]
                        
                        if any(checkForInvalid):
                            errorArg = valuesToCheck[checkForInvalid.index(True)]
                            raise TypeInstanceCreationError("A {2} value found doesn't match the allowed types {3} for slot {0} of template {4}::{1}".format(
                                        field.slotName,
                                        self.templateName,
                                        "function {0} return".format(errorArg.funcName) if isinstance(errorArg, FunctionCall) else errorArg.__class__.__name__,
                                        tuple([t.__name__ for t in allowedTypes]),
                                        self.templateDefinition.moduleName
                                    ))
                                
            
        except KeyError:
            raise TypeInstanceCreationError("Invalid slot {0} not defined in corresponding deftemplate {2}::{1}".format(
                                                        field.slotName,
                                                        self.templateName,
                                                        self.templateDefinition.moduleName
                                                    ))
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{3}::{1},slots={2}>".format(self.__class__.__name__,
                                    self.templateName,
                                    self.templateSlots,
                                    self.templateDefinition.moduleName
                                    )
        
class AssignedPatternCE(PatternCE):
    __FIELDS__=['variable', 'pattern']
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
    __FIELDS__=['pattern']
    def __init__(self, pattern):
        if isinstance(pattern, AssignedPatternCE):
            raise TypeInstanceCreationError("A pattern CE cannot be bound to a pattern-address within a not CE")
        PatternCE.__init__(self, pattern)
        self.pattern = pattern
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                    self.pattern
                                    )

class AndPatternCE(PatternCE):
    __FIELDS__=['patterns']
    def __init__(self, patterns):
        if len(patterns) == 0 :#and isinstance(patterns[0], AssignedPatternCE):
            raise TypeInstanceCreationError("Syntax Error: Check appropriate syntax for the and conditional element")
        PatternCE.__init__(self, patterns)
        self.patterns = patterns
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                    self.patterns
                                    )

class OrPatternCE(PatternCE):
    __FIELDS__=['patterns']
    def __init__(self, patterns):
        if len(patterns) > 0 and isinstance(patterns[0], AssignedPatternCE):
            raise TypeInstanceCreationError("Syntax Error:  Check appropriate syntax for the first field of a pattern.")
        PatternCE.__init__(self, patterns)
        self.patterns = patterns
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                    self.patterns
                                    )


class TestPatternCE(PatternCE):
    __FIELDS__=['function']
    def __init__(self, function):
        PatternCE.__init__(self, function)
        self.function = function
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                    self.function,
                                    )

 
class Constraint(ParsedType):
    __FIELDS__=['constraint']
    def __init__(self, constraint, connectedConstraints=None):
        ParsedType.__init__(self, constraint)
        self.constraint = constraint
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                    self.constraint
                                    )

class ConnectedConstraint(ParsedType):
    __FIELDS__=['constraint', 'connectedConstraints']
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
    __FIELDS__=['term']
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
    __FIELDS__=['slotName', 'slotValue']
    def __init__(self, slotName, slotValue):
        ParsedType.__init__(self, slotName)
        self.slotName = slotName.evaluate() if isinstance(slotName, BaseParsedType) else slotName
        self.slotValue = slotValue

class MultiFieldLhsSlot(FieldLhsSlot):
    def __init__(self, slotName, slotValue=None):
        FieldLhsSlot.__init__(self, slotName, slotValue if slotValue != None else [])

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},value={2}>".format(self.__class__.__name__,
                                        self.slotName,
                                        self.slotValue)

class SingleFieldLhsSlot(FieldLhsSlot):
    def __init__(self, slotName, slotValue):
        FieldLhsSlot.__init__(self, slotName, slotValue)

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},value={2}>".format(self.__class__.__name__,
                                        self.slotName,
                                        self.slotValue)    

class SlotDefinition(ParsedType):
    __FIELDS__=['slotName', 'attributes']
    def __init__(self, slotName, attributes=None):
        ParsedType.__init__(self, slotName)
        self.slotName = slotName.evaluate() if isinstance(slotName, BaseParsedType) else slotName
        self.attributes = attributes if attributes != None else []
        if len(self.attributes) != len(set([x.__class__ for x in self.attributes])):
            raise TypeInstanceCreationError("Multiple definition for same type of attribute")

class SingleSlotDefinition(SlotDefinition):
    
    def __init__(self, slotName, attributes=None):
        SlotDefinition.__init__(self, slotName, attributes=attributes)

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},attributes={2}>".format(self.__class__.__name__,
                                        self.slotName,
                                        self.attributes)    

class MultiSlotDefinition(SlotDefinition):

    def __init__(self, slotName, attributes=None):
        SlotDefinition.__init__(self, slotName, attributes=attributes)

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},attributes={2}>".format(self.__class__.__name__,
                                        self.slotName,
                                        self.attributes)    

class Attribute(ParsedType):
    pass

class DefaultAttribute(Attribute):
    __FIELDS__=['defaultValue']
    def __init__(self, defaultValue):
        Attribute.__init__(self, defaultValue)
        self.defaultValue = defaultValue if isinstance(defaultValue, ParsedType) else SPECIAL_VALUES[defaultValue]
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                        self.defaultValue)    

class TypeAttribute(Attribute):
    __FIELDS__=['allowedTypes']
    def __init__(self, allowedTypes=None):
        Attribute.__init__(self, allowedTypes)
        self.allowedTypes = tuple([TYPES[x] for x in allowedTypes]) if isinstance(allowedTypes, list) else tuple([TYPES["?VARIABLE"]])
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}>".format(self.__class__.__name__,
                                        self.allowedTypes)    

class DefTemplateConstruct(ParsedType, HasScope):
    __FIELDS__=['templateName', 'templateComment', 'slots']
    def __init__(self, templateName, modulesManager, templateComment=None, slots=None):
        ParsedType.__init__(self, templateName)
        HasScope.__init__(self, modulesManager)
        
        templateName = templateName.evaluate() if isinstance(templateName, BaseParsedType) else templateName
        self.templateName = HasScope.cleanName(templateName)
        
        self.templateComment = templateComment.evaluate().strip('"') if isinstance(templateComment, BaseParsedType) else None
        self.slots = slots if slots != None else []
        if len(self.slots) != len(set([x.slotName for x in self.slots])):
            raise TypeInstanceCreationError("Multiple definition for same slot name")
        
        
        # check if a template with the same name is already available
        try:
            #scope.templates.getTemplateDefinitions(self.templateName)
            self.scope.templates.getDefinition(self.templateName)
            raise TypeInstanceCreationError("Multiple definition for template {0}".format(self.templateName))
        except KeyError:
            # create slot template definitions
            tslots = dict([(sd.getSlotName(), sd) for sd 
                                in [TemplateSlotDefinition.fromParserSlotDefinition(slot) 
                                        for slot in self.slots]])
            
            # push new template definition into the manager
            self.scope.templates.addDefinition(TemplateDefinition(self.scope.moduleName, self.templateName, self, tslots))
            
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{4}::{1},comment='{2}',slots={3}>".format(self.__class__.__name__,
                                        self.templateName,
                                        self.templateComment,
                                        self.slots,
                                        self.scope.moduleName)
        
class DefGlobalConstruct(ParsedType, HasScope):
    __FIELDS__=['moduleName', 'assignments']
    def __init__(self, modulesManager, assignments=None, moduleName=None):
        ParsedType.__init__(self, assignments)
        
        # scope has the current scope
        # if no moduleName is submitted
        # the current scope is the one submitted
        # otherwise i have to check the scope
        # for moduleName and change current scope to it
        # or raise exception
        if moduleName != None:
            moduleName = moduleName.evaluate() if isinstance(moduleName, BaseParsedType) else moduleName
            modulesManager.changeCurrentScope(moduleName)
        
        # if not exception raised, the scope var
        # has the real current scope (updated if have to)
        # i can call parent constructor now     
        HasScope.__init__(self, modulesManager)
        
        self.assignments = assignments if assignments != None else []
        
        for ass in self.assignments:
            self.scope.globalsvars.addDefinition(GlobalVarDefinition(self.scope.moduleName, ass.variable.evaluate(), ass))
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1},module={2}>".format(self.__class__.__name__,
                                        self.assignments,
                                        self.scope.moduleName)
        
class GlobalAssignment(ParsedType):
    __FIELDS__=['variable', 'value', 'runningValue']
    def __init__(self, variable, value):
        ParsedType.__init__(self, variable)
        self.variable = variable
        self.value = value
        self.runningValue = value
        
    def __repr__(self, *args, **kwargs):
        return "<{0}:{1} = {2}>".format(self.__class__.__name__,
                                        self.variable,
                                        self.value)
        
        
class PortItem(ParsedType):
    __FIELDS__=['portType', 'portNames']
    def __init__(self, content):
        # content can be:
        #    ?ALL | ?NONE | list
        # list can be:
        #    [Symbol, [Symbol] ] | [Symbol, ?ALL] | [Symbol, ?NONE]
        # first list Symbol can be:
        #    deftemplate | defglobal | deffunction
        # second list Symbol is a list of construct names 
        #    (the type of construct it restricted by first Symbol)
        
        self.portType = None
        self.portNames = None
        
        # first check construct type
        if isinstance(content, list):
            # need to go deeper
            type2PromiseMap = {"deftemplate": Scope.PROMISE_TYPE_TEMPLATE,
                               "defglobal": Scope.PROMISE_TYPE_GLOBAL,
                               "deffunction": Scope.PROMISE_TYPE_FUNCTION}
            try:
                self.portType = type2PromiseMap[content[0].evaluate()]
            except KeyError:
                raise TypeInstanceCreationError("Syntax Error: Check appropriate syntax for defmodule export specification")
            
            # now i need to evalutate the name of the construct
            if isinstance(content[1], list):
                # i got a list, so all symbols are construct name
                # but i can't check if they are valid here
                # need to pospone check on defmodule/import/export creation
                self.portNames = [x.evaluate() if self.portType != Scope.PROMISE_TYPE_GLOBAL
                                        else "?*%s*"%x.evaluate()
                                    for x in content[1]] # only cast to real str
            else:
                if content == "?ALL":
                    self.portNames = Scope.PROMISE_NAME_ALL
                elif content == "?NONE":
                    self.portNames = Scope.PROMISE_NAME_NONE
                else:
                    raise TypeInstanceCreationError("Syntax Error: Check appropriate syntax for defmodule export specification")
                
        else:
            if content == "?ALL":
                self.portType = Scope.PROMISE_NAME_ALL
                self.portNames = Scope.PROMISE_NAME_ALL
            elif content == "?NONE":
                self.portType = Scope.PROMISE_NAME_NONE
                self.portNames = Scope.PROMISE_NAME_NONE
            else:
                raise TypeInstanceCreationError("Syntax Error: Check appropriate syntax for defmodule export specification")
        # not end object construction
        ParsedType.__init__(self, self.portType)
        
        
        
class ImportSpecification(ParsedType):
    __FIELDS__=['item', 'moduleName']
    def __init__(self, moduleName, item, modulesManager):
        moduleName = moduleName.evaluate() if isinstance(moduleName, BaseParsedType) else moduleName # cast to raw
        ParsedType.__init__(self, moduleName)
        self.moduleName = moduleName
        self.item = item
        
        # check if the scope of that name exists
        if not modulesManager.isDefined(moduleName):
            raise TypeInstanceCreationError("Unable to find defmodule %s"%moduleName)
        
        
class ExportSpecification(ParsedType):
    __FIELDS__=['item']
    def __init__(self, item):
        ParsedType.__init__(self, item)
        self.item = item
        

class DefModuleConstruct(ParsedType, HasScope):
    __FIELDS__=['moduleName', 'comment', 'specifications']
    def __init__(self, moduleName, modulesManager, specifications=None, comment=None):
        moduleName = moduleName.evaluate() if isinstance(moduleName, BaseParsedType) else moduleName
        comment = comment.evaluate().strip('"') if isinstance(comment, BaseParsedType) else comment
        specifications = specifications if isinstance(specifications, list) else []
        
        ParsedType.__init__(self, moduleName)
        self.moduleName = moduleName
        self.comment = comment
        self.specifications = specifications
        
        # time to create che new Scope
        
        try:
            Scope(moduleName, modulesManager, imports=[
                        ScopeImport(imp.moduleName, imp.item.portType, imp.item.portNames)
                            for imp in self.specifications if isinstance(imp, ImportSpecification)
                    ], exports=[
                        ScopeExport(exp.item.portType, exp.item.portNames)
                            for exp in self.specifications if isinstance(exp, ExportSpecification)
                    ])
        except Exception, e:
            # causes of failure:
            #    moduleName already exists
            #    import from unknown module
            #    import of an unknown construct
            #    name conflicts
            # i can use the original name
            raise TypeInstanceCreationError(e.args[0])
        
        # scope is automatically changed to the new one.
        # now i can complete HasScope init and the scope
        # is the new create scope
        
        # HasScope init must che the last thing to be done, after scope creation
        HasScope.__init__(self, modulesManager)
        
        
class DefFunctionConstruct(ParsedType, HasScope):
    __FIELDS__=['functionName', 'comment', 'params', 'actions']
    def __init__(self, functionName, modulesManager, params=None, actions=None, comment=None ):
        functionName = HasScope.cleanName(functionName.evaluate() if isinstance(functionName, BaseParsedType) else functionName)
        ParsedType.__init__(self, functionName)
        HasScope.__init__(self, modulesManager)
        
        self.functionName = functionName
        self.comment = comment.evaluate().strip('"') if isinstance(comment, BaseParsedType) else comment
        self.params = [] if params is None else params
        self.actions = [] if actions is None else actions
        
        self.functionDefinition = None
        
        # lets create the function definition
        if self.scope.functions.has(functionName):
            # has function return True
            # is exists a definition
            # and it is not a forward declaration
            # system functions aren't always forwards
            # valutate systemFunction only for 
            # custom error
            if self.scope.functions.hasSystemFunction(functionName):
                raise TypeInstanceCreationError("Deffunctions are not allowed to replace external functions: %s"%functionName)
            else:
                raise TypeInstanceCreationError("Cannot define deffunction %s because of an import/export conflict"%functionName)

        # generate constraints from params
        
        constraints = []
        
        # args length
        
        minParams = len([x for x in self.params if isinstance(x, SingleFieldVariable)])
        hasMax = not isinstance(self.params[-1], MultiFieldVariable )
        
        if hasMax:
            constraints.append( Constraint_ExactArgsLength(minParams) )
        else :
            constraints.append( Constraint_MinArgsLength(minParams) )
            
        from myclips.functions.UserFunction import UserFunction
            
        functionHandler = UserFunction(self.params, self.actions)
            
        fDef = FunctionDefinition(self.scope.moduleName, functionName,
                                    linkedType=functionHandler, 
                                    returnTypes=(self.actions[-1].funcDefinition.returnTypes 
                                                    if len(self.actions) > 0 and isinstance(self.actions[-1], FunctionCall)
                                                        else self.actions[-1].__class__ if isinstance(self.actions[-1], BaseParsedType)
                                                            else (Lexeme, Number, list, WME)), 
                                    handler=functionHandler.do, 
                                    constraints=constraints, 
                                    forward=True)
        
        functionHandler.DEFINITION = fDef
                
        self.scope.functions.addDefinition(fDef)

    def __repr__(self, *args, **kwargs):
        return "<{0}:{1}::{2},comment={3},params={4},actions={5}>".format(
                        self.__class__.__name__,
                        self.scope.moduleName,
                        self.functionName,
                        '"'+self.comment+'"' if self.comment != None else '""',
                        self.params,
                        self.actions
                    )
    
class NullValue(BaseParsedType):
    
    def __init__(self):
        BaseParsedType.__init__(self, None)
        
    def __repr__(self):
        return "<nil>"

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


class TypeInstanceCreationError(MyClipsException):
    pass

class TypeRecoverableInstanceCreationError(MyClipsException):
    pass
