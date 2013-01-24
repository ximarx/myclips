'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType, Constraint_MinArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function

class Unwatch(Function):
    '''
    This function disables the effect of the watch command.
    
    (unwatch (all|network|facts|activations|rules|focus|actions|strategy|statistics)*)
    
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-13.2.html#Heading418
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, *args, **kargs):
        """
        function handler implementation
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-13.2.html#Heading418
        """
        
        if len(args):
            args = dict([(x, True) for x in self.resolve(theEnv, 
                                                         self.semplify(theEnv, args))])
            
            if args.has_key("all") or args.has_key("network"):
                try:
                    theEnv.network.settings.delSetting("_funcs.Watch.network").uninstall()
                except:
                    pass

            if args.has_key("all") or args.has_key("facts"):
                try:
                    theEnv.network.settings.delSetting("_funcs.Watch.facts").uninstall()
                except:
                    pass

            if args.has_key("all") or args.has_key("rules"):
                try:
                    theEnv.network.settings.delSetting("_funcs.Watch.rules").uninstall()
                except:
                    pass

            if args.has_key("all") or args.has_key("activations"):
                try:
                    theEnv.network.settings.delSetting("_funcs.Watch.activations").uninstall()
                except:
                    pass

            if args.has_key("all") or args.has_key("focus"):
                try:
                    theEnv.network.settings.delSetting("_funcs.Watch.focus").uninstall()
                except:
                    pass

            if args.has_key("all") or args.has_key("actions"):
                try:
                    theEnv.network.settings.delSetting("_funcs.Watch.actions").uninstall()
                except:
                    pass
                
            if args.has_key("all") or args.has_key("strategy"):
                try:
                    theEnv.network.settings.delSetting("_funcs.Watch.strategy").uninstall()
                except:
                    pass

            if args.has_key("all") or args.has_key("statistics"):
                try:
                    theEnv.network.settings.delSetting("_funcs.Watch.statistics").uninstall()
                except:
                    pass
        
        return types.NullValue()
    
    
Unwatch.DEFINITION = FunctionDefinition("?SYSTEM?", "unwatch", Unwatch(), types.NullValue, Unwatch.do ,
            [
                Constraint_MinArgsLength(1),
                Constraint_ArgType(types.Lexeme, (None,None), failIfMissing=False)
            ],forward=False)
        
        