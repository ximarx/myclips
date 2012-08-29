'''
Created on 27/lug/2012

@author: Francesco Capozzo
'''

import myclips.parser.Types as types
from myclips.rete.tests.locations import VariableLocation, VariableReference,\
    AtomLocation
from myclips.MyClipsException import MyClipsBugException, MyClipsException
from myclips.rete.tests.AlphaInBetaNetworkTest import AlphaInBetaNetworkTest
from myclips.rete.tests.OrConnectiveTest import OrConnectiveTest
from myclips.rete.tests.OrderedFactLengthTest import OrderedFactLengthTest
from myclips.rete.tests.ScopeTest import ScopeTest
from myclips.rete.tests.TemplateNameTest import TemplateNameTest
from myclips.rete.tests.MultislotLengthTest import MultislotLengthTest
from myclips.rete.tests.ConstantValueAtIndexTest import ConstantValueAtIndexTest
from myclips.rete.tests.NegativeAlphaTest import NegativeAlphaTest
from myclips.rete.tests.DynamicFunctionTest import DynamicFunctionTest
from myclips.rete.tests.VariableBindingTest import VariableBindingTest
from copy import copy

def getVar(varName, variables, inPatternVariables):
    '''
    Get a location where the ?varName variable
    was found first or False if the ?varName is not defined yet
    
    @param varName: a variable name
    @type varName: string
    @param variables: a dict of varName => VariableLocation
    @param inPatternVariables: a list of variable found in the same pattern
        and not merged to the main dict yet
    @return: VariableLocation or False
    '''
    
    if variables.has_key(varName):
        return variables[varName]
    
    for prevVar in inPatternVariables:
        if prevVar.name == varName:
            return prevVar
    
    return False



def analyzeFunction(theFunction, patternIndex, variables, inPatternVariables=None, fakeVariables = None, realToFakeMap = None, vIndex = None, fakeNames = None):
    '''
    Analyze a FunctionCall inside a Test-CE to replace variables name with fake names
    an bound locations to improve reuse of test-nodes (normalize variables names) 
    
    @param theFunction: a function call to replace
    @type theFunction: types.FunctionCall
    @param patternIndex: the index of the test-pattern in the chain of ce
    @type patternIndex: int
    @param variables: a dict of variable name => VariableReferences
    @type variables: dict
    @param fakeVariables: a dict of fake variables references or None (to make a new one)
    @type fakeVariables: dict
    @param realToFakeMap: a map of real variables names to fake ones
    @type realToFakeMap: dict
    @param vIndex: the index for fake variables name generation
    @type vIndex: int
    '''
    
    inPatternVariables = [] if inPatternVariables is None else inPatternVariables
    aNewFunctionCallArgs = []
    fakeVariables = {} if fakeVariables is None else fakeVariables
    fakeNames = {} if fakeNames is None else fakeNames
    realToFakeMap = {} if realToFakeMap is None else realToFakeMap
    vIndex = [] if vIndex is None else vIndex;
    
    if isinstance(theFunction, types.FunctionCall):
        
        assert isinstance(theFunction, types.FunctionCall)
        
        for aArg in theFunction.funcArgs:
            
            # globals are resolved at function-call execution time
            if isinstance(aArg, (types.SingleFieldVariable, types.MultiFieldVariable)):
                # i've already created a fake_var for this var?
                if not realToFakeMap.has_key(aArg.evaluate()) :
                
                    # where i found the variable first?
                    mainReference = getVar(aArg.evaluate(), variables, inPatternVariables)
                    
                    if mainReference is False:
                        raise MyClipsException("Variable %s found in the expression %s was referenced in CE #%d before being defined."%(
                                aArg.evaluate(),
                                theFunction.toClipsStr(),
                                patternIndex
                            ))
                    
                    varReference = VariableReference()
                    varReference.reference = mainReference
                    varReference.relPatternIndex = mainReference.patternIndex - patternIndex
                    
                    theFakeName = "%"+str(len(vIndex))
                    vIndex.append(None)
                    
                    theFakeVar = aArg.__class__(types.Symbol(theFakeName)) 
                    
                    fakeVariables[theFakeVar.evaluate()] = varReference
                    realToFakeMap[aArg.evaluate()] = theFakeVar.evaluate()
                    fakeNames[aArg.evaluate()] = theFakeVar 
                
                else:
                    theFakeVar = fakeNames[aArg.evaluate()]
                     
                
                # replace the variable name with a fake name
                #aArg.content = theFakeName
                aNewFunctionCallArgs.append(theFakeVar)
                
            elif isinstance(aArg, types.FunctionCall):
                
                # recursion: replace arguments inside the function call
                # fakeReferences are ignored because the dict is automatically
                # updated by the recursion.
                aInnerNewFunctionCall, _ = analyzeFunction(aArg, patternIndex, variables, inPatternVariables, fakeVariables, realToFakeMap, vIndex, fakeNames)
                
                # replace the old function call with a new one with fake variables
                #theFunction.funcArgs[iArg] = aInnerNewFunctionCall
                aNewFunctionCallArgs.append(aInnerNewFunctionCall)
                
            else:
                aNewFunctionCallArgs.append(aArg)
    
        # get the current scope and backup it
        _tmp_scope = theFunction.scope.modules.currentScope
        # then change it to the original function call scope
        theFunction.scope.modules.changeCurrentScope(theFunction.scope.moduleName)
        # create the new function call
        newFunctionCall = types.FunctionCall(theFunction.funcName, theFunction.scope.modules, aNewFunctionCallArgs)
        # then restore the previous scope
        theFunction.scope.modules.changeCurrentScope(_tmp_scope.moduleName)
    
        return (newFunctionCall, fakeVariables)
    
    else: raise TypeError("AnalyzeFunction require a FunctionCall as first argument")
    


    
