from myclips.rete.WME import WME
from myclips.rete.Token import Token
from myclips.rete.tests.locations import AtomLocation

def getTokenAnchestor(token, tokenRelativeIndex):
    """
    Search a token anchestor from the relative index
    to the current parent
    """
    assert isinstance(token, Token)

    for _ in range(0, tokenRelativeIndex):
        token = token.parent
        
    return token
    
def getWmeFragmentValue(wme, location):
    """
    This function is a proxy for location.toValue(wme)
    THIS FUNCTION IS DEPRECATED
    
    @deprecated: use location.toValue(wme) to get a fragment
        of the wme from a location
    """
    assert isinstance(wme, WME), wme.__class__.__name__
    assert isinstance(location, AtomLocation), location.__class__.__name__
    
    return location.toValue(wme)
    
#    wmeValue = wme.fact
#    
#    if location.fullFact:
#        return wmeValue
#    
#    if location.slotName is not None:
#        wmeValue = wmeValue[location.slotName]
#        
#    if location.fullSlot:
#        return wmeValue
#        
#    if location.isMultiField:
#        wmeValue = wmeValue[location.beginIndex:(location.endIndex if location.endIndex != 0 else None)] 
#    else:
#        if location.fromBegin:
#            wmeValue = wmeValue[location.beginIndex]
#        elif location.fromEnd:
#            wmeValue = wmeValue[location.endIndex - 1]
#
#    return wmeValue
    