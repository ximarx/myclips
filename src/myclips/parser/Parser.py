
import pyparsing as pp
import string
import myclips.parser.types as types
from memoized import memoized

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

class Parser(object):
    
    def __init__(self, debug=False, funcNames=None):
        
        self.subparsers = {}
        self._initied = False
        self._debug = debug
        self._funcNames = funcNames if funcNames != None else []
        
    def isInitied(self):
        return self._initied
    
    def setDebug(self, status):
        if self._debug != status:
            self._debug = status
            if self._initied:
                self._changeDebug()
                
    def setFuncNames(self, funcNames):
        if self._initied:
            return False
        else:
            self._funcNames = funcNames
            return True
    
    def _initParsers(self):
        
        if self._initied:
            return
        
        self._initied = True


        ### BASE PARSERS
        
        LPAR = pp.Literal("(").suppress()
        RPAR = pp.Literal(")").suppress()
        
        self.subparsers["SymbolParser"] = pp.Word("".join([ c for c in string.printable if c not in string.whitespace and c not in "\"'()&?|<~;" ]))\
                .setParseAction(types.makeInstance(types.Symbol))
        
        self.subparsers["StringParser"] = pp.QuotedString('"', '\\', None, True, True)\
                .setParseAction(types.makeInstance(types.String))
        # StringParser alias    
        self.subparsers["CommentParser"] = self.subparsers["StringParser"]
        
        self.subparsers["IntegerParser"] = pp.Combine(pp.Optional(pp.oneOf('+ -')) + pp.Word(pp.nums))\
                .setParseAction(types.makeInstance(types.Integer))
        
        # try to cast to Integer first, otherwise Float
        self.subparsers["FloatParser"] = pp.Regex(r'[+-]?\d+(\.\d*)?([eE]-?\d+)?')\
                .setParseAction(types.tryInstance(types.Integer, types.Float))
                    
        self.subparsers["VariableSymbolParser"] = pp.Word(string.letters, "".join([ c for c in string.printable if c not in string.whitespace and c not in "\"'()&?|<~;" ]))\
                .setParseAction(types.makeInstance(types.Symbol))    
                         
        self.subparsers["NumberParser"] = (self.getSParser("FloatParser") ^ self.getSParser("IntegerParser"))\
                .setParseAction(forwardParsed())
        
        self.subparsers["LexemeParser"] = (self.getSParser("StringParser") ^ self.getSParser("SymbolParser"))\
                .setParseAction(forwardParsed())
        
        self.subparsers["ConstantParser"] = (self.getSParser("NumberParser") ^ self.getSParser("LexemeParser"))\
                .setParseAction(forwardParsed())
        
        self.subparsers["SingleFieldVariableParser"] = (pp.Literal("?") + self.getSParser("VariableSymbolParser"))\
                .setParseAction(types.makeInstance(types.SingleFieldVariable, 1))
        
        self.subparsers["MultiFieldVariableParser"] = (pp.Literal("$?") + self.getSParser("VariableSymbolParser"))\
                .setParseAction(types.makeInstance(types.MultiFieldVariable, 1))
            
        self.subparsers["GlobalVariableParser"] = (pp.Literal("?*") + self.getSParser("VariableSymbolParser"))\
                .setParseAction(types.makeInstance(types.GlobalVariable, 1))
        
        self.subparsers["VariableParser"] = (self.getSParser("MultiFieldVariableParser") | self.getSParser("GlobalVariableParser") | self.getSParser("SingleFieldVariableParser"))\
                .setParseAction(forwardParsed(key=0))
        
        ### CONSTRUCTS PARSERS        
        
        self.subparsers["ExpressionParser"] = pp.Forward()
        
        self.subparsers["FunctionCallParser"] = (LPAR + self.getSParser("VariableSymbolParser") + pp.Group(pp.ZeroOrMore(self.getSParser("ExpressionParser"))) + RPAR)\
                .setParseAction(types.makeInstanceDict(types.FunctionCall, {'funcName': 0, 'funcArgs': 1}))
        
        self.subparsers["ExpressionParser"] << (self.getSParser("ConstantParser") ^ self.getSParser("VariableParser") ^ self.getSParser("FunctionCallParser") )\
                .setParseAction(forwardParsed())
                
        # expression alias    
        self.subparsers["ActionParser"] = self.subparsers["ExpressionParser"]

        self.subparsers["RhsFieldParser"] = self.subparsers["ExpressionParser"]

        self.subparsers["MultiFieldRhsSlotParser"] = (LPAR + self._sb("SymbolParser") + pp.Group(pp.ZeroOrMore(self._sb("RhsFieldParser"))).setResultsName("content") + RPAR )\
                .setParseAction(types.makeInstanceDict(types.MultiFieldRhsSlot, {"slotName" : 0, "slotValue" : "content"}))

        self.subparsers["SingleFieldRhsSlotParser"] = (LPAR + self._sb("SymbolParser") + self._sb("RhsFieldParser") + RPAR )\
                .setParseAction(types.makeInstanceDict(types.SingleFieldRhsSlot, {"slotName" : 0, "slotValue" : 1}))
        
        self.subparsers["RhsSlotParser"] = (self._sb('SingleFieldRhsSlotParser') ^ self._sb("MultiFieldRhsSlotParser"))\
                .setParseAction(forwardParsed(key=0))
        
        self.subparsers["OrderedRhsPatternParser"] = (LPAR + self._sb("SymbolParser") + pp.ZeroOrMore(self._sb("RhsFieldParser")) + RPAR)\
                .setParseAction(types.makeInstance(types.OrderedRhsPattern, None))

        self.subparsers["TemplateRhsPatternParser"] = (LPAR + self._sb("SymbolParser") + pp.Group(pp.ZeroOrMore(self._sb("RhsSlotParser"))) + RPAR)\
                .setParseAction(types.makeInstanceDict(types.TemplateRhsPattern, {'templateName': 0, 'templateSlots': 1}))

        self.subparsers["RhsPatternParser"] = (self._sb("TemplateRhsPatternParser") ^ self._sb("OrderedRhsPatternParser"))\
                .setParseAction(forwardParsed(key=0))

        

        ### DEFFACTS
        
        self.subparsers['DefFactsNameParser'] = self._sb("SymbolParser")        
        
        self.subparsers["DefFactsConstructParser"] = (LPAR + pp.Keyword("deffacts").suppress() + self._sb("DefFactsNameParser").setResultsName("DefFactsNameParser") + 
                                                        pp.Optional(self._sb("CommentParser")).setName("comment").setResultsName("comment") + 
                                                        pp.Group(pp.OneOrMore(self._sb("RhsPatternParser"))).setName("rhs").setResultsName("rhs") + RPAR)\
                .setParseAction(types.makeInstanceDict(types.DefFactsConstruct, {"deffactsName" : 'DefFactsNameParser', "deffactsComment" : "comment", "rhs" : "rhs"}))

        
        ### HIGH-LEVEL PARSERS

        self.subparsers["ConstructParser"] = (self._sb("DefFactsConstructParser") 
                                                #| self._sb("DefTemplateConstructParser")
                                                #| self._sb("DefGlobalContructParser")
                                                #| self._sb("DefRuleConstructParser")
                                                #| self._sb("DefFunctionConstructParser")
                                                #| self._sb("DefModuleConstructParser")
                                                )#\
                #.setParseAction(forwardParsed())\
                #.setDebug(self._debug)
                  
        
        self.subparsers["CLIPSProgramParser"] = pp.OneOrMore( self.getSParser("ConstructParser") )

        for k in self.subparsers.keys():
            self.subparsers[k].setName(k).setDebug(self._debug)
        
            
    def getSParser(self, name):
        self._initParsers()
        return self.subparsers[name]

    # shortcut
    _sb = getSParser
    
    def _changeDebug(self):
        for p in self.subparsers:
            p.setDebug(self._debug)
    
