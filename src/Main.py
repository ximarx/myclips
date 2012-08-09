from myclips.parser.Parser import Parser
import sys
from myclips.ModulesManager import ModulesManager
from myclips.parser.Types import ParsedType
import myclips
from myclips.functions.Function import FunctionInternalError, HaltException
import traceback
from myclips.Agenda import AgendaNoMoreActivationError

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
    
    if True:
        try:
            n = myclips.main()
            while True:
                try:
                    pnode, token = n.agenda.getActivation()
                    pnode.execute(token)
                    print '-----', pnode.mainRuleName
                    for (salience, pnode, token) in n.agenda.activations():
                        print "%-6d %s: %s"%(salience, pnode.mainRuleName, token)
                    print '---------'
                    
                except AgendaNoMoreActivationError:
                    try:
                        # try to pop the focusStack
                        n.agenda.focusStack.pop()
                    except IndexError:
                        # pop from an empty stack
                        break
            
        except FunctionInternalError, e:
            print e.args[2]
            raise
        except HaltException, e:
            print "HAAAAAALT!!" 
    
        exit()
    
    s = r"""
    
(defmodule A
    (export ?ALL))

(deffunction A::funzione (?A)
    (printout t ?A)
)

(deftemplate A::template
    (slot A)
    (slot B)
    (multislot C)
)

(defmodule BC
    (export ?ALL))

(deftemplate BC::rule
    (multislot if)
    (multislot then))

(deftemplate BC::attribute
   (slot name)
   (slot value))

(deftemplate BC::goal
   (slot attribute))

(defmodule USEBC
    (import BC ?ALL))

(deffacts USEBC::wine-rules
   (rule (if main-course is red-meat)
         (then best-color is red))

   (rule (if main-course is fish)
         (then best-color is white))

   (rule (if main-course is poultry and
             meal-is-turkey is yes)
         (then best-color is red))

   (rule (if main-course is poultry and
             meal-is-turkey is no)
         (then best-color is white)))

(deffacts USEBC::initial-goal
   (goal (attribute best-color))
   (A B C)
)
   
(defrule A::regola
    (template (A 1) (B 2) (C $?c1s3))
    ?c2 <- (template (A ?))
    (A 2 c 4)
=>
    (printout t ?c2 crlf)
    (modify ?c2 (A 100))
)

(defrule A::r 
    (A B C D) 
    => 
    (printout t "blablabl" crlf)
    (assert (D C B A))
    (assert (template (A 10)))
    (loop-for-count (?var 1 5) (printout t ?var crlf))
)



"""


    MM = ModulesManager()
    MM.addMainScope()
    
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
        