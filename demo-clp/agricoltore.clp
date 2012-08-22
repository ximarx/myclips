(deftemplate configurazione "Stato del gioco"
	(slot agricoltore (type STRING) 
			     (default "sulla-riva-vicina"))
	(slot cavolo      (type STRING)
			     (default "sulla-riva-vicina"))
	(slot pecora      (type STRING) 
			     (default "sulla-riva-vicina"))
	(slot lupo        (type STRING) 
			     (default "sulla-riva-vicina")))

(deftemplate inizia "Configurazione iniziale"
	(slot config_iniziale  (type SYMBOL) 
				(default ACPL))) 


(defrule regola1 
   ?indice_conf1 <- 
   (configurazione  (agricoltore  "sulla-riva-vicina") 
 	       	(cavolo       "sulla-riva-vicina")
			(pecora       "sulla-riva-vicina")
			(lupo         "sulla-riva-vicina"))
  =>
(printout t "Trasborda la pecora" crlf)
(retract ?indice_conf1)
(assert(configurazione(agricoltore "sulla-riva-lontana") 
       		      (cavolo      "sulla-riva-vicina")
			      (pecora      "sulla-riva-lontana")
			      (lupo        "sulla-riva-vicina"))))


(defrule regola2 
   ?indice_conf2 <- 
   (configurazione  (agricoltore  "sulla-riva-lontana") 
 	       	(cavolo       "sulla-riva-vicina")
			(pecora       "sulla-riva-lontana")
			(lupo         "sulla-riva-vicina"))
  =>
(printout t "Ritorna alla riva vicina" crlf)
(retract ?indice_conf2)
(assert(configurazione(agricoltore "sulla-riva-vicina") 
       		      (cavolo      "sulla-riva-vicina")
			      (pecora      "sulla-riva-lontana")
			      (lupo        "sulla-riva-vicina"))))


(defrule regola3 
   ?indice_conf3 <- 
   (configurazione  (agricoltore  "sulla-riva-vicina") 
 	       	(cavolo       "sulla-riva-vicina")
			(pecora       "sulla-riva-lontana")
			(lupo         "sulla-riva-vicina"))
  =>
(printout t "Trasborda il lupo" crlf)
(retract ?indice_conf3)
(assert(configurazione(agricoltore "sulla-riva-lontana") 
       		      (cavolo      "sulla-riva-vicina")
			      (pecora      "sulla-riva-lontana")
			      (lupo        "sulla-riva-lontana"))))

(defrule regola4 
   ?indice_conf4 <- 
   (configurazione  (agricoltore  "sulla-riva-vicina") 
 	       	(cavolo       "sulla-riva-vicina")
			(pecora       "sulla-riva-lontana")
			(lupo         "sulla-riva-vicina"))
  =>
(printout t "Trasborda il cavolo" crlf)
(retract ?indice_conf4)
(assert(configurazione(agricoltore "sulla-riva-lontana") 
       		      (cavolo      "sulla-riva-lontana")
			      (pecora      "sulla-riva-lontana")
			      (lupo        "sulla-riva-vicina"))))


(defrule regola5 
   ?indice_conf5 <- 
   (configurazione  (agricoltore  "sulla-riva-lontana") 
 	       	(cavolo       "sulla-riva-vicina")
			(pecora       "sulla-riva-lontana")
			(lupo         "sulla-riva-lontana"))
  =>
(printout t "Riporta indietro la pecora" crlf)
(retract ?indice_conf5)
(assert(configurazione(agricoltore "sulla-riva-vicina") 
       		      (cavolo      "sulla-riva-vicina")
			      (pecora      "sulla-riva-vicina")
			      (lupo        "sulla-riva-lontana"))))


(defrule regola6 
   ?indice_conf6 <- 
   (configurazione  (agricoltore  "sulla-riva-lontana") 
 	       	(cavolo       "sulla-riva-lontana")
			(pecora       "sulla-riva-lontana")
			(lupo         "sulla-riva-vicina"))
  =>
(printout t "Riporta indietro la pecora" crlf)
(retract ?indice_conf6)
(assert(configurazione(agricoltore "sulla-riva-vicina") 
       		      (cavolo      "sulla-riva-lontana")
			      (pecora      "sulla-riva-vicina")
			      (lupo        "sulla-riva-vicina"))))


