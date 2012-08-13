
import pyparsing as pp
import string
import myclips.parser.Types as types
import time
from myclips.ModulesManager import ModulesManager
import myclips


class Parser(object):
    
    def __init__(self, debug=False, enableComments=False, enableDirectives=False, modulesManager=None):
        
        self.subparsers = {}
        self._initied = False
        self._debug = debug
        self._enableComments = enableComments
        self._enableDirectives = enableDirectives
        self._modulesManager = (ModulesManager()
                                    if not isinstance(modulesManager, ModulesManager)
                                        else modulesManager)
        self._lastParseError = None
        # need to check if ModulesManager is ready to 
        # to get all construct. This means at least a 
        # scope must be available
        if len(self._modulesManager.getModulesNames()) == 0:
            self._modulesManager.addMainScope()
            
        
    def isInitied(self):
        return self._initied
    
    def setDebug(self, status):
        if self._debug != status:
            self._debug = status
            if self._initied:
                self._changeDebug()
        
    def setAllowDirectives(self, newStatus):
        if self._initied:
            if self._enableDirectives != newStatus:
                self._initied = False
                self.subparsers = {}
        self._enableDirectives = newStatus            

    def setAllowComments(self, newStatus):
        if self._initied:
            if self._enableComments != newStatus:
                self._initied = False
                self.subparsers = {}
        self._enableComments = newStatus            
    
    def isCommentsAllowed(self):
        return self._enableComments
    
    def isDirectivesAllowed(self):
        return self._enableDirectives
    
    def _initParsers(self):
        
        if self._initied:
            return
        
        self._initied = True


        ### INTERNAL FUNCTION FOR TYPE CREATION
                
        def makeInstance(cls, position=0):
            def makeAction(s,l,t):
                argsToUse = None
                if position != None:
                    try:
                        argsToUse = t[position].asList()
                    except:
                        argsToUse = t[position]
                else:
                    try:
                        argsToUse = t.asList()
                    except:
                        argsToUse = t
                
                try:
                    i = cls(argsToUse)
                    # need to reset last error on first positive match
                    self._lastParseError = None
                    return i
                except types.TypeRecoverableInstanceCreationError as e:
                    self._lastParseError = e.message
                    raise pp.ParseException(s,l, self._lastParseError)
                except types.TypeInstanceCreationError as e:
                    raise pp.ParseFatalException(s,l,e.message)
                    
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
                try:
                    i = cls(**targs)
                    # need to reset last error on first positive match
                    self._lastParseError = None
                    return i
                except types.TypeRecoverableInstanceCreationError as e:
                    self._lastParseError = e.message
                    raise pp.ParseException(s,l, self._lastParseError)
                except types.TypeInstanceCreationError as e:
                    raise pp.ParseFatalException(s,l,e.message)
                
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
                    
                
        def forwardParsed(bounds=None, key=None):
            def forwardAction(s,l,t):
                rlist = t.asList()
                if key != None:
                    return rlist[key]
                elif bounds != None and len(bounds) == 2:
                    return rlist[bounds[0]:bounds[1]]
                else:
                    return rlist
                    
            return forwardAction
        
        def valutateScopeChange(modulesManager):
            def changeScopeAction(s,l,t):
                constructName = t[0].evaluate() # i assume a Symbol is here
                splitted = constructName.split("::", 2)
                if len(splitted) == 2:
                    # there is a module definition
                    moduleName, _ = splitted
                    # need to valutate the currentScope
                    myclips.logger.debug("Changing scope: %s -> %s", modulesManager.currentScope.moduleName, moduleName)
                    if moduleName != modulesManager.currentScope.moduleName:
                        try:
                            modulesManager.currentScope.modules.changeCurrentScope(moduleName)
                        except ValueError, e:
                            raise pp.ParseFatalException(s,l,e.args[0])
                
            return changeScopeAction
        
        
        def doScopeChange(modulesManager):
            def changeScopeAction(s,l,t):
                moduleName = t[0].evaluate() # i assume a Symbol is here
                # need to valutate the currentScope
                myclips.logger.debug("Changing scope: %s -> %s", modulesManager.currentScope.moduleName, moduleName)
                if moduleName != modulesManager.currentScope.moduleName:
                    try:
                        modulesManager.currentScope.modules.changeCurrentScope(moduleName)
                    except ValueError, e:
                        raise pp.ParseFatalException(s,l,e.args[0])
                
            return changeScopeAction
        

        ### BASE PARSERS
        
        LPAR = pp.Literal("(").suppress()
        RPAR = pp.Literal(")").suppress()
        
        self.subparsers["SymbolParser"] = pp.Word("".join([ c for c in string.printable if c not in string.whitespace and c not in "\"'()&?|<~;" ]),
                                                          "".join([ c for c in string.printable if c not in string.whitespace and c not in "\"'()&?|<~;" ]))\
                .setParseAction(makeInstance(types.Symbol))
        
        self.subparsers["StringParser"] = pp.QuotedString('"', '\\', None, True, True)\
                .setParseAction(makeInstance(types.String))
        # StringParser alias    
        self.subparsers["CommentParser"] = self.subparsers["StringParser"]
        
        self.subparsers["IntegerParser"] = pp.Combine(pp.Optional(pp.oneOf('+ -')) + pp.Word(pp.nums))\
                .setParseAction(makeInstance(types.Integer))
        
        # try to cast to Integer first, otherwise Float
        self.subparsers["FloatParser"] = pp.Regex(r'[+-]?\d+(\.\d*)?([eE]-?\d+)?')\
                .setParseAction(tryInstance(types.Integer, types.Float))
                    
        self.subparsers["VariableSymbolParser"] = pp.Word(string.letters, "".join([ c for c in string.printable if c not in string.whitespace and c not in "*\"'()&?|<~;" ]))\
                .setParseAction(makeInstance(types.Symbol))    
                         
        self.subparsers["NumberParser"] = (self.getSParser("FloatParser") ^ self.getSParser("IntegerParser"))\
                .setParseAction(forwardParsed())
        
        #self.subparsers["InstanceNameParser"]
        
        self.subparsers["LexemeParser"] = (self.getSParser("StringParser") | self.getSParser("SymbolParser"))\
                .setParseAction(forwardParsed())
        
        self.subparsers["ConstantParser"] = (self.getSParser("NumberParser") ^ self.getSParser("LexemeParser"))\
                .setParseAction(forwardParsed())
        
        self.subparsers["SingleFieldVariableParser"] = (pp.Literal("?") - self.getSParser("VariableSymbolParser"))\
                .setParseAction(makeInstance(types.SingleFieldVariable, 1))
        
        self.subparsers["MultiFieldVariableParser"] = (pp.Literal("$?") - self.getSParser("VariableSymbolParser"))\
                .setParseAction(makeInstance(types.MultiFieldVariable, 1))
            
        self.subparsers["GlobalVariableParser"] = (
                                                   pp.Literal("?*") 
                                                   - self._sb("VariableSymbolParser").copy().leaveWhitespace() 
                                                   - pp.Literal("*").leaveWhitespace()
                                                   )\
                .setParseAction(makeInstanceDict(types.GlobalVariable, {'content': 1, 
                                                                              "modulesManager": self._modulesManager
                                                                              }))
        
        self.subparsers["VariableParser"] = (self._sb("MultiFieldVariableParser") 
                                                | self._sb("GlobalVariableParser")
                                                | self._sb("SingleFieldVariableParser"))\
                .setParseAction(forwardParsed(key=0))
        
        ### CONSTRUCTS PARSERS        
        
        self.subparsers["ExpressionParser"] = pp.Forward()
        self.subparsers["RhsFunctionCallParser"] = pp.Forward()
        
        self.subparsers["FunctionNameParser"] = (pp.oneOf(self.getModulesManager().currentScope.functions.systemFunctions )\
                                                    .setName("SystemFunctioName")\
                                                    .setParseAction(makeInstance(types.Symbol, 0))
                                                 | self.getSParser("VariableSymbolParser"))\
                .setParseAction(forwardParsed(key=0))
        
        self.subparsers["FunctionCallParser"] = (LPAR + self.getSParser("FunctionNameParser") 
                                                    + pp.Group(pp.ZeroOrMore(self.getSParser("ExpressionParser"))) 
                                                    + RPAR)\
                .setParseAction(makeInstanceDict(types.FunctionCall, {'funcName': 0,
                                                                            'funcArgs': 1, 
                                                                            "modulesManager": self._modulesManager
                                                                            }))

        self.subparsers["ExpressionParser"] << (self._sb("FunctionCallParser") 
                                                | self._sb("VariableParser")
                                                | self._sb("ConstantParser") )\
                .setParseAction(forwardParsed())
        
        self.subparsers["RhsExpressionParser"] = (self._sb("RhsFunctionCallParser") 
                                                | self._sb("VariableParser")
                                                | self._sb("ConstantParser") )\
                .setParseAction(forwardParsed())

        self.subparsers["RhsFieldParser"] = self.subparsers["ExpressionParser"].copy()

        self.subparsers["MultiFieldRhsSlotParser"] = (LPAR + self._sb("SymbolParser") + pp.Group(pp.ZeroOrMore(self._sb("RhsFieldParser"))).setResultsName("content") + RPAR )\
                .setParseAction(makeInstanceDict(types.MultiFieldRhsSlot, {"slotName" : 0, "slotValue" : "content"}))

        self.subparsers["SingleFieldRhsSlotParser"] = (LPAR + self._sb("SymbolParser") + self._sb("RhsFieldParser") + RPAR )\
                .setParseAction(makeInstanceDict(types.SingleFieldRhsSlot, {"slotName" : 0, "slotValue" : 1}))
        
        self.subparsers["RhsSlotParser"] = (self._sb('SingleFieldRhsSlotParser') | self._sb("MultiFieldRhsSlotParser"))\
                .setParseAction(forwardParsed(key=0))
        
        self.subparsers["OrderedRhsPatternParser"] = (LPAR + self._sb("SymbolParser") + pp.ZeroOrMore(self._sb("RhsFieldParser")) + RPAR)\
                .setParseAction(makeInstance(types.OrderedRhsPattern, None))

        self.subparsers["TemplateRhsPatternParser"] = (LPAR + self._sb("SymbolParser") + pp.Group(pp.ZeroOrMore(self._sb("RhsSlotParser"))) + RPAR)\
                .setParseAction(makeInstanceDict(types.TemplateRhsPattern, {'templateName': 0, 
                                                                                  'templateSlots': 1,
                                                                                  "modulesManager": self._modulesManager
                                                                                  }))

        self.subparsers["RhsPatternParser"] = (self._sb("TemplateRhsPatternParser") | self._sb("OrderedRhsPatternParser"))\
                .setParseAction(forwardParsed(key=0))

        self.subparsers["FactDefinitionParser"] = self._sb("RhsPatternParser").copy()
        
        self.subparsers["ArgumentsGroupParser"] = (LPAR + pp.Group( pp.OneOrMore(self._sb("RhsFieldParser")) ) + RPAR)\
                .setParseAction(forwardParsed())
        
        self.subparsers["RhsFunctionCallParser"] << (LPAR + self._sb("FunctionNameParser") 
                                                        + pp.Group(pp.ZeroOrMore(
                                                            self._sb("RhsExpressionParser")
                                                                | self._sb("FactDefinitionParser")
                                                                | self._sb("ArgumentsGroupParser")
                                                        ))
                                                    + RPAR)\
                .setParseAction(makeInstanceDict(types.FunctionCall, {'funcName': 0,
                                                                            'funcArgs': 1,
                                                                            "modulesManager": self._modulesManager
                                                                            }))
                
        # expression alias    
        self.subparsers["ActionParser"] = (self._sb("VariableParser")
                                                | self._sb("ConstantParser")
                                                | self._sb("RhsFunctionCallParser") )\
                .setParseAction(forwardParsed())


        ### DEFFACTS
        
        self.subparsers['DefFactsNameParser'] = self._sb("SymbolParser").copy()\
                .addParseAction(valutateScopeChange(self.getModulesManager()))
        
        self.subparsers["DefFactsConstructParser"] = (LPAR + pp.Keyword("deffacts").suppress() 
                                                        - self._sb("DefFactsNameParser").setResultsName("DefFactsNameParser") 
                                                            - pp.Optional(self._sb("CommentParser")).setName("comment").setResultsName("comment") 
                                                        - pp.Group(pp.OneOrMore(self._sb("RhsPatternParser"))).setName("rhs").setResultsName("rhs")
                                                        - RPAR)\
                .setParseAction(makeInstanceDict(types.DefFactsConstruct, {"deffactsName" : 'DefFactsNameParser', 
                                                                                 "deffactsComment" : "comment", 
                                                                                 "rhs" : "rhs",
                                                                                 "modulesManager": self._modulesManager
                                                                                 }))


        ### DEFRULE
        
        self.subparsers['RulePropertyParser'] = (LPAR + 
                                                 ( 
                                                     (pp.Keyword('salience') + self._sb("IntegerParser")) |
                                                     (pp.Keyword('auto-focus') + self._sb("SymbolParser")) #|
                                                     #(pp.Keyword('specificity') + self._sb("IntegerParser")) #|
                                                     #(self._sb("SymbolParser") + self._sb("SymbolParser")) 
                                                 ) +
                                                RPAR)\
                .setParseAction(makeInstanceDict(types.RuleProperty, {"propertyName" : 0, "propertyValue" : 1}))
        
        self.subparsers['DeclarationParser'] = (LPAR + pp.Keyword("declare").suppress() +
                                                    pp.Group(pp.OneOrMore(self._sb("RulePropertyParser") )) +
                                                RPAR)\
                .setParseAction(forwardParsed(key=0))
        
        
        self.subparsers['UnnamedSingleFieldVariableParser'] = pp.Keyword("?")\
                .setParseAction(makeInstance(types.UnnamedSingleFieldVariable))
                
        self.subparsers['UnnamedMultiFieldVariableParser'] = pp.Keyword("$?")\
                .setParseAction(makeInstance(types.UnnamedMultiFieldVariable))
        
        self.subparsers['TermParser'] = (                                         
                                         (
                                            ((pp.Literal(':') | pp.Literal('=')) - self._sb("FunctionCallParser"))\
                                                .setParseAction(forwardParsed(key=1))
                                            )
                                         | self._sb("SingleFieldVariableParser")
                                         | self._sb("MultiFieldVariableParser") 
                                         | self._sb("ConstantParser")
                                        )\
                .setParseAction(forwardParsed(key=0))
        
        self.subparsers['SingleConstraintParser'] = (pp.Optional(pp.Literal('~')).setResultsName("not") + 
                                                     self._sb("TermParser").setResultsName("term"))\
                .setParseAction(tryInstance(types.NegativeTerm, types.PositiveTerm, {"term" : "term", 
                                                                                           "isNot" : 'not' 
                                                                                           }))
        
        self.subparsers['ConnectedConstraintParser'] = pp.Forward()
        self.subparsers['ConnectedConstraintParser'] << (self._sb("SingleConstraintParser").setResultsName("constraint") 
                                                            + pp.Optional(
                                                                pp.Group(
                                                                    ( pp.Literal("|") + self._sb("ConnectedConstraintParser")) |
                                                                    ( pp.Literal("&") + self._sb("ConnectedConstraintParser"))
                                                                )
                                                            ).setResultsName("connectedConstraint")\
                                                                .setParseAction(forwardParsed())
                                                         )\
                .setParseAction(tryInstance(types.ConnectedConstraint, types.Constraint, {"constraint" : "constraint", 
                                                                                                "connectedConstraints" : "connectedConstraint" 
                                                                                                }))
        
        self.subparsers['ConstraintParser'] = (self._sb("UnnamedSingleFieldVariableParser")
                                               | self._sb("UnnamedMultiFieldVariableParser") 
                                               | self._sb("ConnectedConstraintParser"))\
                .setParseAction(forwardParsed(key=0))
        
        self.subparsers["SingleFieldLhsSlotParser"] = (LPAR + 
                                                        self._sb("SymbolParser") +
                                                        self._sb("ConstraintParser") +
                                                       RPAR)\
                .setParseAction(makeInstanceDict(types.SingleFieldLhsSlot, {"slotName" : 0, "slotValue" : 1}))
        
        self.subparsers["MultiFieldLhsSlotParser"] = (LPAR + 
                                                        self._sb("SymbolParser") + 
                                                        pp.Group(pp.ZeroOrMore(self._sb("ConstraintParser"))).setResultsName("content") + 
                                                      RPAR )\
                .setParseAction(makeInstanceDict(types.MultiFieldLhsSlot, {"slotName" : 0, "slotValue" : "content"}))
        
        
        self.subparsers['LhsSlotParser'] = (self._sb("SingleFieldLhsSlotParser")
                                            | self._sb("MultiFieldLhsSlotParser"))\
                .setParseAction(forwardParsed(key=0))
        
        self.subparsers['OrderedPatternCEParser'] = (LPAR + pp.Group(self._sb("SymbolParser") + pp.ZeroOrMore(self._sb("ConstraintParser"))) + RPAR)\
                .setParseAction(makeInstanceDict(types.OrderedPatternCE, {"constraints": 0, "modulesManager": self._modulesManager}))

        self.subparsers['TemplatePatternCEParser'] = (LPAR + self._sb("SymbolParser").setResultsName("templateName") + 
                                                        pp.Group(pp.ZeroOrMore(self._sb("LhsSlotParser"))).setResultsName("templateSlots") + 
                                                      RPAR)\
                .setParseAction(makeInstanceDict(types.TemplatePatternCE, {"templateName" : "templateName", 
                                                                                 "templateSlots" : "templateSlots", 
                                                                                 "modulesManager": self._modulesManager
                                                                                 }))
        
        self.subparsers['PatternCEParser'] = (self._sb("OrderedPatternCEParser")
                                              | self._sb("TemplatePatternCEParser"))\
                .setParseAction(forwardParsed(key=0))
                
        self.subparsers['AssignedPatternCEParser'] = (self._sb("SingleFieldVariableParser") 
                                                        - pp.Literal("<-").suppress()
                                                        - self._sb("PatternCEParser")
                                                    )\
                .setParseAction(makeInstanceDict(types.AssignedPatternCE, {"variable": 0, "pattern": 1}))

        # recursive parser in And/Not/Or
        self.subparsers['ConditionalElementParser'] = pp.Forward()

        
        self.subparsers['NotCEParser'] = (LPAR 
                                            + pp.Keyword("not") 
                                            - self._sb("ConditionalElementParser") 
                                            - RPAR)\
                .setParseAction(makeInstance(types.NotPatternCE, 1))

        self.subparsers['AndCEParser'] = (LPAR 
                                            + pp.Keyword("and") 
                                            - pp.Group(pp.OneOrMore(self._sb("ConditionalElementParser"))) 
                                            - RPAR)\
                .setParseAction(makeInstance(types.AndPatternCE, 1))

        self.subparsers['OrCEParser'] = (LPAR 
                                            + pp.Keyword("or") 
                                            - pp.Group(pp.OneOrMore(self._sb("ConditionalElementParser"))) 
                                            - RPAR)\
                .setParseAction(makeInstance(types.OrPatternCE, 1))

        self.subparsers['TestCEParser'] = (LPAR 
                                            + pp.Keyword("test") 
                                            - self._sb("FunctionCallParser") 
                                            - RPAR)\
                .setParseAction(makeInstance(types.TestPatternCE, 1))
        
        self.subparsers['ConditionalElementParser'] << (self._sb("NotCEParser") # not before pattern, or not will be parsed as template name
                                                            | self._sb("AndCEParser") # and before pattern, or and will be parsed as template name
                                                            | self._sb("TestCEParser") # test before pattern, or test will be parsed as template name
                                                            | self._sb("OrCEParser") # or before pattern-ce, or OR will be parsed as template name
                                                            #| self._sb("LogicalCEParser") 
                                                            #| self._sb("ExistsCEParser")
                                                            #| self._sb("ForallCEParser")
                                                            | self._sb("AssignedPatternCEParser") 
                                                            | self._sb("PatternCEParser") 
                                                        )\
                .setParseAction(forwardParsed(key=0))
                
        
        self.subparsers['DefRuleNameParser'] = self._sb("SymbolParser").copy()\
                .addParseAction(valutateScopeChange(self.getModulesManager()))
        
        self.subparsers['DefRuleConstructParser'] = (LPAR + pp.Keyword("defrule").suppress()  
                                                        - self._sb("DefRuleNameParser").setResultsName('rulename')
                                                            - pp.Optional(self._sb("CommentParser")).setName("defruleComment").setResultsName("comment")
                                                            - pp.Optional(self._sb("DeclarationParser")).setName("defruleDeclaration").setResultsName("declaration")
                                                            - pp.Optional(pp.Group(pp.ZeroOrMore(self._sb("ConditionalElementParser")))).setResultsName("lhs")\
                                                                    .setParseAction(forwardParsed())
                                                        - pp.Literal("=>").suppress()
                                                        - pp.Group(pp.ZeroOrMore(self._sb("ActionParser"))).setResultsName("rhs")
                                                     - RPAR)\
                .setParseAction(makeInstanceDict(types.DefRuleConstruct, {"defruleName" : 'rulename', 
                                                                                "defruleComment" : "comment", 
                                                                                "defruleDeclaration" : "declaration", 
                                                                                "lhs" : "lhs", 
                                                                                "rhs" : "rhs",
                                                                                "modulesManager": self._modulesManager
                                                                                }))


        ### DEFTEMPLATE

        self.subparsers["DefaultAttributeParser"] = (LPAR + pp.Keyword("default").suppress()
                                                        - ( pp.Keyword("?DERIVE")
                                                            | pp.Keyword("?NONE")
                                                            | self._sb("ExpressionParser")
                                                           )
                                                     - RPAR)\
                .setParseAction(makeInstance(types.DefaultAttribute, 0))
        
        self.subparsers["TypeSpecificationParser"] = (pp.Group( 
                                                        pp.OneOrMore(
                                                            pp.oneOf( types.TYPES.keys() ))
                                                        )
                                                      )\
                .setParseAction(forwardParsed())
        
        self.subparsers["TypeAttributeParser"] = (LPAR + pp.Keyword("type").suppress()
                                                    - self._sb("TypeSpecificationParser")
                                                    - RPAR)\
                .setParseAction(makeInstance(types.TypeAttribute, 0))                                                  
        
        # Re-enable when other constraints will be implemented
        #self.subparsers["ConstraintAttributeParser"] = self._sb("TypeAttributeParser").copy()\
        #        .setParseAction(forwardParsed(key=0))
        

        self.subparsers["TemplateAttributeParser"] = (self._sb("DefaultAttributeParser")
                                                        #| self._sb("ConstraintAttributeParser")
                                                        | self._sb("TypeAttributeParser")
                                                        )\
                .setParseAction(forwardParsed(key=0))

        self.subparsers["SingleSlotDefinitionParser"] = (LPAR + pp.Keyword("slot").suppress()
                                                            - self._sb("SymbolParser")
                                                            - pp.Group( pp.ZeroOrMore( self._sb("TemplateAttributeParser") ))
                                                         - RPAR)\
                .setParseAction(makeInstanceDict(types.SingleSlotDefinition, {"slotName": 0, "attributes": 1}))

        self.subparsers["MultiSlotDefinitionParser"] = (LPAR + pp.Keyword("multislot").suppress()
                                                            - self._sb("SymbolParser")
                                                            - pp.Group( pp.ZeroOrMore( self._sb("TemplateAttributeParser") ))
                                                         - RPAR)\
                .setParseAction(makeInstanceDict(types.MultiSlotDefinition, {"slotName": 0, "attributes": 1}))
        
        self.subparsers["SlotDefinitionParser"] = ( self._sb("MultiSlotDefinitionParser")
                                                    | self._sb("SingleSlotDefinitionParser")
                                                    )\
                .setParseAction(forwardParsed())


        self.subparsers['DefTemplateNameParser'] = self._sb("SymbolParser").copy()\
                .addParseAction(valutateScopeChange(self.getModulesManager()))
        
        self.subparsers["DefTemplateConstructParser"] = (LPAR + pp.Keyword("deftemplate").suppress()  
                                                        - self._sb("DefTemplateNameParser").setResultsName('templateName')
                                                            - pp.Optional(self._sb("CommentParser")).setName("templateComment").setResultsName("templateComment")
                                                        - pp.Group(pp.ZeroOrMore(self._sb("SlotDefinitionParser"))).setResultsName("slots")
                                                        - RPAR)\
                .setParseAction(makeInstanceDict(types.DefTemplateConstruct, {"templateName" : 'templateName',
                                                                                    "templateComment" : "templateComment", 
                                                                                    "slots" : "slots", 
                                                                                    "modulesManager": self._modulesManager
                                                                                    })) 
        
        
        ### DEFGLOBAL
        
        self.subparsers["GlobalAssignmentParser"] = (self._sb("GlobalVariableParser").copy()
                                                        .setParseAction(makeInstanceDict(types.GlobalVariable, {'content': 1, 
                                                                                                                "modulesManager": self._modulesManager,
                                                                                                                "ignoreCheck": True
                                                                                                                }))
                                                     + pp.Literal("=").suppress()
                                                     + self._sb("ExpressionParser"))\
                .setParseAction(makeInstanceDict(types.GlobalAssignment, {"variable": 0,
                                                                          "value": 1}))
                
        self.subparsers['DefGlobalModuleParser'] = self._sb("SymbolParser").copy()\
                .addParseAction(doScopeChange(self.getModulesManager()))
        
        self.subparsers["DefGlobalConstructParser"] = (LPAR + pp.Keyword("defglobal").suppress()
                                                            - pp.Optional(self._sb("DefGlobalModuleParser")).setResultsName("moduleName")
                                                        - pp.Group(pp.ZeroOrMore(self._sb("GlobalAssignmentParser"))).setResultsName("assignments")
                                                        - RPAR)\
                .setParseAction(makeInstanceDict(types.DefGlobalConstruct, {"assignments": "assignments", 
                                                                            "moduleName": "moduleName", 
                                                                            "modulesManager": self._modulesManager
                                                                            }))
        
        
        ### DEFMODULE
        
        self.subparsers["PortConstructParser"] = pp.oneOf(["deftemplate", "defglobal", "deffunction"])\
                .setParseAction(makeInstance(types.Symbol))
        
        self.subparsers["PortItemParser"] = (pp.Keyword("?ALL")
                                                | pp.Keyword("?NONE")
                                                | pp.Group(
                                                        self._sb("PortConstructParser")
                                                        - ( pp.Keyword("?ALL")
                                                            | pp.Keyword("?NONE")
                                                            |  pp.Group(pp.OneOrMore(self._sb("SymbolParser"))))
                                                    )
                                             )\
                .setParseAction(makeInstance(types.PortItem, position=0))
        

        self.subparsers["PortSpecificationImportParser"] = (LPAR + pp.Keyword("import").suppress()
                                                            - self._sb("SymbolParser")
                                                            - self._sb("PortItemParser")
                                                            - RPAR)\
                .setParseAction(makeInstanceDict(types.ImportSpecification, {"moduleName": 0,
                                                                             "item": 1,
                                                                             "modulesManager": self._modulesManager
                                                                             }))
        
        self.subparsers["PortSpecificationExportParser"] = (LPAR + pp.Keyword("export").suppress()
                                                            - self._sb("PortItemParser")
                                                            - RPAR)\
                .setParseAction(makeInstance(types.ExportSpecification, position=0))
        
        self.subparsers["PortSpecificationParser"] = (self._sb("PortSpecificationImportParser")
                                                        | self._sb("PortSpecificationExportParser"))\
                .setParseAction(forwardParsed(key=0))

        self.subparsers["DefModuleConstructParser"] = (LPAR + pp.Keyword("defmodule").suppress()
                                                        - self._sb("SymbolParser").setResultsName("moduleName")
                                                            - pp.Optional(self._sb("CommentParser")).setResultsName("comment")
                                                        - pp.Group(pp.ZeroOrMore(self._sb("PortSpecificationParser"))).setResultsName("specifications")
                                                        - RPAR)\
                .setParseAction(makeInstanceDict(types.DefModuleConstruct, {"specifications": "specifications",
                                                                            "comment": "comment",
                                                                            "moduleName": "moduleName", 
                                                                            "modulesManager": self._modulesManager
                                                                            }))
        
        ### DEFFUNCTION
        
        self.subparsers['DefFunctionNameParser'] = self._sb("SymbolParser").copy()\
                .addParseAction(valutateScopeChange(self.getModulesManager()))
        
        self.subparsers["DefFunctionConstructParser"] = (LPAR + pp.Keyword("deffunction").suppress()  
                                                        - self._sb("DefFunctionNameParser").setResultsName('functionName')
                                                            - pp.Optional(self._sb("CommentParser")).setResultsName("comment")
                                                        - LPAR
                                                            - pp.Group( pp.ZeroOrMore(self._sb("SingleFieldVariableParser"))
                                                                - pp.Optional(self._sb("MultiFieldVariableParser"))
                                                                ).setResultsName("params")
                                                        - RPAR
                                                        - pp.Group(pp.ZeroOrMore(self._sb("ActionParser"))).setResultsName("actions")
                                                        - RPAR)\
                .setParseAction(makeInstanceDict(types.DefFunctionConstruct, {"functionName" : 'functionName',
                                                                              "comment" : "comment",
                                                                              "params" : "params", 
                                                                              "actions" : "actions", 
                                                                              "modulesManager": self._modulesManager
                                                                            }))        
                
        
        ### HIGH-LEVEL PARSERS
        
        ### COMMENTS & DIRECTIVE
        
        # small speed parsing improvements disabiling directive
        if self._enableDirectives:
            self.subparsers["MyClipsDirectiveParser"] = pp.Regex(r'\;\@(?P<command>\w+)\((?P<params>.+?)\)')\
                    .setName("MyClipsDirectiveParser").suppress()
                    #.setParseAction(lambda s,l,t: ('myclips-directive', (t['command'], t['params'])))
                

            self.subparsers["ConstructParser"] = ( self._sb("DefFactsConstructParser") 
                                                    | self._sb("DefGlobalConstructParser")
                                                    | self._sb("DefRuleConstructParser")
                                                    | self._sb("DefTemplateConstructParser")
                                                    | self._sb("DefFunctionConstructParser")
                                                    | self._sb("DefModuleConstructParser")
                                                    | self._sb("MyClipsDirectiveParser")
                                                    | pp.CharsNotIn(")") - ~pp.Word(pp.printables).setName("<unknown>")
                                                    )
        else:
            self.subparsers["ConstructParser"] = ( self._sb("DefFactsConstructParser") 
                                                    | self._sb("DefGlobalConstructParser")
                                                    | self._sb("DefRuleConstructParser")
                                                    | self._sb("DefTemplateConstructParser")
                                                    | self._sb("DefFunctionConstructParser")
                                                    | self._sb("DefModuleConstructParser")
                                                    | pp.CharsNotIn(")") - ~pp.Word(pp.printables).setName("<unknown>")
                                                    )
            
        self.subparsers["ConstructParser"]\
                .setParseAction(forwardParsed(key=0))
                #.setDebug(self._debug)

        # if file/string doesn't contain comments
        # 1/3 faster parsing can be archived
        # setting containsComments = False
        if self._enableComments:
            self.subparsers["ClipsCommentParser"] = (
                        #pp.Regex(r'\;^\@.*?\n')
                        ( ";" + pp.NotAny('@') + pp.SkipTo("\n") ).setName("ClipsComment")
                        )
            self.subparsers["ConstructParser"].ignore(self._sb("ClipsCommentParser"))#\
                  
        
        self.subparsers["CLIPSProgramParser"] = pp.OneOrMore( self.getSParser("ConstructParser") )\
                .setParseAction(forwardParsed())

        for k in self.subparsers.keys():
            self.subparsers[k].setName(k).setDebug(self._debug)

    def getModulesManager(self):
        return self._modulesManager
            
    def getSParser(self, name):
        self._initParsers()
        return self.subparsers[name]

    # shortcut
    _sb = getSParser
    
    def parse(self, text, filterReturn=False):
        try:
            return [x for x 
                        in self.getSParser('CLIPSProgramParser').parseString(text, True).asList() 
                            if not isinstance(x, (str, unicode)) # always filter simple strings
                                # filter functions/templates/modules constructs (they are loaded in the MM)
                                and (( filterReturn and isinstance(x, (types.DefFactsConstruct, types.DefRuleConstruct)))
                                     or not filterReturn )] 
                        
        except pp.ParseBaseException, e:
            if self._lastParseError != None and e.msg != self._lastParseError:
                raise pp.ParseFatalException(e.pstr,
                                             e.loc,
                                             e.msg + ". Possible cause: " + self._lastParseError )
            else:
                raise
            
    
    def _changeDebug(self):
        for p in self.subparsers:
            p.setDebug(self._debug)
            
    @staticmethod
    def ExceptionPPrint(err, original_string, prev_lines=10, after_lines=5, customMsg=False, returnArray=False):
        try:
            if err.loc == 0:
                raise Exception()
            
            splitted = original_string.splitlines()
            lines_padding = len(str(len(splitted))) + 1
            format_string = "% " + str(lines_padding) + "d| %s"
            rVal = [err.__class__.__name__]
            rVal += [format_string%(i+1+max(0,err.lineno-prev_lines),x) for (i,x) in enumerate(splitted[max(0,err.lineno-prev_lines):err.lineno-1])]
            rVal.append(format_string%(err.lineno,err.line))
            rVal.append(" "*(err.column+lines_padding+1) + "^")
            if customMsg == False: 
                rVal.append(str(err))
            else:
                rVal.append(str(customMsg))
            rVal.append("")
            rVal += [format_string%(i+1+err.lineno,x) for (i,x) in enumerate(splitted[err.lineno:err.lineno+after_lines])]
            
            if not returnArray:
                rVal = "\n".join(rVal)
            
            return rVal
        except:
            # if an error is found (for example if no lineno attr available in err
            rVal = ["*** No error location available ***", str(err)]
            
            if not returnArray:
                rVal = "\n".join(rVal)
            
            return rVal
