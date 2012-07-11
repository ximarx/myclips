

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
                                        repr([repr(x) for x in self.funcArgs] ))

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
                    targs[k] = t[v]
        return cls(**targs)
        
    return makeDictAction

def tryInstance(cls1, cls2, position=0):
    def tryMakeAction(s,l,t):
        try:
            return makeInstance(cls1, position)(s,l,t)
        except:
            return makeInstance(cls2, position)(s,l,t)
            
    return tryMakeAction
    
