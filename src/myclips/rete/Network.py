'''
Created on 24/lug/2012

@author: Francesco Capozzo
'''
from myclips.Agenda import Agenda
import myclips.parser.Types as types
from myclips.MyClipsException import MyClipsBugException, MyClipsException
from myclips.rete.nodes.PropertyTestNode import PropertyTestNode
from myclips.rete.tests.ScopeTest import ScopeTest
from myclips.rete.tests.ConstantValueAtIndexTest import ConstantValueAtIndexTest
from myclips.rete.tests.NegativeAlphaTest import NegativeAlphaTest
from myclips.rete.nodes.AlphaMemory import AlphaMemory
from myclips.rete.nodes.RootNode import RootNode
from myclips.rete.WME import WME
from myclips.rete.nodes.BetaMemory import BetaMemory
from myclips.rete.tests.VariableBindingTest import VariableBindingTest
from myclips.rete.nodes.JoinNode import JoinNode
from myclips.rete.tests.OrderedFactLengthTest import OrderedFactLengthTest
from myclips.rete.tests.locations import VariableLocation, AtomLocation
from myclips.rete.analysis import analyzePattern, normalizeAtom
from myclips.rete.tests.TemplateNameTest import TemplateNameTest
from myclips.rete.nodes.NegativeJoinNode import NegativeJoinNode
from myclips.rete.nodes.NccNode import NccNode
from myclips.rete import analysis
from myclips.rete.nodes.PNode import PNode
from myclips.EventsManager import EventsManager
from myclips.ModulesManager import ModulesManager, UnknownModuleError
from myclips.Fact import Fact
from myclips.TemplatesManager import TemplateDefinition
import sys


