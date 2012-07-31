import logging

FORMAT = '[%(levelname).3s %(module)s::%(funcName)s:%(lineno)d] %(message)s'
logging.basicConfig(format=FORMAT)

logger = logging.getLogger('myclips')
logger.setLevel(logging.DEBUG)

#
#logger.debug("Logger enabled")
#logger.info("Logger enabled")
#logger.warn("Logger enabled")
#logger.error("Logger enabled")
#logger.critical("Logger enabled")

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