def _analyzeTerm(atomLocation, aTerm, variables, inPatternVariables):
    '''
    Analyze a types.Term and create a list of pattern tests and join tests
    to describe the term
    
    @param atomLocation: the location of the term inside the LHS
    @param aTerm: a types.Term element
    @param variables: a dict of varName => VarLocation(s) in previous patterns
    @param inPatternVariables: a list of VarLocations in the current pattern
    '''
    

    alphaTests = []
    joinTests = []
    
    isNegative = True if isinstance(aTerm, types.NegativeTerm) else False
    # dewrap: aTerm from a Term object to Term's content 
    aTerm = aTerm.term
    
    if isinstance(aTerm, (types.MultiFieldVariable, types.SingleFieldVariable)):
        varLocation = VariableLocation.fromAtomLocation(aTerm.evaluate(), atomLocation)
        # check the main location of the variable
        # but if it's the same of this location, ignore the cc
        mainReference = getVar(aTerm.evaluate(), variables, inPatternVariables)
        if mainReference is not False:
            # create a reference to this variable
            varReference = VariableReference()
            varLocation.toVarReference(varReference)
            varReference.reference = mainReference
            varReference.isNegative = isNegative
            # calcolate the relPatternIndex
            if varLocation.patternIndex is not None:
                varReference.relPatternIndex = mainReference.patternIndex - varLocation.patternIndex
            else:
                varReference.relPatternIndex = 0
            
            # make a new join test
            joinTests.append(VariableBindingTest(varReference))
            
        else:
            # unknown variable!
            inPatternVariables.append(varLocation)
        
    elif isinstance(aTerm, types.BaseParsedType):
        # a pattern test is required, but created by _makeAlphaNetwork. so ignore
        # remove patternIndex location from the atomLocation
        # because alpha tests are always on the wme from the right
        atomLocationCopy = copy(atomLocation)
        atomLocationCopy.patternIndex = None
        aAlphaTest = ConstantValueAtIndexTest(atomLocationCopy, aTerm)
        alphaTests.append(aAlphaTest if not isNegative else NegativeAlphaTest(aAlphaTest))
    
    elif isinstance(aTerm, types.FunctionCall):
        # well... this is a special case. This must be converted in a
        # (test (function-call))
        _newFunc, _fakeVar = analyzeFunction(aTerm, atomLocation.patternIndex, variables, inPatternVariables)
        joinTests.append(DynamicFunctionTest(_newFunc, _fakeVar))
        
    # unnamed multifield and single field are ignored
        
    return (alphaTests, joinTests)

    
