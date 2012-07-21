from myclips.parser.Parser import Parser
import sys
from myclips.Scope import Scope, ScopeImport, ScopeExport
from myclips.ModulesManager import ModulesManager
from myclips.parser.Types import ParsedType

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
    
(defmodule MOD
    (export defglobal b))

(defglobal MOD
    ?*b* = 2
)

(deffacts MOD::bla
    (A B C)
)

(defmodule A
    (import MOD defglobal b))
    
(defglobal A
    ?*a* = 2
)

(deftemplate A::template 
    (slot A (type INTEGER)))

(defrule A::r1
    (declare
        (salience 100))
    ?a <- (A ?a&:(+ 1 2 3) C)
    (template (A 1))
=>
    (printout t ?*a* ?*b*)
)


"""


    MM = ModulesManager()
    MM.addMainScope()
    #Scope("MOD", MM, exports=[ScopeExport(Scope.PROMISE_TYPE_GLOBAL, Scope.PROMISE_NAME_ALL)])
    #Scope("A", MM, imports=[ScopeImport("MOD", Scope.PROMISE_TYPE_GLOBAL, Scope.PROMISE_NAME_ALL)])
    #MM.changeCurrentScope("MAIN")
    
    try:
    
        [constructs_prettyprint(repr(x)) for x in Parser(modulesManager=MM, debug=False).parse(s) if isinstance(x, ParsedType)]
            
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
        