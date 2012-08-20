'''
Created on 27/lug/2012

@author: Francesco Capozzo
'''

import myclips.parser.Types as types
from myclips.rete.tests.locations import VariableLocation, VariableReference
from myclips.MyClipsException import MyClipsBugException, MyClipsException
import myclips
from copy import copy, deepcopy

def getVar(varName, variables, inPatternVariables):
    if variables.has_key(varName):
        return variables[varName]
    
    for prevVar in inPatternVariables:
        if prevVar.name == varName:
            return prevVar
    
    return False


def analyzeSequence(sequence, variables):
    
    inPatternVariables = []
    inPatternReferences = []

    prevMultifieldCount = 0
    
    for (fIndex, field) in enumerate(sequence):
        
        field, isNegative, connectedConstraints = normalizeAtom(field)
        if len(connectedConstraints) > 0:
            myclips.logger.error("FIXME: Connected contraints ignored in sequence analysis: %s", connectedConstraints)
        
        varLocation = None
        
        if isinstance(field, (types.SingleFieldVariable, types.BaseParsedType, types.UnnamedSingleFieldVariable)):
            # ignora tutte le cose non "variabili" nell'analisi
            # ma il fatto che abbia trovato un elemento di lunghezza
            # conosciuta dopo ad un eventuale multifield
            # mi dice che il multifield nn si puo estendere oltre una
            # certa lunghezza.
            # aggiorno tutte le variabili precedenti con questa informazione
            for var in inPatternVariables:
                if var.fromEnd:
                    var.endIndex += 1

            for var in inPatternReferences:
                if var.fromEnd:
                    var.endIndex += 1
        
        if isinstance(field, types.SingleFieldVariable) and not isinstance(field, types.UnnamedSingleFieldVariable):
            # ho trovato una variabile
            # controllo se ce l'ho gia
                
            # nuova occorrenza
            varLocation = VariableLocation(field.evaluate())
            varLocation.isMultifield = False
            
            varLocation.beginIndex = fIndex
            varLocation.endIndex = 0
            
            varLocation.fromBegin = (prevMultifieldCount == 0)
            varLocation.fromEnd = (prevMultifieldCount > 0)

            
        elif isinstance(field, types.MultiFieldVariable):
            
            if not isinstance(field, types.UnnamedMultiFieldVariable):
                
                # nuova occorrenza
                varLocation = VariableLocation(field.evaluate())
                #varLocation.patternIndex = index
                varLocation.isMultiField = True
                
                varLocation.beginIndex = fIndex
                varLocation.endIndex = 0
                
                varLocation.fromBegin = (prevMultifieldCount == 0)
                varLocation.fromEnd = (prevMultifieldCount > 0)

            # DOPO AVER CREATO LA VARIABILE
            # AGGIORNO IL CONTATORE
            prevMultifieldCount += 1
            
                
        if varLocation is not None: 
            mainDefinition = getVar(varLocation.name, variables, inPatternVariables)
            if not mainDefinition:
                inPatternVariables.append(varLocation)
                
            else:
                # convert the variable location, in a variable reference
                varReference = VariableReference()
                varLocation.toVarReference(varReference)
                varReference.reference = mainDefinition
                varReference.isNegative = isNegative
                inPatternReferences.append(varReference)
    
    for var in inPatternVariables:
        if not var.fromBegin:
            var.fromBegin = None
            var.beginIndex = None
        elif not var.fromEnd:
            var.fromEnd = None
            var.endIndex = None

    for var in inPatternReferences:
        if not var.fromBegin:
            var.fromBegin = None
            var.beginIndex = None
        elif not var.fromEnd:
            var.fromEnd = None
            var.endIndex = None

    
    return (inPatternVariables, inPatternReferences)
    

def VariableAnalysis(thePatterns, variables = None, joinConstraints = None, indexPrefix = 0):
    variables = {} if variables is None else variables
    joinConstraints = [] if joinConstraints is None else joinConstraints
    for (index, thePattern) in enumerate(thePatterns):
        inPatternVariables = []
        inPatternReferences = []
        index += indexPrefix

        if isinstance(thePattern, types.AssignedPatternCE):
        
            if not not getVar(thePattern.variable.evaluate(), variables, []):
                raise MyClipsBugException("Assigned variable in assigned-pattern-CE can't be a reference")
            
            varLocation = VariableLocation()
            varLocation.name = thePattern.variable.evaluate()
            varLocation.patternIndex = index
            inPatternVariables.append(varLocation)
            
            thePattern = thePattern.pattern
        
        if isinstance(thePattern, types.OrderedPatternCE):
        
            (inPatternVariables, inPatternReferences) = analyzeSequence(thePattern.constraints, variables)
        
        if isinstance(thePattern, types.TemplatePatternCE):
            for slot in thePattern.templateSlots:
                if isinstance(slot, types.SingleFieldLhsSlot):
                    if isinstance(slot.slotValue, types.SingleFieldVariable):
                        varLocation = VariableLocation(slot.slotValue.evaluate())
                        varLocation.slotName = slot.slotName
                        varLocation.patternIndex = index
                        mainReference = getVar(slot.slotValue.evaluate(), variables, inPatternVariables)
                        if not mainReference:
                            inPatternVariables.append(varLocation)
                        else:
                            varReference = varLocation.toVarReference()
                            varReference.reference = mainReference
                            inPatternReferences.append(varReference)
                            
                else:
                    (inPatternVariables, inPatternReferences) = analyzeSequence(slot.slotValue, variables)
                    for var in inPatternVariables:
                        var.patternIndex = index
                        var.slot = slot.slotName
                    for var in inPatternReferences:
                        var.patternIndex = index
                        var.slot = slot.slotName
                
        # set patternIndex to variables and references
        for var in inPatternVariables:
            var.patternIndex = index

        for var in inPatternReferences:
            var.relPatternIndex = var.reference.patternIndex - index
                    
        variables.update(dict([(var.name, var) for var in inPatternVariables]))
        joinConstraints.append(inPatternReferences)
        
    return (variables, joinConstraints)