if __name__ == '__main__':


    import pprint
    # definizioni di base

    
#    tests = [
#             (SymbolParser, "wefoijefwoijefoi", 0),
#             (StringParser, '"ciao"', 0),
#             (IntegerParser, "1", 0),
#             (IntegerParser, "213121", 0),
#             (IntegerParser, "+132211", 0),
#             (IntegerParser, "-1123123", 0),
#             (FloatParser, "-1123123", 0),
#             (FloatParser, "+1123123", 0),
#             (FloatParser, "-112.3123", 0),
#             (FloatParser, "-1.45e-10", 0),
#             ]
#    
#    for (PARSER, STR, POS) in tests:
#        print "Parsing {0} with {1}".format(STR, repr(PARSER.func))
#        res = PARSER().parseString(STR)           
#        print "\tResult: ", res.asList()
#        print "\tContent[{0}] (RAW): ".format(POS), res[POS].content
#        print "\tType[{0}] (RAW): ".format(POS), res[POS].content.__class__
#        print "\tContent[{0}]: ".format(POS), res[POS].evaluate()
#        print "\tType[{0}]: ".format(POS), res[POS].evaluate().__class__
#        print


    complete_test = r"""
    (deffacts nome1 "commento"
        (1 2 3)
        (coap coapw qw)
    )
    ( deffacts nome2
        (2321 1)
    )
    """

    parser = Parser(debug=True)

    #parser.getSParser("VariableSymbolParser").setDebug(True)
    #parser.getSParser("SingleFieldVariableParser").setDebug(True)

    complete_P = pp.OneOrMore(
                    parser.getSParser("DefFactsConstructParser").setDebug(True)
                )


    res = complete_P.parseString(complete_test).asList()
    pprint.pprint(res)
    
    
    