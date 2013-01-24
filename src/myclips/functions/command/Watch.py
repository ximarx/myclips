'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ExactArgsLength,\
    Constraint_ArgType, Constraint_MinArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function
from myclips.listeners.NetworkBuildPrinter import NetworkBuildPrinter
from myclips.listeners.FactsWatcher import FactsWatcher
from myclips.listeners.RulesWatcher import RulesWatcher
from myclips.listeners.FocusWatcher import FocusWatcher
from myclips.listeners.ActivationsWatcher import ActivationsWatcher
from myclips.listeners.ActionsWatcher import ActionsWatcher
from myclips.listeners.StrategyWatcher import StrategyWatcher
from myclips.listeners.StatisticsWatcher import StatisticsWatcher

class Watch(Function):
    '''
    This function causes messages to be displayed when certain MyCLIPS operations take place
    
    (watch all|network|facts|activations|rules|focus|actions|strategy|statistics*)
    
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-13.2.html#Heading417
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, *args, **kargs):
        """
        function handler implementation
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-13.2.html#Heading417
        """
        
        if len(args):
            args = dict([(x, True) for x in self.resolve(theEnv, 
                                                         self.semplify(theEnv, args))])
            
            if args.has_key("all") or args.has_key("network"):
                try:
                    theEnv.network.settings.getSetting("_funcs.Watch.network")
                except KeyError:
                    theEnv.network.settings.setSetting("_funcs.Watch.network", 
                                                       NetworkBuildPrinter(theEnv.RESOURCES['wtrace']).install(theEnv.network.eventsManager))

            if args.has_key("all") or args.has_key("facts"):
                try:
                    theEnv.network.settings.getSetting("_funcs.Watch.facts")
                except KeyError:
                    theEnv.network.settings.setSetting("_funcs.Watch.facts", 
                                                       FactsWatcher(theEnv.RESOURCES['wtrace']).install(theEnv.network.eventsManager))

            if args.has_key("all") or args.has_key("rules"):
                try:
                    theEnv.network.settings.getSetting("_funcs.Watch.rules")
                except KeyError:
                    theEnv.network.settings.setSetting("_funcs.Watch.rules", 
                                                       RulesWatcher(theEnv.RESOURCES['wtrace']).install(theEnv.network.eventsManager))

            if args.has_key("all") or args.has_key("activations"):
                try:
                    theEnv.network.settings.getSetting("_funcs.Watch.activations")
                except KeyError:
                    theEnv.network.settings.setSetting("_funcs.Watch.activations", 
                                                       ActivationsWatcher(theEnv.RESOURCES['wtrace']).install(theEnv.network.eventsManager))

            if args.has_key("all") or args.has_key("focus"):
                try:
                    theEnv.network.settings.getSetting("_funcs.Watch.focus")
                except KeyError:
                    theEnv.network.settings.setSetting("_funcs.Watch.focus", 
                                                       FocusWatcher(theEnv.RESOURCES['wtrace']).install(theEnv.network.eventsManager))

            if args.has_key("all") or args.has_key("actions"):
                try:
                    theEnv.network.settings.getSetting("_funcs.Watch.actions")
                except KeyError:
                    theEnv.network.settings.setSetting("_funcs.Watch.actions", 
                                                       ActionsWatcher(theEnv.RESOURCES['wtrace']).install(theEnv.network.eventsManager))

            if args.has_key("all") or args.has_key("strategy"):
                try:
                    theEnv.network.settings.getSetting("_funcs.Watch.strategy")
                except KeyError:
                    theEnv.network.settings.setSetting("_funcs.Watch.strategy", 
                                                       StrategyWatcher(theEnv.RESOURCES['wtrace']).install(theEnv.network.eventsManager))

            if args.has_key("all") or args.has_key("statistics"):
                try:
                    theEnv.network.settings.getSetting("_funcs.Watch.statistics")
                except KeyError:
                    theEnv.network.settings.setSetting("_funcs.Watch.statistics", 
                                                       StatisticsWatcher(theEnv.RESOURCES['wtrace'], theEnv.network).install(theEnv.network.eventsManager))
        
        return types.NullValue()
    
    
Watch.DEFINITION = FunctionDefinition("?SYSTEM?", "watch", Watch(), types.NullValue, Watch.do ,
            [
                Constraint_MinArgsLength(1),
                Constraint_ArgType(types.Lexeme, (None,None), failIfMissing=False)
            ],forward=False)
        
        