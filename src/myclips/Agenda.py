'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.EventsManager import EventsManager
import myclips.strategies as strategies
from myclips.MyClipsException import MyClipsException

class Agenda(object):
    '''
    myclips actiovations Agenda
    '''

    def __init__(self, network):
        '''
        Constructor
        '''
        self._network = network
        # Keep all activations organized
        # as a dict of per-module dicts of
        # strategy's activation container
        # using module's name as top dict
        # index and salience as
        # inner dicts's keys
        self._activations = {}
        # Keep sets of fired activation
        # using a per-complete-rule-name based index
        self._fired_activations = {}
        self._strategy = strategies.factory.newInstance()
        self._ignored_activations = {}
        self._focusStack = []
        try:
            self._focusStack.append(network.modulesManager.currentScope.moduleName)
        except:
            pass 
        
    @property
    def focusStack(self):
        """
        Get the focus stack
        """
        return self._focusStack
        
    def insert(self, pnode, token):
        '''
        Add a new activation inside the agenda
        (only if a same activation wasn't fired in past)        
        '''
        from myclips.rete.nodes.PNode import PNode
        assert isinstance(pnode, PNode)

        # check if the same activation was already fired in the past
        if self._isInFired(pnode.completeRuleName(), token.hashString):
            # store the activation in a structure to allow
            # the refresh method to re-add ignored activation on the need
            #    NB: double dict is necessary to avoid duplications
            #        in ignored_activations
            try:
                ruleDict = self._ignored_activations[pnode.completeRuleName()]
            except KeyError:
                # no ignored activations for this rule, create a new dict for it
                ruleDict = {}
                self._ignored_activations[pnode.completeRuleName()] = ruleDict
                
            ruleDict[token.hashString] = (pnode, token)
            return

        salience = pnode.getSalience()

        self._network.eventsManager.fire(EventsManager.E_RULE_ACTIVATED, pnode, token)

        try:
            per_module_activations = self._activations[pnode.moduleName]
        except KeyError:
            # not previous rules of this module
            # got an activation, so the dict have to be
            # created
            per_module_activations = {}
            self._activations[pnode.moduleName] = per_module_activations

        try:
            same_salience_queue = per_module_activations[salience]
        except KeyError:
            
            # if no previous rule with the same salience
            # was insered before, the activation container
            # have to be initialized
            # let's create the new container
            same_salience_queue = self._strategy.newContainer()
            per_module_activations[salience] = same_salience_queue
        
        # delegate the insert operation to the strategy
        #    (it know how to insert the activation in
        #        its own container)
        self._strategy.insert(same_salience_queue, pnode, token)
    
    def getActivation(self):
        '''
        Get the max priority activation for the
        currentScope to be executed
        '''
        # get the current module activations container
        try:
            # get the module key from the focus stack
            try:
                moduleKey = self.focusStack[-1]
                if moduleKey != self._network.modulesManager.currentScope.moduleName:
                    # the focus changed, update the scope
                    self._network.modulesManager.changeScope(moduleKey)
            except IndexError:
                # the stack is empty. Try with the current module
                moduleKey = self._network.modulesManager.currentScope.moduleName
            
            module_activations = self._activations[moduleKey]
        except KeyError:
            # no activations for this module
            # raise an exception to 
            # notify no more activations left for this module
            raise AgendaNoMoreActivationError()
        
        max_salience = max(module_activations.keys())
        pnode, token = self._strategy.pop(module_activations[max_salience])
        # check if more activations are available with the same salience
        if len(module_activations[max_salience]) == 0:
            # when no more rule for the current salience
            # are available, remove the container too
            del module_activations[max_salience]
            
        # check if more activations are available with the same module
        if len(module_activations) == 0:
            # when no more activations for the current
            # module are availble, remove the container
            # (this way, on the next getActivation call
            # a AgendaNoMoreActivationError will be raised
            # and network run loop will try to change the 
            # currentScope
            del self._activations[moduleKey]
        
        from myclips.rete.nodes.PNode import PNode
        assert isinstance(pnode, PNode)
        
        completeRuleName = pnode.completeRuleName()
        
        ##########################################################
        # store the activation inside a fired activation history #
        ##########################################################
        
        # get the history for the rule
        if self._fired_activations.has_key(completeRuleName):
            fired_per_rule = self._fired_activations[completeRuleName]
        else:
            # if no history found, create a new empty history
            fired_per_rule = set()
            # and store it
            self._fired_activations[completeRuleName] = fired_per_rule
            
        # archive the activation
        # using the token.hashString
        # NB:
        #    token's hashString is a token conversion
        #    to an unique string of the token's wme list
        fired_per_rule.add(token.hashString)
        
        return (pnode, token)
        
    def refresh(self, completeRuleName):
        '''
        Reset the fired activations history
        for the rule with ruleName
        '''
        try:
            # remove the memory for the completeRuleName
            del self._fired_activations[completeRuleName]
            
            # then revaluate all ignored activations
            # that could be re-insered in the agenda
            for pnode, token in self._ignored_activations[completeRuleName].values():
                self.insert(pnode, token)
                
            # remove ignored_activation for this rule
            del self._ignored_activations[completeRuleName]
            
        except KeyError:
            # no fired activations (this implies no ignored activation too)
            # or
            # fired activations but no ignored activation yer
            # nothing to do, return
            return
        
    def remove(self, pnode, token):
        '''
        Remove an activation from the agenda
        '''
        
        salience = pnode.getSalience()
        
        self._network.eventsManager.fire(EventsManager.E_RULE_ACTIVATED, pnode, token)

        ########################################################
        # Remove the activation from activables agenda, if any #
        ########################################################
        
        try:
            
            per_module_activations = self._activations[pnode.moduleName]
            
            same_salience_queue = per_module_activations[salience]

            self._strategy.remove(same_salience_queue, pnode, token)
            
            if len(same_salience_queue) == 0:
                del per_module_activations[salience]
                
            if len(per_module_activations) == 0:
                del self._activations[pnode.moduleName]
                
        except (KeyError, ValueError):
            # no per-module activations
            # or no per-salience module activation
            # = this activation is not in the activable agenda
            pass
            
        #######################################################
        # Remove the activation from the ignored ones, if any #
        #######################################################
        
        try:
            del self._ignored_activations[pnode.completeRuleName()][token.hashString]
        except KeyError:
            # no token.hashString in per-rule-ignored
            # or no per-rule-ignored in ignored
            pass

        try:        
            if len(self._ignored_activations[pnode.completeRuleName()]) == 0:
                del self._ignored_activations[pnode.completeRuleName()]
        except:
            # no per-rule-ignored
            pass
        
        
    def clear(self):
        '''
        Completly reset agenda status
        '''
        self._activations = {}
        self._fired_activations = {}
        self._ignored_activations = {}
        

    def refreshAll(self):
        '''
        Reset the fired activations history
        for the all rules (and reevaluate ignored activations)
        '''
        
        self._fired_activations = {}
        
        for ignoredAct in self._ignored_activations.values():
            for pnode, token in ignoredAct.values():
                self.insert(pnode, token)
                
    
    def isEmpty(self):
        '''
        Check if the activation queue is empty for the 
        current module
        '''
        try:
            return len(self._activations[self._network.modulesManager.currentScope.moduleName]) == 0
        except KeyError:
            # key-error = there is no _per_modules_activations_dict_ = no activations left
            # so... return true
            return True
        
    def isEmptyAllModules(self):
        '''
        Check if the activation queue is empty for all modules
        '''
        return len(self._activations) == 0
    
    def changeStrategy(self, strategy):
        """
        Change the current strategy with a new one
        resorting the activations with the strategy 
        """
        self._network.eventsManager.fire(EventsManager.E_STRATEGY_CHANGED, strategy)
        if self._strategy != strategy:
            oldStrategy = self._strategy
            self._strategy = strategy
            if not self.isEmptyAllModules():
                # there is at least one activation
                # so i need to resort all containers
                for per_modules_queue in self._activations.values():
                    for (salience, per_saliance_list) in per_modules_queue.items():
                        returned = self._strategy.resort(per_saliance_list, oldStrategy)
                        if returned is not None:
                            # the new strategy can't do on-place-resort
                            # so, returned a new container to replace the old one
                            per_modules_queue[salience] = returned
                            
                    
    def activations(self, moduleName=None):
        moduleName = moduleName if moduleName is not None else self._network.modulesManager.currentScope.moduleName
        try:
            saliences = sorted(self._activations[moduleName].keys(), reverse=True)
            activations = []
            for salience in saliences:
                for (pnode, token) in self._strategy.iterable(self._activations[moduleName][salience]):
                    activations.append((salience, pnode, token))
            activations.reverse()
            return activations
        except:
            return []
    
    def _isInFired(self, completeRuleName, tokenHashString):
        try:
            return (tokenHashString in self._fired_activations[completeRuleName])
        except KeyError:
            # on KeyError caught, no previous
            # activation for this completeRuleName was fired
            return False
    
class AgendaNoMoreActivationError(MyClipsException):
    pass
