

if __name__ == '__main__':
    
    r = r"""
(defrule rulename{0}
    (A B C)
    (D ~E F)
    (G ?h&:(+ ?h 2)|:(eq ?h 4) I)
    (tttttttt 
        (s1 v1) 
        (s2 v2)
    )
    (tttttttt2 
        (s1 ?var&:(+ 1 2)) 
        (s2 1 2 3) 
        (s3 $?ciao) 
        (s4 $?) 
        (s5 ?)
    )
    => 
)
"""

    t = """
(deftemplate tttttttt
    (slot s1 (default ?NONE))
    (multislot s2 (default ?NONE))
    (multislot s3 (default ?NONE))
    (multislot s4 (default ?NONE))
    (slot s5 (default ?NONE))
)
(deftemplate tttttttt2
    (slot s1 (default ?NONE))
    (multislot s2 (default ?NONE))
    (multislot s3 (default ?NONE))
    (multislot s4 (default ?NONE))
    (slot s5 (default ?NONE))
)
"""

    f = open("../clips-500-rules-test.clp", "w")
    
    f.write(t)
    for i in range(0,500):
        f.write(r.format(i))
        
    f.close()
