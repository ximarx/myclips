

class factory(object):
    DEFAULT_STRATEGY_NAME = "depth"
    
    STRATEGIES = {
        'depth': 'myclips.strategies.Depth.Depth',
        'breadth': 'myclips.strategies.Breadth.Breadth',
        'lex': 'myclips.strategies.Lex.Lex',
        'mea': 'myclips.strategies.Mea.Mea',
        'complexity': 'myclips.strategies.Complexity.Complexity',
        'semplicity': 'myclips.strategies.Semplicity.Semplicity',
        'random': 'myclips.strategies.Random.Random'
    }
    
    @classmethod
    def newInstance(cls, strategyName=None):
        strategyName = strategyName if strategyName is not None and cls.isValid(strategyName) else cls.DEFAULT_STRATEGY_NAME
        strategyName = cls.STRATEGIES[strategyName]
        import myclips
        return myclips.newInstance_fromCanonicalClassname(strategyName)

    @classmethod
    def isValid(cls, strategyName):
        return cls.STRATEGIES.has_key(strategyName)

class Strategy(object):
    
    NAME = ""
    
    @classmethod
    def getName(cls):
        return cls.NAME
        
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