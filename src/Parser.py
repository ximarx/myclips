
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
    
    def __init__(self, debug=False):
        
        self.subparsers = {}
        self._initied = False
        self._debug = debug
    
    def setDebug(self, status):
        if self._debug != status:
            self._debug = status
            if self._initied:
                self._changeDebug()
    
    def _initParsers(self):
        
        if self._initied:
            return
        
        self._initied = True
        
        self.subparsers["SymbolParser"] = pp.Word("".join([ c for c in string.printable if c not in string.whitespace and c not in "\"'()&?|<~;" ]))\
                .setParseAction(types.makeInstance(types.Symbol))\
                .setDebug(self._debug)
        
        self.subparsers["StringParser"] = pp.QuotedString('"', '\\', None, True, True)\
                .setParseAction(types.makeInstance(types.String))\
                .setDebug(self._debug)
        # StringParser alias    
        self.subparsers["CommentParser"] = self.subparsers["StringParser"]
        
        self.subparsers["IntegerParser"] = pp.Combine(pp.Optional(pp.oneOf('+ -')) + pp.Word(pp.nums))\
                .setParseAction(types.makeInstance(types.Integer))\
                .setDebug(self._debug)
        
        # try to cast to Integer first, otherwise Float
        self.subparsers["FloatParser"] = pp.Regex(r'[+-]?\d+(\.\d*)?([eE]-?\d+)?')\
                .setParseAction(types.tryInstance(types.Integer, types.Float))\
                .setDebug(self._debug)
                    
        self.subparsers["VariableSymbolParser"] = pp.Word(string.letters, "".join([ c for c in string.printable if c not in string.whitespace and c not in "\"'()&?|<~;" ]))\
                .setParseAction(types.makeInstance(types.Symbol))\
                .setDebug(self._debug)    
                         
        self.subparsers["NumberParser"] = (self.getSParser("FloatParser") ^ self.getSParser("IntegerParser"))\
                .setParseAction(forwardParsed())\
                .setDebug(self._debug)
        
        self.subparsers["LexemeParser"] = (self.getSParser("StringParser") ^ self.getSParser("SymbolParser"))\
                .setParseAction(forwardParsed())\
                .setDebug(self._debug)
        
        self.subparsers["ConstantParser"] = (self.getSParser("LexemeParser") ^ self.getSParser("NumberParser"))\
                .setParseAction(forwardParsed())\
                .setDebug(self._debug)
        
        self.subparsers["SingleFieldVariableParser"] = (pp.Literal("?") + self.getSParser("VariableSymbolParser"))\
                .setParseAction(types.makeInstance(types.SingleFieldVariable, 1))\
                .setDebug(self._debug)
        
        self.subparsers["MultiFieldVariableParser"] = (pp.Literal("$?") + self.getSParser("VariableSymbolParser"))\
                .setParseAction(types.makeInstance(types.MultiFieldVariable, 1))\
                .setDebug(self._debug)
            
        self.subparsers["GlobalVariableParser"] = (pp.Literal("?*") + self.getSParser("VariableSymbolParser"))\
                .setParseAction(types.makeInstance(types.GlobalVariable, 1))\
                .setDebug(self._debug)
        
        self.subparsers["VariableParser"] = (self.getSParser("MultiFieldVariableParser") | self.getSParser("GlobalVariableParser") | self.getSParser("SingleFieldVariableParser"))\
                .setParseAction(forwardParsed(key=0))\
                .setDebug(self._debug)
        
        self.subparsers["ExpressionParser"] = pp.Forward()
        
        self.subparsers["FunctionCallParser"] = (pp.Literal("(").suppress() + self.getSParser("VariableSymbolParser") + pp.Group(pp.ZeroOrMore(self.getSParser("ExpressionParser"))) + pp.Literal(")").suppress())\
                .setParseAction(types.makeInstanceDict(types.FunctionCall, {'funcName': 0, 'funcArgs': 1}))\
                .setDebug(self._debug)
        
        self.subparsers["ExpressionParser"] << (self.getSParser("ConstantParser") ^ self.getSParser("VariableParser") ^ self.getSParser("FunctionCallParser") )\
                .setParseAction(forwardParsed()).setDebug()\
                .setDebug(self._debug)
            
            
    def getSParser(self, name):
        self._initParsers()
        return self.subparsers[name]
    
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
    (sum ?uno due)
    (bla)
    (?due)
    """

    parser = Parser(debug=False)

    #parser.getSParser("VariableSymbolParser").setDebug(True)
    #parser.getSParser("SingleFieldVariableParser").setDebug(True)

    complete_P = pp.ZeroOrMore(
                              parser.getSParser("FunctionCallParser")#.setDebug(True)
                            )


    res = complete_P.parseString(complete_test).asList()
    pprint.pprint(res)
    
    
    