def _analyzeConstraint(aConstraint, atomLocation, variables, inPatternVariables):
    '''
    Analyze a types.Constraint or types.ConnectedConstraint element
    to extract a list of pattern-test or join-test over the element
     
    @param aConstraint: a types.Constraint or a types.ConnectedConstraint
    @param atomLocation: the item location
    @param variables: a dict of variables found in previous patterns
    @param inPatternVariables: a list of variables found in the current pattern
    '''
    
    # both connected than simple constraints have got the $.constraint field to analyze
    # but first field in ordered could be not wrapped by Constraint or CConstraint
    # so, a normalization must be applied
    firstField = aConstraint.constraint if isinstance(aConstraint, (types.ConnectedConstraint, types.Constraint)) else aConstraint
    firstField = types.PositiveTerm(firstField) if not isinstance(firstField, types.Term) else firstField 
    
    alphaTests, joinTests = _analyzeTerm(atomLocation, firstField, variables, inPatternVariables)
    
    # but only ConnectedConstraints has a connectedConstraint field
    
    if isinstance(aConstraint, types.ConnectedConstraint):
    
        ccLength = len(aConstraint.connectedConstraints)
        for i in range(0, ccLength):
            conj, aTerm = aConstraint.connectedConstraints[i]
    
            alphas, joins = _analyzeTerm(atomLocation, aTerm, variables, inPatternVariables)
            
            if conj == "|": # // or
                # wrap the cc in a or ( [tests] | B )
                
                if len(joinTests) > 0:
                    # all tests for this constraint must be done on beta network
                    if len(alphas) > 0:
                        joins = [AlphaInBetaNetworkTest(alphas)]
    
                    if len(joins) > 0:
                        #joinTests += joins
                        joinTests = joinTests[:-1] + [OrConnectiveTest(joinTests[-1:] + joins)]
                else:
                    if len(alphas) > 0:
                        alphaTests = alphaTests[:-1] + [OrConnectiveTest(alphaTests[-1:] + alphas)]
                    elif len(joins) > 0:
                        # need to be carefull:
                        # if i got a new join test and i got previous
                        # alpha tests, i need to convert them in alpha-in-beta-network tests
                        if len(alphaTests) > 0:
                            joinTests = [AlphaInBetaNetworkTest(alphaTests[:-1])] + [OrConnectiveTest([AlphaInBetaNetworkTest(alphaTests[-1:])] + joins)]
                            alphaTests = []
                            
                        else:
                            joinTests = [OrConnectiveTest(joins)] 
                
                
            else: # conj == & // and
    
                if len(joinTests) > 0:
                    # all tests for this constraint must be done on beta network
                    if len(alphas) > 0:
                        joins = [AlphaInBetaNetworkTest(alphas)]
    
                    if len(joins) > 0:
                        joinTests += joins
                else:
                    if len(alphas) > 0:
                        alphaTests += alphas
                    elif len(joins) > 0:
                        # need to be carefull:
                        # if i got a new join test and i got previous
                        # alpha tests, i need to convert them in alpha-in-beta-network tests
                        if len(alphaTests) > 0:
                            joinTests = [AlphaInBetaNetworkTest(alphaTests)] + joins
                            alphaTests = []
                        else:
                            joinTests = joins
    
    return (alphaTests, joinTests)
    
def _isMultifield(atom):
    '''
    Check the atom composition and return True
    if it could contain a multifield element
    
    FunctionCall evaluation is done checking return types:
    if list is one of their possible values, this function return True
    
    $.constraint field is evaluated for types.ConnectedConstraint atoms
    (this means only the first element of a CC)
    
    @param atom: a types.Constraint or types.ConnectedConstraint element
    @rtype: boolean
    '''
    
    
    while not isinstance(atom, (types.Variable, types.BaseParsedType, types.FunctionCall)):
        if isinstance(atom, types.ConnectedConstraint):
            atom = atom.constraint
        
        elif isinstance(atom, types.Constraint):
            atom = atom.constraint
            
        elif isinstance(atom, types.Term):
            atom = atom.term
            
        else:
            break
        
    if isinstance(atom, types.FunctionCall):
        # check the return values: it could be a multifield?
        return list in atom.funcDefinition.returnTypes
    else:
        return isinstance(atom, (types.MultiFieldVariable, types.UnnamedMultiFieldVariable))
    
    
