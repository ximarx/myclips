
from myclips.rete.Network import Network
from myclips.parser.Parser import Parser
import myclips.parser.Types as types

import logging as _logging

VERSION="0.0-dev"

FORMAT = '[%(levelname).3s %(module)s::%(funcName)s:%(lineno)d] %(message)s'
_logging.basicConfig(format=FORMAT)

logger = _logging.getLogger('myclips')
logger.setLevel(_logging.DEBUG)

# THIS FLAG WILL BE USEFULL IF
# A STRICT_MODE WILL BE AVAILABLE 
STRICT_MODE=False

def newInstance_fromCanonicalClassname(qclass, constrParams=None):
    
    if constrParams == None:
        constrParams = []
    
    lastdot = qclass.rfind('.')
    modulename = qclass[0:lastdot]
    classname = qclass[lastdot + 1:]
    
    return newInstance(classname, constrParams, modulename)
    
    #__import__('icse.ps.constraints.OrChain')
    #chain2 = globals()['OrChain']()
    
def newInstance(classname, constrParams=None, modulename=None):
    
    if constrParams == None:
        constrParams = []
    
    
    if modulename != None:
        imported = __import__(modulename, globals(), locals(), [classname], -1)
        attr = getattr(imported, classname)
        #print "creo: "+classname+" con ",constrParams
        if isinstance(constrParams, list):
            return attr(*constrParams)
        elif isinstance(constrParams, dict):
            return attr(**constrParams)
        else:
            return attr()
    else:
        if isinstance(constrParams, list):
            return globals()[classname](*constrParams)
        elif isinstance(constrParams, dict):
            return globals()[classname](**constrParams)
        else:
            return globals()[classname]()

def importPath(fullpath):
    '''
    Importa un modulo da qualsiasi percorso (fullpath) deve essere
    un percorso assoluto. Con percorsi relativi gli effetti
    potrebbero essere "interessanti" :)
    Una volta caricato il modulo, la path viene rimossa dalla sourcepath
    '''
    import sys
    import os
    path, filename = os.path.split(fullpath)
    filename, _ = os.path.splitext(filename)
    sys.path.insert(0, path)
    module = __import__(filename)
    reload(module) # Might be out of date
    del sys.path[0]
    return module

