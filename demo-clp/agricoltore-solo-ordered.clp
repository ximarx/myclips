
(defrule mostra-goal "Mostra il goal"
	(declare (salience 1000))
	?f1 <- (su-riva agricoltore lontana)
	?f2 <- (su-riva pecora lontana)
	?f3 <- (su-riva lupo lontana)
	?f4 <- (su-riva cavolo lontana)
=>
	(printout t "Hai raggiunto il goal!!!" crlf)
	(retract ?f1 ?f2 ?f3 ?f4)
)

(defrule torna-agricoltore-solo "Sposta l'agricoltore dalla sponda lontana a quella vicina"
	?agricoltore <- (su-riva agricoltore lontana)
	(not (and
			(su-riva pecora lontana)
			(su-riva cavolo lontana)
			(su-riva lupo vicina)
		)
	)
	(not (and
			(su-riva lupo lontana)
			(su-riva pecora lontana)
			(su-riva cavolo vicina)
		)
	)
=>
	(printout t "Sposto agricoltore vicino" crlf)
	(retract ?agricoltore)
	(assert (su-riva agricoltore vicina))
)

(defrule torna-agricoltore-con-pecora-se-lupo-lontano "Sposta l'agricoltore e la pecora dalla sponda lontana a quella vicina se il lupo e' lontano"
	?agricoltore <- (su-riva agricoltore lontana)
	?pecora <- (su-riva pecora lontana)
	(su-riva lupo lontana)
	(su-riva ? vicina)
=>	
	(printout t "Sposto agricoltore e pecora vicino" crlf)
	(retract ?agricoltore)
	(assert (su-riva agricoltore vicina))
	(retract ?pecora)
	(assert (su-riva pecora vicina))
)



(defrule torna-agricoltore-con-pecora-se-cavolo-lontano "Sposta l'agricoltore e la pecora dalla sponda lontana a quella vicina se il cavolo e' lontano"
	?agricoltore <- (su-riva agricoltore lontana)
	?pecora <- (su-riva pecora lontana)
	(su-riva cavolo lontana)
	(su-riva ? vicina)
=>	
	(printout t "Sposto agricoltore e pecora vicino" crlf)
	(retract ?agricoltore)
	(assert (su-riva agricoltore vicina))
	(retract ?pecora)
	(assert (su-riva pecora vicina))
)
		 
(defrule manda-pecora-iniziale "Sposta la pecora e l'agricoltore dalla sponda vicina a quella lontana (lasciando lupo e cavolo sulla sponda vicina)"
	?agricoltore <- (su-riva agricoltore vicina)
	?pecora <- (su-riva pecora vicina)
	(su-riva lupo vicina)
	(su-riva cavolo vicina)
=>
	(printout t "Sposto agricoltore e pecora lontano" crlf)
	(retract ?agricoltore)
	(assert (su-riva agricoltore lontana))
	(retract ?pecora)
	(assert (su-riva pecora lontana))
)


(defrule manda-lupo "Sposta l'agricoltore ed il lupo dalla sponda vicina a quella lontana" 
	?agricoltore <- (su-riva agricoltore vicina)
	?lupo <- (su-riva lupo vicina)
	(su-riva pecora lontana)
	(su-riva cavolo vicina)
=>
	(printout t "Sposto agricoltore e lupo lontano" crlf)
	(retract ?agricoltore)
	(assert (su-riva agricoltore lontana))
	(retract ?lupo)
	(assert (su-riva lupo lontana))
)

(defrule manda-cavolo "Sposta l'agricoltore ed il cavolo dalla sponda vicina a quella lontana"
	?agricoltore <- (su-riva agricoltore vicina)
	?cavolo <- (su-riva cavolo vicina)
	(su-riva lupo lontana)
=>
	(printout t "Sposto agricoltore e cavolo lontano" crlf)
	(retract ?agricoltore)
	(assert (su-riva agricoltore lontana))
	(retract ?cavolo)
	(assert (su-riva cavolo lontana))
)	


(defrule manda-pecora-finale "Sposta l'agricoltore e la pecora sulla sponda lontana (se lupo e cavolo sono sull'altra sponda)"
	?agricoltore <- (su-riva agricoltore vicina)
	?pecora <- (su-riva pecora vicina)
	(su-riva ?op1 lontana)
	(su-riva ~?op1 lontana)
=>
	(printout t "Sposto agricoltore e pecora lontano" crlf)
	(retract ?agricoltore)
	(retract ?pecora)
	(assert (su-riva agricoltore lontana))
	(assert (su-riva pecora lontana))
)