def _toAtomSequence(aSequence):
    
    prevMultifieldCount = 0
    returnSequence = []
    
    for fieldIndex, fieldContent in enumerate(aSequence):
        
        atomLocation = AtomLocation()
        isMultiField = _isMultifield(fieldContent) 
        
        if prevMultifieldCount and isMultiField:
            raise MyClipsException("Two multifields in a single expression found!")
            
        # calculate position from the end
        if prevMultifieldCount == 0:
            atomLocation.beginIndex = fieldIndex
            atomLocation.fromBegin = True
            
        if prevMultifieldCount > 0 or isMultiField :
            atomLocation.endIndex = len(aSequence) - fieldIndex - 1
            atomLocation.fromEnd = True
            
        if isMultiField:
            prevMultifieldCount += 1
            atomLocation.isMultiField = True
            
        returnSequence.append((atomLocation, fieldContent))
        
    return returnSequence
    
    
def _patternToAtomLocations(aPatternCE, patternIndex):
    
    if isinstance(aPatternCE, types.OrderedPatternCE):
        
        returnSequence = _toAtomSequence(aPatternCE.constraints)
        for atomLocation, _ in returnSequence:
            atomLocation.patternIndex = patternIndex
    
        return returnSequence
    
    elif isinstance(aPatternCE, types.TemplatePatternCE):
        
        returnSequence = []
        
        for slot in aPatternCE.templateSlots:
            
            if isinstance(slot, types.SingleFieldLhsSlot):
                # easy to handle: convert the location to a atom location with a field element
                atomLocation = AtomLocation()
                atomLocation.slotName = slot.slotName
                atomLocation.fullSlot = True
                atomLocation.patternIndex = patternIndex
            
                returnSequence.append((atomLocation, slot.slotValue))
                
            else:
                
                multifieldSequence = _toAtomSequence(slot.slotValue)
                for atomLocation, _ in returnSequence:
                    atomLocation.patternIndex = patternIndex
                    atomLocation.slotName = slot.slotName
                    
                returnSequence += multifieldSequence
                
        return returnSequence
        
    else:
        raise ValueError("Invalid aPatternCE types: %s"%aPatternCE.__class__.__name__)
    
    
def analyzePattern(aPatternCE, patternIndex, variables, inPatternVariables):
    
    # this function iterate over aPatternCE's elements and
    # call other analysis function to create alpha/join tests about the elements
    # then return the list of list of alpha and join tests
    
    listOfAlphas = []
    listOfJoins = []
    
    atoms = _patternToAtomLocations(aPatternCE, patternIndex)
    
    prevSlotName = None
    addMultifieldLength = False # starting value == True because on first lostname change from None to slotName
                            # the slottest length must not be added
    lastMultiSlotIndex = -1
    
    for (atomLocation, aConstraint) in atoms:
        
        # check slot focus change and need to add multi-slot length test
        if isinstance(aPatternCE, types.TemplatePatternCE):
            
            # on slot name change
            if prevSlotName != atomLocation.slotName:
                # if a length test could be usefull
                if addMultifieldLength:
                    # add it
                    listOfAlphas.append(MultislotLengthTest(prevSlotName, lastMultiSlotIndex + 1))
            
                prevSlotName = atomLocation.slotName
                lastMultiSlotIndex = -1
                # choose if this slot need a length test: if is a multislot, then it could need one
                # otherwise no for sure!
                addMultifieldLength = False if atomLocation.fullSlot is True else True
                
            # choose if this multislot still need a length test: if no multifield value
            # has been found it could need one!
            addMultifieldLength = addMultifieldLength and not atomLocation.isMultiField
            lastMultiSlotIndex += 1 
        
        alphas, joins = _analyzeConstraint(aConstraint, atomLocation, variables, inPatternVariables)
        
        if len(alphas) > 0:
            listOfAlphas.append(alphas)
            
        # some alpha test could be added for TemplateFact: if multifieldSlot length test could be add
            
        if len(joins) > 0:
            listOfJoins += joins
            
    if isinstance(aPatternCE, types.OrderedPatternCE):
        # need to add a scope-test as first test in alpha
        listOfAlphas.insert(0, [ScopeTest(aPatternCE.scope.moduleName)])
        
        # need to add a length if no multifield inside!
        # if the last atom location of the sequence of atoms has fromEnd = True
        # then at least 1 multifield is in the sequence and no length test must be added
        if atoms[-1][0].fromEnd is not True:
            listOfAlphas.append( [OrderedFactLengthTest(len(aPatternCE.constraints))] )
            
    elif isinstance(aPatternCE, types.TemplatePatternCE):
        # order of test insertion is reversed because a insert-top is done
        listOfAlphas.insert(0, [TemplateNameTest(aPatternCE.templateName)])
        listOfAlphas.insert(0, [ScopeTest(aPatternCE.templateDefinition.moduleName)])
        # real order will be:
        # ROOT -> SCOPE -> TEMPLATE -> SLOTS...
        
            
    return listOfAlphas, listOfJoins
    

