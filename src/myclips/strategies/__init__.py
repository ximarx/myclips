

class factory(object):
    DEFAULT_STRATEGY_NAME = "depth"
    
    STRATEGIES = {
        'depth': 'myclips.strategies.Depth.Depth',
        'breadth': 'myclips.strategies.Breadth.Breadth',
        'lex': 'myclips.strategies.Lex.Lex',
        'mea': 'myclips.strategies.Mea.Mea',
        'complexity': 'myclips.strategies.Complexity.Complexity',
        'simplicity': 'myclips.strategies.Simplicity.Simplicity',
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
    '''
    Base class for all valid CRS Strategies
    '''
    
    NAME = ""
    '''strategy id'''
    
    @classmethod
    def getName(cls):
        '''
        Get the name of the strategy
        '''
        return cls.NAME
        
    def insert(self, perSalienceContainer, thePNode, theToken):
        '''
        Add a new activation (pnode, token) in a container
        @param perSalienceContainer: the container
        @type perSalienceContainer: the same time of Strategy.newContainer
        @param thePNode: the Pnode
        @type thePNode: l{myclips.rete.nodes.PNode.PNode}
        @param theToken: the token
        @type theToken: Token
        '''
        raise NotImplementedError()
    
    def resort(self, perSalienceContainer, theOldStrategy):
        '''
        resort activation in the container. Can check oldstrategy
        to setup special resort procedure for known strategies
        (ex simplicity = reverse complexity)
        @param perSalienceContainer: the iterable container
        @type perSalienceContainer: iterable
        @param theOldStrategy: the old strategy
        @type theOldStrategy: Strategy
        '''
        raise NotImplementedError()
    
    def remove(self, perSalienceContainer, thePNode, theToken):
        '''
        Remove an activation from the container
        @param perSalienceContainer: the container
        @type perSalienceContainer: object
        @param thePNode: the pnode
        @type thePNode: PNode
        @param theToken: the token
        @type theToken: Token
        '''
        raise NotImplementedError()
    
    def iterable(self, perSalienceContainer):
        '''
        Convert the special container into a
        basic iterable type
        @param perSalienceContainer: the container
        @type perSalienceContainer: object
        @rtype: iterable
        '''
        raise NotImplementedError()
    
    def pop(self, perSalienceContainer):
        '''
        Get top priority activation and remove it from
        the container
        @param perSalienceContainer: the container
        @type perSalienceContainer: object
        '''
        raise NotImplementedError()
    
    def newContainer(self):
        '''
        Setup the new container for this strategy
        '''
        return []