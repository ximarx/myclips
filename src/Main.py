from myclips.parser.Parser import Parser
import sys
from myclips.Scope import Scope
from myclips.ModulesManager import ModulesManager
from pyparsing import ParseSyntaxException, ParseFatalException

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
(defglobal modulo
    ?*a* = 2
)
"""

    s2 = r"""

(deffacts MOD::bla
    (A B C)
)

(defrule A::r1
    (declare
        (salience 100))
    ?a <- (A ?a&:(efwohoi 1 2 3) C)
    (template (A 1))
=>
    (printout t ?*a*)
)


"""

    s = s + s2

    #import pprint
    
    MM = ModulesManager()
    MM.addMainScope()
    Scope("MOD", MM)
    Scope("modulo", MM)
    Scope("A", MM)
    MM.changeCurrentScope("MAIN")
    
    try:
    
        [constructs_prettyprint(repr(x)) for x in Parser(modulesManager=MM, debug=False).parse(s)]
        
        for scopeName in MM.getModulesNames():
            print MM.getScope(scopeName)
            
    except Exception, err:
        print Parser.ExceptionPPrint(err, s)