def normalizeLHS(lhs, MM):
    """
    Change patterns orders (and nested patterns order)
    to normalize lhs in a Or (And ( normal form
    with all nested Or regrouped in a single
    top level Or
    """
    
    if isinstance(lhs, list):
        
        # check if LHS has not pattern and handle this case as
        # (or (and (initial-fact)))
        if len(lhs) == 0:
            return types.OrPatternCE([types.AndPatternCE([_makeInitialFactPattern(MM)])])
        
        # wrap the pattern list with an AndCE
        lhs = types.AndPatternCE(lhs)
        
    if isinstance(lhs, types.AndPatternCE):
        # wrap the AndCE with an OrCE
        lhs = types.OrPatternCE([lhs])
        
    # then normalize lhs in a
    # form that has
    # all or inside the lhs reduced to
    # a single or at the top level of
    # the rule
    
    while _browseOr(lhs):
        continue
    
    # then compact all
    # (or (or
    # and
    # (and (and
    # as a single container
    
    while _compactPatterns(lhs):
        continue

    # then add a (initial-fact)
    # before (not or (test pattern
    # if they are first in the a group
    _initialFactNormalization(lhs, MM)
        
    return lhs

            
def _browseOr(Or):
    changed = False
    for (index, inOrPattern) in enumerate(Or.patterns):
        if isinstance(inOrPattern, types.AndPatternCE):
            changed = _swapAndOr(inOrPattern, Or.patterns, index) or changed
        if isinstance(inOrPattern, types.OrPatternCE):
            changed = _browseOr(inOrPattern) or changed
        if isinstance(inOrPattern, types.NotPatternCE):
            changed = _swapNotOr(inOrPattern, Or.patterns, index) or changed
            
    return changed
            
def _swapAndOr(And, AndParent, AndIndex):
    changed = False
    for index, inAndPattern in enumerate(And.patterns):
        if isinstance(inAndPattern, types.OrPatternCE):
            newOrPatterns = []
            for orPattern in inAndPattern.patterns:
                #newOrPatterns = And.patterns[0:index] + [orPattern] + And.patterns[index+1:None]
                newOrPatterns.append(types.AndPatternCE(And.patterns[0:index] + [orPattern] + And.patterns[index+1:None]))
            newOr = types.OrPatternCE(newOrPatterns)
            if isinstance(AndParent, types.NotPatternCE):
                AndParent.pattern = newOr
            elif AndIndex is not None:
                AndParent[AndIndex] = newOr
            else:
                raise MyClipsBugException("Parent of And is not Not and no index is available")
            changed = True
        elif isinstance(inAndPattern, types.AndPatternCE):
            changed = _swapAndOr(inAndPattern, And.patterns, index) or changed
        elif isinstance(inAndPattern, types.NotPatternCE):
            changed = _swapNotOr(inAndPattern, And.patterns, index) or changed
            
        #if changed:
        #    return changed
        
    return changed

