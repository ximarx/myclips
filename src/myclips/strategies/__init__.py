

STRATEGIES = {
    'depth': 'myclips.strategies.Depth.Depth',
    'breadth': 'myclips.strategies.Breadth.Breadth',
    'lex': 'myclips.strategies.Lex.Lex',
    'mea': 'myclips.strategies.Mea.Mea',
    'complexity': 'myclips.strategies.Complexity.Complexity',
    'semplicity': 'myclips.strategies.Semplicity.Semplicity',
    'random': 'myclips.strategies.Random.Random'
}

class factory(object):
    DEFAULT_STRATEGY_CLASSNAME = "depth"
    @classmethod
    def newInstance(cls, strategyName=None):
        strategyName = strategyName if strategyName is not None and STRATEGIES.has_key(strategyName) else cls.DEFAULT_STRATEGY_CLASSNAME
        strategyName = STRATEGIES[strategyName]
        import myclips
        return myclips.newInstance_fromCanonicalClassname(strategyName)

def isValid(strategyName):
    return STRATEGIES.has_key(strategyName)

class Strategy(object):
    
    def __init__(self, *args, **kwargs):
        object.__init__(self, *args, **kwargs)
        
    def insert(self, perSalienceContainer, thePNode, theToken):
        raise NotImplementedError()
    
    def resort(self, perSalienceContainer, theOldStrategy):
        raise NotImplementedError()
    
    def remove(self, perSalienceContainer, thePNode, theToken):
        raise NotImplementedError()
    
    def iterable(self, perSalienceContainer):
        raise NotImplementedError()
    
    def pop(self, perSalienceContainer):
        raise NotImplementedError()
    
    def newContainer(self):
        return []