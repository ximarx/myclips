from myclips.parser.Parser import Parser
import sys
from myclips.ModulesManager import ModulesManager
from myclips.parser.Types import ParsedType
import myclips
from myclips.functions.Function import FunctionInternalError, HaltException
import traceback
from myclips.Agenda import AgendaNoMoreActivationError
from myclips.rete.Network import Network

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
    
(defrule r 
    (A B|s C)
=>
)

"""


    MM = ModulesManager()
    MM.addMainScope()
    
    parsed = Parser(modulesManager=MM, debug=False).parse(s)
    
    try:
    
        [constructs_prettyprint(repr(x)) for x in parsed if isinstance(x, ParsedType)]
            
    except Exception, err:
        try:
            print Parser.ExceptionPPrint(err, s)
        except:
            # raise the original exception,
            # pretty printer failed
            raise err
    finally:
        for scopeName in MM.getModulesNames():
            print MM.getScope(scopeName)
        
    n = Network(modulesManager=MM)
        
    for p in parsed:
        
        if p.__class__.__name__ == 'DefRuleConstruct':
            
            n.addRule(p)
            
        