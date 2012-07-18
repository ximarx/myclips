from myclips.parser.Parser import Parser
from myclips.parser.Functions import _SampleFunctionsInit
import sys

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
(deftemplate template "un commento"
    (slot s1 (type INTEGER SYMBOL))
    (multislot s2 (type NUMBER SYMBOL ?VARIABLE))
    (slot s3 (type INTEGER))
)

"""

    s2 = r"""
(defrule r1
    (declare
        (salience 100))
    (A B|D C)
    (template 
        (s1 1|c|=(+ 1 (+ 3 4)))
        (s2 1 =(eq ciao bubu))
        (s3 ?var&~2))
=>
)
"""

    s += s2

    #import pprint
    
    _SampleFunctionsInit()
    
    [constructs_prettyprint(repr(x)) for x in Parser().parse(s)]