(defrule regola7 
   ?indice_conf7 <- 
   (configurazione  (agricoltore  "sulla-riva-vicina") 
 	       	(cavolo       "sulla-riva-vicina")
			(pecora       "sulla-riva-vicina")
			(lupo         "sulla-riva-lontana"))
  =>
(printout t "Trasborda il cavolo" crlf)
(retract ?indice_conf7)
(assert(configurazione(agricoltore "sulla-riva-lontana") 
       		      (cavolo      "sulla-riva-lontana")
			      (pecora      "sulla-riva-vicina")
			      (lupo        "sulla-riva-lontana"))))


(defrule regola8 
   ?indice_conf8 <- 
   (configurazione  (agricoltore  "sulla-riva-vicina") 
 	       	(cavolo       "sulla-riva-lontana")
			(pecora       "sulla-riva-vicina")
			(lupo         "sulla-riva-vicina"))
  =>
(printout t "Trasborda il lupo" crlf)
(retract ?indice_conf8)
(assert(configurazione(agricoltore "sulla-riva-lontana") 
       		      (cavolo      "sulla-riva-lontana")
			      (pecora      "sulla-riva-vicina")
			      (lupo        "sulla-riva-lontana"))))


(defrule regola9 
   ?indice_conf9 <- 
   (configurazione  (agricoltore  "sulla-riva-lontana") 
 	       	(cavolo       "sulla-riva-lontana")
			(pecora       "sulla-riva-vicina")
			(lupo         "sulla-riva-lontana"))
  =>
(printout t "Ritorna alla riva vicina" crlf)
(retract ?indice_conf9)
(assert(configurazione(agricoltore "sulla-riva-vicina") 
       		      (cavolo      "sulla-riva-lontana")
			      (pecora      "sulla-riva-vicina")
			      (lupo        "sulla-riva-lontana"))))


(defrule regola10 
   ?indice_conf10 <- 
   (configurazione  (agricoltore  "sulla-riva-vicina") 
 	       	(cavolo       "sulla-riva-lontana")
			(pecora       "sulla-riva-vicina")
			(lupo         "sulla-riva-lontana"))
  =>
(printout t "Trasborda la pecora" crlf)
(retract ?indice_conf10)
(assert(configurazione(agricoltore "sulla-riva-lontana") 
       		      (cavolo      "sulla-riva-lontana")
			      (pecora      "sulla-riva-lontana")
			      (lupo        "sulla-riva-lontana"))))


(defrule chiedi_configurazione_iniziale
	(declare (salience 10000))
 =>
(printout t crlf"**************************" crlf crlf
           "Inserisci la configurazione iniziale:" crlf crlf)
(printout t "L'agricoltore e' sulla riva vicina? (S/N): ")
(bind ?agric (read)) 
(if (eq ?agric S) then (bind ?temp_a A) else (bind ?temp_a _))
(printout t "Il cavolo e' sulla riva vicina?     (S/N): ")
(bind ?cav (read))
(if (eq ?cav S) then (bind ?temp_c C) else (bind ?temp_c _))
(printout t "La pecora e' sulla riva vicina?     (S/N): ")
(bind ?pec (read))
(if (eq ?pec S) then (bind ?temp_p P) else (bind ?temp_p _))
(printout t "Il lupo e' sulla riva vicina?       (S/N): ")
(bind ?lup (read))
(if (eq ?lup S) then (bind ?temp_l L) else (bind ?temp_l _))
(bind ?config (sym-cat ?temp_a ?temp_c ?temp_p ?temp_l))
(assert (inizia (config_iniziale ?config)))
(assert (config inesatta))
(printout t crlf crlf))

