from myclips.parser.Parser import Parser
from myclips.parser.Functions import _SampleFunctionsInit


if __name__ == '__main__':
    
    s = r"""
(deftemplate template "un commento"
    (slot s1)
    (multislot s2)
)

"""

    s2 = r"""
(defrule r1
    (template 
        (s1 1)
        (s2 1 2 3)
    )
=>
)
"""

    s += s2

    import pprint
    
    _SampleFunctionsInit()
    
    pprint.pprint(Parser().parse(s))