if __name__ == '__main__':



    complete_test = r"""
        (defrule rulename
            (A B C)
            (D ~E F)
            (G ?h&:(neq ?h t)|:(eq ?h t) I)
            (template
                (s1 v1) 
                (s2 v2)
            )
            (template2 
                (s1 ?var&:(neq s t)) 
                (s2 1 2 3) 
                (s3 $?ciao) 
                (s4 $?) 
                (s5 ?)
            )
            => 
        )
    """
    _complete_test = complete_test
    for i in range(1,500):
        _complete_test += complete_test

    
    parser = Parser(debug=False)
    
    parser.parse(r"""
    (deftemplate template (slot s1) (slot s2))
    (deftemplate template2 (slot s1) (multislot s2) (multislot s3) (multislot s4) (slot s5))
    """)
    
    

    complete_P = pp.OneOrMore(
                    parser.getSParser("ConstructParser").setDebug(False)
                )
    
    #complete_P.enablePackrat()
        

    start_time = time.time()
    res = complete_P.parseString(_complete_test)#.asList()
    print time.time() - start_time, " seconds"
    
    #pprint.pprint(res)
    
#    start_time = time.time()
#    #res = []
#    for i in range(0,500):
#        #res += 
#        complete_P.parseString(complete_test)#.asList()
#    print time.time() - start_time, " seconds"
#    
    
    