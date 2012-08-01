

class default(object):
    DEFAULT_STRATEGY_CLASSNAME = "myclips.strategies.Depth.Depth"
    @classmethod
    def newInstance(cls):
        import myclips
        return myclips.newInstance_fromCanonicalClassname(cls.DEFAULT_STRATEGY_CLASSNAME)