;controllo definizione di input
(defrule controlla_input
	(declare (salience 9000))
	?indice <- (inizia (config_iniziale ?conf_iniz))
	(stato ?conf_iniz)
	?ind <- (config inesatta)
=>
	(retract ?indice ?ind)
	(assert (config esatta))
	(if (eq ?conf_iniz ACPL)
		then (assert (configurazione))
		else (if (eq ?conf_iniz ____) then
			(assert (configurazione(agricoltore "sulla-riva-lontana")
				(cavolo "sulla-riva-lontana")
				(pecora "sulla-riva-lontana")
				(lupo "sulla-riva-lontana"))))
		else (if (eq ?conf_iniz A_P_) then
			(assert (configurazione(agricoltore "sulla-riva-vicina")
				(cavolo "sulla-riva-lontana")
				(pecora "sulla-riva-vicina")
				(lupo "sulla-riva-lontana"))))
		else (if (eq ?conf_iniz _C_L) then
			(assert (configurazione(agricoltore "sulla-riva-lontana")
				(cavolo "sulla-riva-vicina")
				(pecora "sulla-riva-lontana")
				(lupo "sulla-riva-vicina"))))
		else (if (eq ?conf_iniz A_PL) then
			(assert (configurazione(agricoltore "sulla-riva-vicina")
				(cavolo "sulla-riva-lontana")
				(pecora "sulla-riva-vicina")
				(lupo "sulla-riva-vicina"))))
		else (if (eq ?conf_iniz _C__) then
			(assert (configurazione(agricoltore "sulla-riva-lontana")
				(cavolo "sulla-riva-vicina")
				(pecora "sulla-riva-lontana")
				(lupo "sulla-riva-lontana"))))
		else (if (eq ?conf_iniz AC_L) then
			(assert (configurazione(agricoltore "sulla-riva-vicina")
				(cavolo "sulla-riva-vicina")
				(pecora "sulla-riva-lontana")
				(lupo "sulla-riva-vicina"))))
		else (if (eq ?conf_iniz ___L) then
			(assert (configurazione(agricoltore "sulla-riva-lontana")
				(cavolo "sulla-riva-lontana")
				(pecora "sulla-riva-lontana")
				(lupo "sulla-riva-vicina"))))
		else (if (eq ?conf_iniz ACP_) then
			(assert (configurazione(agricoltore "sulla-riva-vicina")
				(cavolo "sulla-riva-vicina")
				(pecora "sulla-riva-vicina")
				(lupo "sulla-riva-lontana"))))
		else (if (eq ?conf_iniz __P_) then
			(assert (configurazione(agricoltore "sulla-riva-lontana")
				(cavolo "sulla-riva-lontana")
				(pecora "sulla-riva-vicina")
				(lupo "sulla-riva-lontana"))))
		)
(printout t "Le mosse dell'agricoltore sono: " crlf crlf))



(defrule ritenta "Se la configurazione data in input e' errata"
  (declare (salience 8500))
  ?indice <- (config inesatta)	
 =>
  (retract ?indice)
  (printout t crlf "La configurazione iniziale data in input 				risulta illegale!!!" crlf crlf crlf)
  (printout t "Vuoi riprovare? (S/N): ")
  (bind ?risposta (read))
  (if (eq ?risposta S) then (reset) 
	else (printout t crlf crlf"**************" crlf crlf)))


(defrule continua_gioco "L'utente vuole giocare ancora?"
  (declare (salience -10000))
  ?indice <- (config esatta)
 =>
  (retract ?indice)
  (printout t crlf crlf crlf "Vuoi giocare ancora? (S/N): ")
  (bind ?risposta(read))
  (if (eq ?risposta S) then (reset)
  	else (printout t crlf "******************" crlf crlf)))



(deffacts stati_legali  "Stati validi nel gioco"
(stato  ACPL)  ; Tutti i personaggi sono sulla riva 1 (stato  ____)  ; Tutti i personaggi sono sulla riva 2
(stato  A_P_)  ; Agricoltore e pecora sulla riva 1 
		     ; Cavolo e Lupo sulla riva 2 	
(stato  _C_L)  ; Cavolo e Lupo sulla riva 1
		     ; Agricoltore e pecora sulla riva 2
(stato  A_PL)  ;...
(stato  _C__)
(stato  AC_L)
(stato  ___L)
(stato  ACP_)
(stato  __P_))

 