class Network(object):
    '''
    Rete network main object
    '''


    def __init__(self, eventsManager = None, modulesManager = None, resources=None):
        '''
        Constructor
        '''
        self._eventsManager = eventsManager if eventsManager is not None else EventsManager.default
        # if a custom modules manager is not submitted, a new default one (with MAIN scope) is used
        if modulesManager is None:
            modulesManager = ModulesManager()
            modulesManager.addMainScope()
            
        self._modulesManager = modulesManager
        self._root = RootNode(self)
        self.eventsManager.fire(EventsManager.E_NODE_ADDED, self._root)
        
        self._agenda = Agenda(self)
        self._rules = {}
        self._facts = {}
        self._factsWmeMap = {}
        self._currentWmeId = 0
        self._linkedParser = None
        self._deffacts = {}
        
        self._resources = resources or {"t" : sys.stdout,
                                        "stdin": sys.stdin,
                                        "stdout": sys.stdout,
                                        "wclips": sys.stdout,
                                        "wdialog": sys.stdout,
                                        "wdisplay": sys.stdout,
                                        "werror": sys.stdout,
                                        "wwarning": sys.stdout,
                                        "wtrace": sys.stdout}
        
        t = self._resources["t"]
        self._resources.setdefault("stdin", sys.stdin)
        self._resources.setdefault("stdout", t)
        self._resources.setdefault("wclips", t)
        self._resources.setdefault("wdialog", t)
        self._resources.setdefault("wdisplay", t)
        self._resources.setdefault("werror", t)
        self._resources.setdefault("wwarning", t)
        self._resources.setdefault("wtrace", t)
        
        self._init_resources = self._resources
        
        try:
            # assert the first fact: initial-fact
            self.assertFact(Fact({}, "initial-fact", "MAIN"))
        except:
            import myclips
            myclips.logger.warning("initial-fact redefinition")
            raise
        
        
    def getParser(self, **kargs):
        """
        Get an instance of myclips.Parser
        (default myclips.parser.Parser.Parser),
        linked to the modulesManager references in this Network instance 
        """
        if self._linkedParser is None:
            import myclips
            self._linkedParser = myclips.Parser(modulesManager=self.modulesManager, **kargs)
            
        return self._linkedParser
        
    def assertFact(self, fact):
        """
        Create a new WME and propagate it to the network
        only if the fact is not already in the working memory
        Return a tuple with the wme (created or the old one) which rappresent
        the fact and a boolean value to show if the wme is new or an old one
        
        @param fact: the fact asserted
        @type fact: Fact
        @return: a tuple with (WME for the fact, bool(the WME is new))
        @rtype: tuple 
        """
        
        if not isinstance(fact, Fact):
            raise InvalidFactFormatError("fact is expected to be a %s instance, %s passed"%(str(Fact), str(fact.__class__)))

        # check if a facts with the same features is already available
        # in the working memory
        # if it exists, return the tuple (old_wme, False)
        # otherwise return (new_wme, True) 
        # fact is propagate to the network only if
        # it's a new fact
        if not self._factsWmeMap.has_key(fact):
            
            # check if fact is valid
            
            # first check moduleName
            if not self.modulesManager.isDefined(fact.moduleName):
                raise UnknownModuleError("Fact module is unknown: %s"%fact.moduleName)
            
            # if fact is a template one
            if fact.isTemplateFact():
                # other validations are required for:
                #    templateName is valid?
                #    templateName is available in this scope?
                #    slots are valid for the template definition?
                
                # if the template name is invalid, an exception is raised 
                tmplDef = self.modulesManager.currentScope.templates.getDefinition(fact.templateName)
                
                assert isinstance(tmplDef, TemplateDefinition)
                
                isValid = tmplDef.isValidFact(fact)
                
                if isValid is not True:
                    raise InvalidFactFormatError(str(isValid))
                 
            
            # create the new wme, ...
            wme = WME(self._currentWmeId, fact)
            # ... link it in the facts table ...
            self._facts[self._currentWmeId] = wme
            # ... and link the fact to the wme
            self._factsWmeMap[wme.fact] = wme
            
            # increment the fact-id counter
            self._currentWmeId += 1 
            
            # propagate the new assertion in the network
            self._root.rightActivation(wme)
            
            # everything done, return the new wme
            # and the isNew marker
            return (wme, True)
        else:
            # the same fact is already in the network
            # just return the old fact and the isNotNew mark
            return (self._factsWmeMap[fact], False)
        
    def retractFact(self, wme):
        """
        Retract a WME from the working memory
        and from the network
        @param wme: the wme to be removed
        @type wme: myclips.rete.WME
        @return: None
        """
        assert isinstance(wme, WME)
        
        if not self._facts[wme.factId] == wme:
            raise InvalidWmeOwner("The wme owner is not this network: %s"%str(wme))
        
        # remove the wme from the wme->id map
        del self._facts[wme.factId]
        # and from the fact -> wme map
        del self._factsWmeMap[wme.fact]
        
        # then start wme revocation from the network
        wme.delete()
        
    
    def addRule(self, defrule):
        '''
        Compile a DefRuleConstruct in a network circuit
        sharing nodes if possible
        @param defrule: a DefRule construct which describe the rule
        @type defrule: types.DefRuleConstruct
        @return: the main PNode produced by the rule. If
            the rule containts more than one OR clause,
            other slave-PNodes are linked to the main one
        @rtype: myclips.rete.nodes.PNode
        '''
        
        
        if self._rules.has_key("::".join([defrule.scope.moduleName, defrule.defruleName])):
            # before add the new rule, need to remove the old one
            self.removeRule(defrule.defruleName, defrule.scope.moduleName)
            
        
        #normalize defule lhs
        defrule.lhs = analysis.normalizeLHS(defrule.lhs)
        # after normalization:
        #    defrule.lhs is a OrPatternCE with at least a nested AndPatternCe
        firstPNode = None
        for (index, AndInOr) in enumerate(defrule.lhs.patterns):
            
            variables = {}
            
            lastNode = self._makeNetwork(None, AndInOr.patterns, None, variables)
            
            # I need to create a PNode (and it must always linked to the first PNode created)
            pNode = PNode(ruleName=defrule.defruleName, 
                          leftParent=lastNode, 
                          network=self, 
                          orClauseCount=index - 1 if index > 0 else None,
                          rhs=defrule.rhs, 
                          properties=analysis.normalizeDeclarations(defrule.defruleDeclaration),
                          variables=variables)
            
            lastNode.prependChild(pNode)
            
            self.eventsManager.fire(EventsManager.E_NODE_ADDED, pNode)
            self.eventsManager.fire(EventsManager.E_NODE_LINKED, lastNode, pNode, -1)
            
            if firstPNode is None:
                firstPNode = pNode
            else:
                firstPNode.linkOrClause(pNode)
        
        # store the main PNode
        # inside the rules map
        
        self._rules[firstPNode.completeMainRuleName()] = firstPNode
        
        return firstPNode
    
    def removeRule(self, ruleName, moduleName=None):
        if moduleName is None:
            # the the moduleName from the current scope
            moduleName = self.modulesManager.currentScope.moduleName
            
        completeRuleName = "::".join([moduleName, ruleName])
            
        try:
            self._rules[completeRuleName].delete()
            del self._rules[completeRuleName]
        except KeyError:
            raise RuleNotFoundError("Unable to find defrule %s"%completeRuleName)
    
    def addDeffacts(self, deffacts):
        assert isinstance(deffacts, types.DefFactsConstruct)
        self._deffacts[deffacts.scope.moduleName+"::"+deffacts.deffactsName] = deffacts
        
    def removeDeffacts(self, deffactsName, deffactsModule=None):
        if deffactsModule is not None:
            tryName = deffactsModule + "::" + deffactsName
        else:
            tryName = deffactsName
            
        # try to remove the deffacts
        try:
            del self._deffacts[tryName]
        except KeyError:
            # key error: if module is None, try again using the current scope
            try:
                tryName = self.modulesManager.currentScope.moduleName + "::" + deffactsName
                del self._deffacts[tryName]
            except KeyError:
                raise DefFactsNotFoundError("Unable to find deffacts %s"%deffactsName)
    
    def getWmeFromId(self, factId):
        try:
            return self._facts[factId]
        except KeyError:
            raise FactNotFoundError("Unable to find fact f-%d"%factId)
    
    def getWmeFromFact(self, fact):
        try:
            return self._factsWmeMap[fact]
        except KeyError:
            raise FactNotFoundError("Unable to find a fact that match %s"%str(fact))
    
    def getPNode(self, completeRuleName):
        try:
            return self._rules[completeRuleName]
        except KeyError:
            # if the first lookup failed, try appending the current modulename scope
            # to the name
            try:
                return self._rules[self.modulesManager.currentScope.moduleName+"::"+completeRuleName]
            except:
                raise RuleNotFoundError("Unable to find defrule %s"%completeRuleName)
    
    def reset(self):
        """
        Reset the network status
        """
        
        # trigger event before reset
        self.eventsManager.fire(EventsManager.E_NETWORK_RESET_PRE, self)
         
        # retract all wme in the network
        for wme in self.facts:
            self.retractFact(wme)
        
        # reset the fact-id counter
        self._currentWmeId = 0
        
        # close all pending resources
        for (name, res) in self._resources.items():
            if name != 't' and hasattr(res, "close"):
                res.close()
                
        # and reset the resources map
        self._resources = {"t": sys.stdout}
        
        # push the MAIN::initial-fact
        self.assertFact(Fact({}, templateName="initial-fact", moduleName="MAIN"))
        
        # push all fact in deffacts again
        for deffact in self._deffacts.values():
            assert isinstance(deffact, types.DefFactsConstruct)
            # switch the scope the one defined in the deffact
            self.modulesManager.changeCurrentScope(deffact.scope.moduleName)
            # in this way asserted ordered fact gain the scope
            # from the current one and templates definition
            # could be checked vs module scope
            for pattern in deffact.rhs:
                if isinstance(pattern, types.TemplateRhsPattern):
                    assert isinstance(pattern, types.TemplateRhsPattern)
                    
                    # prepare values:
                    values = dict([(rhsSlot.slotName, rhsSlot.slotValue) for rhsSlot in pattern.templateSlots])
                    
                    # use the module name of the scope in the template,
                    # not the current one
                    self.assertFact(Fact(values, pattern.templateName, pattern.scope.moduleName))
                    
                elif isinstance(pattern, types.OrderedRhsPattern):
                    assert isinstance(pattern, types.OrderedRhsPattern)
                    
                    # prepare values
                    values = pattern.values
                    
                    # use the moduleName from the deffact scope (or the current one)
                    self.assertFact(Fact(values, moduleName=deffact.scope.moduleName))
                    
        # set current scope back to MAIN
        self.modulesManager.changeCurrentScope("MAIN")
        
        # trigger event after reset
        self.eventsManager.fire(EventsManager.E_NETWORK_RESET_POST, self)

        # all ready
            
    def clear(self):
        # trigger event before clear
        self.eventsManager.fire(EventsManager.E_NETWORK_CLEAR_PRE, self)
        
        # retract all facts
        for wme in self.facts:
            self.retractFact(wme)

        # destroy the network
        for rule in self._rules.values():
            self._rules[rule].delete()
            del self._rules[rule]
        
        # close all pending resources
        for (name, res) in self._resources.items():
            if not self._init_resources.has_key(name) and hasattr(res, "close"):
                res.close()
                
        # and reset the resources map
        self._resources = self._init_resources
        
        # renew the root node
        self._root = RootNode(self)
        
        # renew agenda and maps
        self._agenda = Agenda(self)
        self._rules = {}
        self._facts = {}
        self._factsWmeMap = {}
        self._currentWmeId = 0
        self._linkedParser = None
        self._deffacts = {}
            
        # destoy MM
        self._modulesManager = ModulesManager()
        self._modulesManager.addMainScope()
        
        try:
            # assert the first fact: initial-fact
            self.assertFact(Fact({}, "initial-fact", "MAIN"))
        except:
            import myclips
            myclips.logger.warning("initial-fact redefinition")

        # notify completed clear operation
        self.eventsManager.fire(EventsManager.E_NETWORK_CLEAR_POST, self)
        
        # detach all listeners after the CLEAR_POST events
        self.eventsManager.unregisterObserver()
        
        # for behavioural consistency, notify root creation
        self.eventsManager.fire(EventsManager.E_NODE_ADDED, self._root)

        # ok, all done

    
    @property
    def agenda(self):
        return self._agenda
        
    @property
    def resources(self):
        return self._resources
        
    @property
    def facts(self):
        """
        Return the list of all fact defined in the working memory
        for ALL defined scopes
        """
        return self._facts.values()

    def factsForScope(self, scopeName=None):
        """
        Return a list of wme for all facts
        that can be seen in the scope for scopeName
        @param scopeName: the moduleName for a defined module. If None
            the currentScope name will be used
        @type scopeName: string
        @return: a list of wme
        @rtype: list
        """
        if scopeName is not None:
            # try to change the scope
            # this will force an UnknownModuleError if the modules is not defined
            theScope = self.modulesManager.getScope(scopeName)
        else:
            theScope = self.modulesManager.currentScope
        
        # ok, the module exists. Prepare return
        return [wme for wme in self._facts.values()
                            # fact can be seen if it was defined in the scope (for ordered)
                            if wme.fact.moduleName == theScope.moduleName
                                # of if it's a template fact and is definition is imported in the current scope 
                                or (wme.fact.templateName is not None and theScope.templates.has(wme.fact.templateName)) ]

    @property
    def rules(self):
        return self._rules
    
    @property
    def eventsManager(self):
        return self._eventsManager

    @property
    def modulesManager(self):
        return self._modulesManager

    def _makeNetwork(self, node, patterns, prevPatterns=None, variables=None, testsQueue=None):
        
        variables = {} if variables is None else variables
        prevPatterns = [] if prevPatterns is None else prevPatterns
        testsQueue = [] if testsQueue is None else testsQueue 
        
        for (pIndex, patternCE) in enumerate(patterns):
            
            avoidAppend = False
            
            # get the pattern type:
            if isinstance(patternCE, (types.TemplatePatternCE, 
                                      types.AssignedPatternCE, 
                                      types.OrderedPatternCE)):
                
                # if patternCE is assigned, i need to propagate
                # alpha creation with the inner pattern,
                # not with the main assigned.
                # i use the assigned only to store info about variable
                # use old way to store variables coordinates, waiting for a new one
                if isinstance(patternCE, types.AssignedPatternCE):
                    variables[patternCE.variable.evaluate()] = VariableLocation(patternCE.variable.evaluate(), patternIndex=pIndex, fullFact=True)
                    patternCE = patternCE.pattern
                
                # requires a simple alpha circuit,
                # then a join + beta node if needed (beta join circuit)
                alphaMemory = self._makeAlphaCircuit(patternCE, testsQueue)
                node = self._makeBetaJoinCircuit(node, alphaMemory, patternCE, prevPatterns, variables)
                
                
            elif isinstance(patternCE, types.NotPatternCE):
                # need to check inside the pattern
                # if inside a not-ce there is a and-ce
                # i need to build a ncc
                
                if isinstance(patternCE.pattern, types.AndPatternCE):
                    # that's it: ncc required
                    
                    # this build the normal circuit
                    lastNccCircuitNode = self._makeNetwork(node, patternCE.pattern.patterns, prevPatterns, variables, testsQueue)
                    node = self._makeBetaNccCircuit(node, lastNccCircuitNode, len(patternCE.pattern.patterns))
                    # inner conditions already appended by recursive call
                    avoidAppend = True
                else:
                    # a simple negative join node is required

                    alphaMemory = self._makeAlphaCircuit(patternCE.pattern, testsQueue)
                    node = self._makeBetaNegativeJoinCircuit(node, alphaMemory, patternCE, prevPatterns, variables)

                
            elif isinstance(patternCE, types.TestPatternCE):
                # a special filter must be applied to
                # the circuit
                pass

            # or and and ce must not be supported here
            # after lhs normalization
            # or-ce could be only at top level
            #     of the lhs and are managed from the 
            #     addRule method (each or clause cause a new network circuit
            #     and a new sub-pnode linked to a main one
            # and-ce could be only after a not-ce or the main or-ce
            #    (managed by addRule method)
            #     and are managed as a ncc circuit

            #elif isinstance(patternCE, types.AndPatternCE):
                # need to add support for andCE
                # pass
                #node = self._makeNetwork(node, patternCE.patterns, prevPatterns, variables, testsQueue)
                # inner conditions already appended
                #avoidAppend = True  

                
            #elif isinstance(patternCE, types.OrPatternCE):
                # need to add support for orCE
                # pass
        
            if not avoidAppend:
                prevPatterns.append(patternCE)
            
        return node
            
    def _makeAlphaCircuit(self, patternCE, testQueue):
            import myclips
            # first i need to check the type of the patternCE
            # to create the correct list of tests
            
            lastCircuitNode = self._root

            # first thing to do is add a filter per-module
            # ordered facts are visible only in the module
            # who assert them
            lastCircuitNode = self._shareNode_PropertyTestNode(lastCircuitNode, [ScopeTest(patternCE.scope.moduleName)])
            
            if isinstance(patternCE, types.TemplatePatternCE):
                
                lastCircuitNode = self._shareNode_PropertyTestNode(lastCircuitNode, [TemplateNameTest(patternCE.templateName)])
                
                for slot in patternCE.templateSlots:
                    
                    if isinstance(slot, types.MultiFieldLhsSlot):
                        
                        multiFieldCount = 0
                        
                        for atomIndex, slotAtom in enumerate(slot.slotValue):
                            
                            atom, isNegative, connectedConstraints = normalizeAtom(slotAtom)
                            
                            # not fieldConstraint is a BaseParsedType | Variable
                            # only check for BaseParsedType, variables ignored
                            if isinstance(atom, types.BaseParsedType):
                                
                                indexLocation = AtomLocation()
                                indexLocation.slotName = slot.slotName
                                
                                if multiFieldCount > 0:
                                    indexLocation.fromEnd = True
                                    indexLocation.endIndex = len(slot.slotValue) - atomIndex - 1
                                else:
                                    indexLocation.fromBegin = True
                                    indexLocation.beginIndex = atomIndex
                                
                                # share or create a property test node for each type/value at index
                                tests = [ConstantValueAtIndexTest(indexLocation, atom)]
                                
                                # if this is a NegativeTest, i need to reverse all tests
                                if isNegative:
                                    tests = [NegativeAlphaTest(t) for t in tests]
                                    
                                lastCircuitNode = self._shareNode_PropertyTestNode(lastCircuitNode, tests)
                                
                            elif isinstance(atom, types.MultiFieldVariable):
                                
                                # if i got a multifield variable in the multislot,
                                # any index of constant value must be computed from the end
                                multiFieldCount += 1
                            
                    
                    elif isinstance(slot, types.SingleFieldLhsSlot):
                        atom, isNegative, connectedConstraints = normalizeAtom(slot.slotValue)
                        
                        if isinstance(atom, types.Variable):
                            continue
                        
                        indexLocation = AtomLocation(slotName=slot.slotName)
                        indexLocation.isMultiField = False
                        indexLocation.fullSlot = True
                        
                        tests = [ConstantValueAtIndexTest(indexLocation, atom)]
                        
                        if isNegative:
                            tests = [NegativeAlphaTest(t) for t in tests]
                            
                        lastCircuitNode = self._shareNode_PropertyTestNode(lastCircuitNode, tests)
                    
                    else:
                        myclips.logger.error("Unknown slot type in TemplatePatternCE: %s", slot.__class__.__name__)
                        raise MyClipsBugException("Unknown slot type: %s"%slot.__class__.__name__)
                
            elif isinstance(patternCE, types.OrderedPatternCE):
                
                multiFieldDelta = 0
                
                # this is easy to do:
                # first field is a symbol for parser constraints, but manually
                # submitted rules could have any types of value as first
                for (fieldIndex, fieldConstraint) in enumerate(patternCE.constraints):
                    
                    # ordered fact constraint could be:
                    #    BaseParsedType: (usually the first field is always a Symbol if rule is parsed)
                    #    Constraint<Term<BaseParsedType>
                    #    ConnectedConstraints<Term<BaseParsedType>, [[#connective, <Term>]*]>
                    # 
                    # Strategy is to check if is constraints first. If it is,
                    # replace fieldConstraints value with constraint value and continue
                    #
                    # then check for Term (Positive/Negative) and change tests for it
                    
                    isPositive = True
                    
                    if isinstance(fieldConstraint, types.Constraint):
                        # reduce Constraint to his content
                        fieldConstraint = fieldConstraint.constraint
                        
                    if isinstance(fieldConstraint, types.ConnectedConstraint):
                        # reduce ConnectedConstraint to his main constraint
                        myclips.logger.error("FIXME: Connected contraints alternative values ignored: %s", fieldConstraint.connectedConstraints)
                        fieldConstraint = fieldConstraint.constraint
                        
                    if isinstance(fieldConstraint, types.PositiveTerm):
                        fieldConstraint = fieldConstraint.term
                    
                    if isinstance(fieldConstraint, types.NegativeTerm):
                        isPositive = False
                        fieldConstraint = fieldConstraint.term
                        
                    # not fieldConstraint is a BaseParsedType | Variable
                    # only check for BaseParsedType, variables ignored
                    if isinstance(fieldConstraint, types.BaseParsedType):
                        
                        indexLocation = AtomLocation()
                        
                        if multiFieldDelta > 0:
                            indexLocation.fromEnd = True
                            indexLocation.endIndex = len(patternCE.constraints) - fieldIndex - 1
                        else:
                            indexLocation.fromBegin = True
                            indexLocation.beginIndex = fieldIndex 
                        
                        # share or create a property test node for each type/value at index
                        tests = [ConstantValueAtIndexTest(indexLocation, fieldConstraint)]
                        
                        # if this is a NegativeTest, i need to reverse all tests
                        if not isPositive:
                            tests = [NegativeAlphaTest(t) for t in tests]
                            
                        lastCircuitNode = self._shareNode_PropertyTestNode(lastCircuitNode, tests)
                        
                    elif isinstance(fieldConstraint, types.MultiFieldVariable):
                        
                        # if i got a multifield variable in a field of the ordered, any
                        # field constant value index after this it's not an exact index
                        # position, but is a "minimum index"
                        multiFieldDelta += 1
                        
                # at the end of the loop
                # i need to check if i have to add a lenght test over
                # the circuit (if no multifield variable is used)
                if multiFieldDelta == 0:
                    lastCircuitNode = self._shareNode_PropertyTestNode(lastCircuitNode, [
                                    OrderedFactLengthTest(fieldIndex + 1)
                                ])
                        
            else:
                myclips.logger.critical("Unknown patternCE type: %s", patternCE.__class__.__name__)
                raise MyClipsBugException("Unknown patternCE type: %s"%patternCE.__class__.__name__)
            
            # Here i've built all property test node
            # it's time to link an alpha memory at the end of them
            
            lastCircuitNode = self._shareNode_AlphaMemoryNode(lastCircuitNode)
            
            return lastCircuitNode
        
    def _makeBetaJoinCircuit(self, lastBetaCircuitNode, alphaMemory, patternCE, prevPatterns, variables):
        
        if lastBetaCircuitNode != None:
            lastBetaCircuitNode = self._shareNode_BetaMemory(lastBetaCircuitNode)
            
        # build tests for join node
        tests = []
        
        (newBindings, references) = analyzePattern(patternCE, len(prevPatterns), variables)
        
        # need to merge new bindings in variables
        variables.update(dict([(var.name, var) for var in newBindings]))
    
        # need to create a test of each reference in references
        for reference in references:
            tests.append(VariableBindingTest(reference))
            
         
        return self._shareNode_JoinNode(lastBetaCircuitNode, alphaMemory, tests )           
        

    def _makeBetaNegativeJoinCircuit(self, lastBetaCircuitNode, alphaMemory, patternCE, prevPatterns, variables):
        
        if lastBetaCircuitNode != None:
            lastBetaCircuitNode = self._shareNode_BetaMemory(lastBetaCircuitNode)
            
        # build tests for join node
        tests = []
        
        (newBindings, references) = analyzePattern(patternCE, len(prevPatterns), variables)
        
        # need to merge new bindings in variables
        variables.update(dict([(var.name, var) for var in newBindings]))
    
        # need to create a test of each reference in references
        for reference in references:
            tests.append(VariableBindingTest(reference))
            
         
        return self._shareNode_NegativeJoinNode(lastBetaCircuitNode, alphaMemory, tests )           
        

    def _makeBetaNccCircuit(self, lastBetaCircuitNode, lastNccCircuitNode, nccCircuitLength):
        
        return self._shareNode_NccNode(lastBetaCircuitNode, lastNccCircuitNode, nccCircuitLength)
        

    def _shareNode_AlphaMemoryNode(self, lastCircuitNode):
        """
        Try to share an AlphaMemoryNode available in the circuit
        if possible, otherwise create a new one and add it
        in the network
        
        @param lastCircuitNode: the node where the alpha memory should be linked
        @type lastCircuitNode: PropertyTestNode
        @return: a shared or a new AlphaMemory
        @rtype: AlphaMemory
        """
        
        assert isinstance(lastCircuitNode, PropertyTestNode)

        # if the last node has already a memory linked,
        # just use it        
        if lastCircuitNode.hasMemory():
            self.eventsManager.fire(EventsManager.E_NODE_SHARED, lastCircuitNode)
            return lastCircuitNode.memory
        
        # otherwise create a new one and return it
        memory = AlphaMemory(lastCircuitNode)
        lastCircuitNode.memory = memory
        
        #myclips.logger.info("New node: %s", memory)
        #myclips.logger.info("Linked node: %s to %s", memory, lastCircuitNode)
        
        self.eventsManager.fire(EventsManager.E_NODE_ADDED, memory)
        self.eventsManager.fire(EventsManager.E_NODE_LINKED, lastCircuitNode, memory, 0)
        
        # update the node
        lastCircuitNode.updateChild(memory)
        
        return memory

            
    def _shareNode_PropertyTestNode(self, lastCircuitNode, tests):
        
        if lastCircuitNode != None:
            for child in lastCircuitNode.children:
                if isinstance(child, PropertyTestNode)\
                    and child.tests == tests:
                    # found a node with same contraints
                    # i can share it
                    self.eventsManager.fire(EventsManager.E_NODE_SHARED, child)
                    return child
        
        # if a checked all children and found nothing
        # i need to create a new node for it
        newChild = PropertyTestNode(lastCircuitNode, tests)
        # maybe i could move this code inside the constructor
        lastCircuitNode.addChild(newChild)
        
        self.eventsManager.fire(EventsManager.E_NODE_ADDED, newChild)
        self.eventsManager.fire(EventsManager.E_NODE_LINKED, lastCircuitNode, newChild, 0)
        
        #myclips.logger.info("New node: %s", newChild)
        #myclips.logger.info("Linked node: %s to %s", newChild, lastCircuitNode)
        
        return newChild
    
    def _shareNode_BetaMemory(self, lastCircuitNode):
        
        # beta node are needed only if there is a parent node
        # otherwise dummy node only
        if lastCircuitNode is None:
            return lastCircuitNode
        
        # try to share the beta if possible    
        for child in lastCircuitNode.children:
            if isinstance(child, BetaMemory):
                self.eventsManager.fire(EventsManager.E_NODE_SHARED, child)
                return child
            
         
        # otherwise make a new one
        newChild = BetaMemory(lastCircuitNode)
        lastCircuitNode.prependChild(newChild)
        
        # update the node to synch the beta memory
        # status to the network status
        lastCircuitNode.updateChild(newChild)   
            
        #myclips.logger.info("New node: %s", newChild)
        #myclips.logger.info("Linked node: %s to %s", newChild, lastCircuitNode)

        self.eventsManager.fire(EventsManager.E_NODE_ADDED, newChild)
        self.eventsManager.fire(EventsManager.E_NODE_LINKED, lastCircuitNode, newChild, -1)
        
        return newChild
    
    def _shareNode_JoinNode(self, lastCircuitNode, alphaMemory, tests):
            
        # check if i can share looking at beta network first
        if lastCircuitNode is not None:
            
            for child in lastCircuitNode.children:
                
                # i can't use isinstance, child must be exactly a JoinNode
                # otherwise negative node could be shared and this is a problem
                if (child.__class__ == JoinNode
                    # is a join node
                    and child.rightParent == alphaMemory
                        # alpha memory is the same
                        and child.tests == tests):
                            # tests are the same too
                    
                    # i can share the node
                    self.eventsManager.fire(EventsManager.E_NODE_SHARED, child)
                    return child
        
        else:
            # try to share node looking at the alphaMemory
            # this could allow to share dummy join nodes
            for child in alphaMemory.children:
                # i can't use isinstance, child must be exactly a JoinNode
                # otherwise negative node could be shared and this is a problem
                if (child.__class__ == JoinNode
                    # is a join node
                    and child.isLeftRoot()
                        # like the node i will create, this one is left dummy
                        and child.tests == tests):
                            # tests are the same too
                    
                    # i can share the node
                    self.eventsManager.fire(EventsManager.E_NODE_SHARED, child)
                    return child
            
        # i can't share an old node
        # it's time to create a new one
        
        newChild = JoinNode(rightParent=alphaMemory, leftParent=lastCircuitNode, tests=tests)
        # link the new join to the right alpha memory
        alphaMemory.prependChild(newChild)
        
        if lastCircuitNode is not None:
            # link the join node to the parent
            lastCircuitNode.prependChild(newChild)
            # it's useless to update a leaf join node
            # even if it find matches
            # it has no children to propage the activation
        
        
        #myclips.logger.info("New node: %s", newChild)
        #myclips.logger.info("Right-linked node: %s to %s", newChild, alphaMemory)
        #myclips.logger.info("Left-linked node: %s to %s", newChild, lastCircuitNode)

        self.eventsManager.fire(EventsManager.E_NODE_ADDED, newChild)
        self.eventsManager.fire(EventsManager.E_NODE_LINKED, lastCircuitNode, newChild, -1)
        self.eventsManager.fire(EventsManager.E_NODE_LINKED, alphaMemory, newChild, 1)
        
        return newChild
    
    
    def _shareNode_NegativeJoinNode(self, lastCircuitNode, alphaMemory, tests):
            
        # check if i can share looking at beta network first
        if lastCircuitNode is not None:
            
            for child in lastCircuitNode.children:
                
                # i can't use isinstance, child must be exactly a JoinNode
                # otherwise negative node could be shared and this is a problem
                if (child.__class__ == JoinNode
                    # is a join node
                    and child.rightParent == alphaMemory
                        # alpha memory is the same
                        and child.tests == tests):
                            # tests are the same too
                    
                    # i can share the node
                    self.eventsManager.fire(EventsManager.E_NODE_SHARED, child)
                    return child
        
        else:
            # try to share node looking at the alphaMemory
            # this could allow to share dummy join nodes
            for child in alphaMemory.children:
                # i can't use isinstance, child must be exactly a JoinNode
                # otherwise negative node could be shared and this is a problem
                if (child.__class__ == NegativeJoinNode
                    # is a join node
                    and child.isLeftRoot()
                        # like the node i will create, this one is left dummy
                        and child.tests == tests):
                            # tests are the same too
                    
                    # i can share the node
                    self.eventsManager.fire(EventsManager.E_NODE_SHARED, child)
                    return child
            
        # i can't share an old node
        # it's time to create a new one
        
        newChild = NegativeJoinNode(rightParent=alphaMemory, leftParent=lastCircuitNode, tests=tests)
        # link the new join to the right alpha memory
        alphaMemory.prependChild(newChild)
        
        if lastCircuitNode is not None:
            # link the join node to the parent
            lastCircuitNode.prependChild(newChild)
            
            # try to update from the left
            lastCircuitNode.updateChild(newChild)
            
        else:
            
            # try to update from the right
            alphaMemory.updateChild(newChild)
            
        #myclips.logger.info("New node: %s", newChild)
        #myclips.logger.info("Right-linked node: %s to %s", newChild, alphaMemory)
        #myclips.logger.info("Left-linked node: %s to %s", newChild, lastCircuitNode)

        self.eventsManager.fire(EventsManager.E_NODE_ADDED, newChild)
        self.eventsManager.fire(EventsManager.E_NODE_LINKED, lastCircuitNode, newChild, -1)
        self.eventsManager.fire(EventsManager.E_NODE_LINKED, alphaMemory, newChild, 1)

        
        return newChild    
    
    def _shareNode_NccNode(self, lastCircuitNode, lastNccCircuitNode, partnerCircuitLength):
        
        if lastCircuitNode is None:
            raise MyClipsBugException("Don't know how to handle this")
        
        # try to search for a ncc child of last circuit
        for child in lastCircuitNode.children:
            if isinstance(child, NccNode):
                # it's a ncc, check of it's exactly the same circuit
                # from the right too
                if child.partner.leftParent == lastNccCircuitNode:
                    # ncc in the child + same ncc circuit
                    # this means i can share it
                    self.eventsManager.fire(EventsManager.E_NODE_SHARED, child)
                    return child
                
        # i can't share the node
        # so create a new one
        
        newChild = NccNode(lastCircuitNode, lastNccCircuitNode, partnerCircuitLength)
        
        # link the newChild and the partner to the parents
        
        # ncc have to be the last child to be called
        # because the partner must have token in the buffer
        
        lastCircuitNode.appendChild(newChild)
        lastNccCircuitNode.prependChild(newChild.partner)
        
        # new i need to update the node couple
        # first i update the ncc main node
        # then the parent (this way when token comes to the partner
        # the ncc has already partial results)
        
        lastCircuitNode.updateChild(newChild)
        lastNccCircuitNode.updateChild(newChild.partner)

        # print connections
        
