
from myclips.rete.Network import Network
from myclips.parser.Parser import Parser
import myclips.parser.Types as types


import logging as _logging

FORMAT = '[%(levelname).3s %(module)s::%(funcName)s:%(lineno)d] %(message)s'
_logging.basicConfig(format=FORMAT)

logger = _logging.getLogger('myclips')
logger.setLevel(_logging.DEBUG)

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


def main():
    t = """
    (deffacts df 
        (A B C D)) 
    (defrule r 
        (A B C D) 
        => 
        (printout t "blablabl" crlf)
        (assert (D C B A))
    )
    (defrule r2
        ?f <- (D C B A)
        =>
        (printout t "Trovato: " ?f crlf)
    )
    """
    n = Network()
    try:
        parsed = n.getParser().parse(t, True)
    except Exception, e:
        print n.getParser().ExceptionPPrint(e, t)
    else:
        n.addDeffacts(parsed[0])
        n.addRule(parsed[1])
        n.addRule(parsed[2])
        print n.facts
        print n.reset()
        print n.facts
        for (salience, pnode, token) in n.agenda.activations():
            print "%-6d %s: %s"%(salience, pnode.mainRuleName, token)
    
        return n

if __name__ == '__main__':
    main()