(defrule manda-agricoltore-solo "Sposta SOLO l'agricoltore dalla sponda distante a quella vicina"
	?agricoltore <- (su-riva agricoltore vicina)
	(not (su-riva ~agricoltore vicina))
=>
	(printout t "Sposto agricoltore lontano" crlf)
	(retract ?agricoltore)
	(assert (su-riva agricoltore lontana))
)


(defrule acquisizione "Acquisisce lo stato da tastiera"
	(declare (salience 1000))
	?modalita <- (modalita iniziale)
	(not (su-riva ? ?))
=>
	(printout t "--- Gioco dell'agricoltore ---" crlf)
	(printout t "Immetti lo stato iniziale per cortesia" crlf)
	(retract ?modalita)
)


(defrule acquisizione-elemento "Acquisisce l'elemento fino a quando il valore immesso non sara' corretto"
	(declare (salience 900))
	?serve <- (serve-acquisizione ?elemento)
	(not (su-riva ?elemento ?))
=>
	(printout t "Indica la posizione di " ?elemento ": (vicina/lontana)" crlf)
	(bind ?risposta (read))
	(assert (su-riva ?elemento ?risposta))
	(retract ?serve)
)


(defrule controllo-elemento-acquisito "Se un elemento acquisito e' invalido, prepara la riacquisizione"
	(declare (salience 901))
	?assposizione <- (su-riva ?elemento ?posizione)
	(test (neq ?posizione lontana vicina))
=>
	(printout t "Il valore immesso non e' valido: " ?posizione crlf)
	(retract ?assposizione)
	(assert (serve-acquisizione ?elemento)) 
)

(defrule condizione-errata-stato-pecora-mangia-cavolo "Controlla lo stato in cui la pecora mangia il cavolo e resetta il gioco"
	(declare (salience 800))
	(su-riva pecora ?riva1)
	(su-riva cavolo ?riva1)
	(su-riva agricoltore ~?riva1)
	(su-riva lupo ~?riva1)
=>
	(printout t "Complimenti... la pecora ha mangiato il cavolo.... (sono ironico)" crlf)
	(printout t "Ricominciamo..." crlf crlf)
	(assert (modalita reset))
)


(defrule condizione-errata-stato-lupo-mangia-pecora "Controlla lo stato in cui la pecora mangia il cavolo e resetta il gioco"
	(declare (salience 800))
	(su-riva pecora ?riva)
	(su-riva lupo ?riva)
	(su-riva agricoltore ~?riva)
	(su-riva cavolo ~?riva)
=>
	(printout t "Complimenti... il lupo ha mangiato la pecora.... (sono ironico)" crlf)
	(printout t "Ricominciamo..." crlf crlf)
	(assert (modalita reset))
)


(defrule modalita-reset-pulizia-su-riva "Rimuove tutti gli elementi su-riva durante la modalita' reset"
	(declare (salience 1002))
	(modalita reset)
	?suriva <- (su-riva ? ?)	
=>
	(retract ?suriva)
)


(defrule modalita-reset-pulizia-acquisizione "Rimuove tutti gli elementi serve-acquisizione durante la modalita' reset"
	(declare (salience 1002))
	(modalita reset)
	?acquisizione <- (serve-acquisizione ?)	
=>
	(retract ?acquisizione)
)

(defrule termina-modalita-reset "Resetta lo stato iniziale"
	(declare (salience 1001))
	?modalita <- (modalita reset)
	(not (su-riva ? ?))
	(not (serve-acquisizione ?))
=>
	(retract ?modalita)
	(assert 
		(serve-acquisizione agricoltore)
		(serve-acquisizione lupo)
		(serve-acquisizione cavolo)
		(serve-acquisizione pecora)
		(modalita iniziale)
	)
)	

(deffacts stato-iniziale "Stato iniziale"
	(serve-acquisizione agricoltore)
	(serve-acquisizione lupo)
	(serve-acquisizione cavolo)
	(serve-acquisizione pecora)
	(modalita iniziale)
)

