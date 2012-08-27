from myclips.parser.Parser import Parser
import sys
from myclips.ModulesManager import ModulesManager
from myclips.parser.Types import ParsedType
import myclips
from myclips.functions.Function import FunctionInternalError, HaltException
import traceback
from myclips.Agenda import AgendaNoMoreActivationError
from myclips.rete.Network import Network
from myclips.listeners.NetworkBuildPrinter import NetworkBuildPrinter

def constructs_prettyprint(constr_string, INDENT=0):
    output = sys.stdout
    c_i = 0
    while c_i < len(constr_string):
        c = constr_string[c_i]
        if c == "<":
            output.write("\n"+"".ljust(INDENT, "\t") + c)
            INDENT += 1
        elif c == ">":
            INDENT -= 1
            output.write(c+"\n"+"".ljust(INDENT, "\t"))
        else:
            output.write(c)
        c_i += 1
        

if __name__ == '__main__':
    
    s = r"""
    
(deftemplate possible (slot value) (slot group) (slot id))
(deftemplate impossible (slot value) (slot rank) (slot id))
(deftemplate rank (slot value) (slot process))
(deftemplate technique (slot name) (slot rank))
    
(defrule naked-single-group
   
   (phase match)

   (rank (value ?p) (process yes))

   (technique (name Naked-Single) (rank ?p))
   
   (possible (value ?v) (group ?g) (id ?id))
   
   (not (possible (value ~?v) (group ?g) (id ?id)))
   
   (possible (value ?v) (group ?g) (id ?id2&~?id))
   
   (not (impossible (id ?id2) (value ?v) (rank ?p)))
   
   =>
   )
   
(defrule r
    => (draw-circuit naked-single-group))
   
"""


    MM = ModulesManager()
    MM.addMainScope()
    
    try:
    
        parsed = Parser(modulesManager=MM, debug=False).parse(s)
    
        [constructs_prettyprint(repr(x)) for x in parsed if isinstance(x, ParsedType)]
            
    except Exception, err:
        try:
            print Parser.ExceptionPPrint(err, s)
        except:
            # raise the original exception,
            # pretty printer failed
            raise err
#    finally:
#        for scopeName in MM.getModulesNames():
#            print MM.getScope(scopeName)
        
    n = Network(modulesManager=MM)
    
    NetworkBuildPrinter(sys.stdout).install(n.eventsManager)
        
    for p in parsed:
        
        if p.__class__.__name__ == 'DefRuleConstruct':
            
            n.addRule(p)
            
    n.run(1)
            
        