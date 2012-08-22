; verifica che non vengano lasciati riferimenti orfani
; dovuti a collisioni degli hash di token o wme

(defrule r (not (and (A B) (C D))) => )
(assert (A B) (C D))
(retract 2)
(clear)