def _swapNotOr(Not, NotParent, NotIndex):
    # not arg is a single subpattern
    # it could be another and/or/not or an
    # ordered/template
    # (not (or must be converted to (or (not (not
    # (not (and (or must be converted to (or (not (and
    changed = False
    if isinstance(Not.pattern, types.OrPatternCE):
        # need to start a new browseOr here
        # before make reversions
        while _browseOr(Not.pattern):
            changed = True
            
        # then reverse (not (or with (or (not
        reversedOrArguments = []
        for inOrPattern in Not.pattern.patterns:
            reversedOrArguments.append(types.NotPatternCE(inOrPattern))
        # then replace the main Not arg with the new Or ([Not, Not,..])
        NotParent[NotIndex] = types.OrPatternCE(reversedOrArguments)
        changed = True
        
    elif isinstance(Not.pattern, types.AndPatternCE):
        # if found an (not (and (???
        # status, i need to try to reverse 
        # all (and (or in the  
        changed = _swapAndOr(Not.pattern, Not, None) or changed
        
        
    return changed

    
def _compactPatterns(Combiner):
    """
    Remove useless patterns container
    like ( Or ( Or )) or ( And ( And ))
    """
    changed = False
    restart = True
    while restart:
        restart = False
        for index, inCombinerPattern in enumerate(Combiner.patterns):
            # (or (or [] -> (or []
            if isinstance(inCombinerPattern, (types.AndPatternCE, types.OrPatternCE)):
                while _compactPatterns(inCombinerPattern):
                    changed = True
                if inCombinerPattern.__class__ == Combiner.__class__:
                    tmpList = Combiner.patterns
                    tmpList = tmpList[0:index+1] + inCombinerPattern.patterns + tmpList[index+1:None]
                    del tmpList[index]
                    Combiner.patterns = tmpList
                    restart = True
                    changed = True
                    break # force to restart the reduceOrOr with the new list
                
            elif isinstance(inCombinerPattern, types.NotPatternCE):
                if isinstance(inCombinerPattern.pattern, (types.AndPatternCE, types.OrPatternCE)):
                    changed = _compactPatterns(inCombinerPattern.pattern) or changed
                    # it's useless to restart from the begin
                    # just continue 
        
    return changed


def _initialFactNormalization(Combiner, MM):
    """
    Add (initial-fact) pattern before (not or (test if they are first in a group
    """
    
    # check if the first pattern in the list is one 
    # of the right type, otherwise, add a (initial-fact)
    # pattern as first
    if len(Combiner.patterns) and isinstance(Combiner.patterns[0], (types.TestPatternCE, types.NotPatternCE)):
        # first pattern in the group is a test or a not.
        Combiner.patterns.insert(0, _makeInitialFactPattern(MM) )
    
    for inCombinerPattern in Combiner.patterns:
        if isinstance(inCombinerPattern, (types.AndPatternCE, types.OrPatternCE)):
            # go deeper
            _initialFactNormalization(inCombinerPattern, MM)
            
        elif isinstance(inCombinerPattern, types.NotPatternCE):
            if isinstance(inCombinerPattern.pattern, (types.AndPatternCE, types.OrPatternCE)):
                _initialFactNormalization(inCombinerPattern.pattern, MM)
                # it's useless to restart from the begin
                # just continue 
        

def _makeInitialFactPattern(modulesManager):
    return types.TemplatePatternCE('initial-fact', modulesManager)



def normalizeDeclarations(declarations):
    """
    Convert a list of RuleProperty object in a dict
    of RuleProperty.name = RuleProperty.value
    and return it
    if at least one RuleProperty is available,
    otherwise return None
    
    @param declarations: list of rule properties parsed
    @type declasarions: list of RuleProperty
    @return: dict of (RuleProperty.name, RuleProperty.value) or None
    @rtype: dict|None
    """

    return dict([(dec.propertyName, dec.propertyValue) for dec in declarations if isinstance(dec, types.RuleProperty)]) \
            if len(declarations) > 0 \
                else None
    

if __name__ == '__main__':
    
    lhs = [types.AndPatternCE([
                types.OrPatternCE(["A", "B"]),
                types.OrPatternCE(["C", "D",
                    types.AndPatternCE(["Z",
                            types.OrPatternCE(["W", "X"]) 
                        ])
                    ])
        ])]
    
    import pprint
    
    lhs = normalizeLHS(lhs)
    
    pprint.pprint(lhs)
    
    
    