def normalizeAtom(atom):
    
    isNegative = False
    connected = []
    while not isinstance(atom, (types.Variable, types.BaseParsedType, types.FunctionCall)):
        if isinstance(atom, types.ConnectedConstraint):
            atom = atom.constraint
            connected = atom.connectedConstraints
        
        elif isinstance(atom, types.Constraint):
            atom = atom.constraint
            
        elif isinstance(atom, types.PositiveTerm):
            atom = atom.term
            
        elif isinstance(atom, types.NegativeTerm):
            atom = atom.term
            isNegative = True
    
    return (atom, isNegative, connected)

def analyzePattern(thePattern, patternIndex, variables):
    inPatternReferences = []
    inPatternVariables = []

    if isinstance(thePattern, types.OrderedPatternCE):
    
        (inPatternVariables, inPatternReferences) = analyzeSequence(thePattern.constraints, variables)
    
    if isinstance(thePattern, types.TemplatePatternCE):
        for slot in thePattern.templateSlots:
            if isinstance(slot, types.SingleFieldLhsSlot):
                
                # normalize to basetype or variable
                slotValue, isNegative, connectedConstraints = normalizeAtom(slot.slotValue)
                if len(connectedConstraints) > 0:
                    myclips.logger.error("FIXME: Connected contraints ignored in pattern analysis: %s", connectedConstraints)
                
                if isinstance(slotValue, types.SingleFieldVariable):
                    varLocation = VariableLocation(slotValue.evaluate())
                    varLocation.slotName = slot.slotName
                    varLocation.fullSlot = True
                    mainReference = getVar(slotValue.evaluate(), variables, inPatternVariables)
                    if not mainReference:
                        inPatternVariables.append(varLocation)
                    else:
                        varReference = VariableReference()
                        varLocation.toVarReference(varReference)
                        varReference.reference = mainReference
                        varReference.isNegative = isNegative
                        inPatternReferences.append(varReference)
                        
            else:
                (inPatternVariables, inPatternReferences) = analyzeSequence(slot.slotValue, variables)
                for var in inPatternVariables:
                    var.slotName = slot.slotName
                for var in inPatternReferences:
                    var.slotName = slot.slotName

    for var in inPatternVariables:
        var.patternIndex = patternIndex

    for var in inPatternReferences:
        var.relPatternIndex = var.reference.patternIndex - patternIndex

    return (inPatternVariables, inPatternReferences)

def analyzeFunction(theFunction, patternIndex, variables, fakeVariables = None, realToFakeMap = None, vIndex = None):
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
    
    aNewFunctionCallArgs = []
    fakeVariables = fakeVariables or {}
    realToFakeMap = realToFakeMap or {}
    vIndex = vIndex or 0;
    
    if isinstance(theFunction, types.FunctionCall):
        
        assert isinstance(theFunction, types.FunctionCall)
        
        for aArg in theFunction.funcArgs:
            
            # globals are resolved at function-call execution time
            if isinstance(aArg, (types.SingleFieldVariable, types.MultiFieldVariable)):
                # i've already created a fake_var for this var?
                if not realToFakeMap.has_key(aArg.evaluate()) :
                
                    # where i found the variable first?
                    mainReference = getVar(aArg.evaluate(), variables, [])
                    
                    if mainReference is False:
                        raise MyClipsException("Variable %s found in the expression %s was referenced in CE #%d before being defined."%(
                                aArg.evaluate(),
                                theFunction.toClipsStr(),
                                patternIndex
                            ))
                    
                    varReference = VariableReference()
                    varReference.reference = mainReference
                    varReference.relPatternIndex = mainReference.patternIndex - patternIndex
                    
                    theFakeName = "%"+str(vIndex)
                    vIndex += 1
                    
                    theFakeVar = aArg.__class__(types.Symbol(theFakeName)) 
                    
                    fakeVariables[theFakeVar.evaluate()] = varReference
                    realToFakeMap[aArg.evaluate()] = theFakeVar.evaluate()
                
                else:
                    theFakeVar = fakeVariables[realToFakeMap[aArg.evaluate()]]
                     
                
                # replace the variable name with a fake name
                #aArg.content = theFakeName
                aNewFunctionCallArgs.append(theFakeVar)
                
            elif isinstance(aArg, types.FunctionCall):
                
                # recursion: replace arguments inside the function call
                # fakeReferences are ignored because the dict is automatically
                # updated by the recursion.
                aInnerNewFunctionCall, _ = analyzeFunction(aArg, patternIndex, variables, fakeVariables, realToFakeMap, vIndex)
                
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

def normalizeLHS(lhs):
    """
    Change patterns orders (and nested patterns order)
    to normalize lhs in a Or (And ( normal form
    with all nested Or regrouped in a single
    top level Or
    """
    if isinstance(lhs, list):
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
    
    