#        myclips.logger.info("New node: %s", newChild)
#        myclips.logger.info("New node: %s", newChild.partner)
#        myclips.logger.info("Partner-linked node: %s to %s", newChild, newChild.partner)
#        myclips.logger.info("Left-linked node: %s to %s", newChild, lastCircuitNode)
#        myclips.logger.info("Left-linked node: %s to %s", newChild.partner, lastNccCircuitNode)
        
        self.eventsManager.fire(EventsManager.E_NODE_ADDED, newChild)
        self.eventsManager.fire(EventsManager.E_NODE_ADDED, newChild.partner)
        self.eventsManager.fire(EventsManager.E_NODE_LINKED, lastCircuitNode, newChild, -1)
        self.eventsManager.fire(EventsManager.E_NODE_LINKED, lastNccCircuitNode, newChild.partner, -1)
        self.eventsManager.fire(EventsManager.E_NODE_LINKED, newChild.partner, newChild, 0)
        
        
        return newChild
    
    
class FactNotFoundError(MyClipsException):
    pass

class InvalidFactFormatError(MyClipsException):
    pass
    
class RuleNotFoundError(MyClipsException):
    pass

class DefFactsNotFoundError(MyClipsException):
    pass

class InvalidWmeOwner(MyClipsException):
    pass