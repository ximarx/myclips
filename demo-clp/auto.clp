
;;;======================================================
;;;   Automotive Expert System
;;;
;;;     This expert system diagnoses some simple
;;;     problems with a car.
;;;
;;;     CLIPS Version 6.3 Example
;;;
;;;     To execute, merely load, reset and run.
;;;======================================================

;;****************
;;* DEFFUNCTIONS *
;;****************

(deffunction ask_question (?question $?allowed_values)
   (printout t ?question)
   (bind ?answer (read))
   (if (lexemep ?answer) 
       then (bind ?answer (lowcase ?answer)))
   (while (not (member ?answer ?allowed_values)) do
      (printout t ?question)
      (bind ?answer (read))
      (if (lexemep ?answer) 
          then (bind ?answer (lowcase ?answer))))
   ?answer)

(deffunction yes_or_no_p (?question)
   (bind ?response (ask_question ?question yes no y n))
   (if (or (eq ?response yes) (eq ?response y))
       then yes 
       else no))

;;;***************
;;;* QUERY RULES *
;;;***************

(defrule determine_engine_state ""
   (not (engine_starts ?))
   (not (repair ?))
   =>
   (assert (engine_starts (yes_or_no_p "Does the engine start (yes/no)? "))))
   
(defrule determine_runs_normally ""
   (engine_starts yes)
   (not (repair ?))
   =>
   (assert (runs_normally (yes_or_no_p "Does the engine run normally (yes/no)? "))))

(defrule determine_rotation_state ""
   (engine_starts no)
   (not (repair ?))   
   =>
   (assert (engine_rotates (yes_or_no_p "Does the engine rotate (yes/no)? "))))
   
(defrule determine_sluggishness ""
   (runs_normally no)
   (not (repair ?))
   =>
   (assert (engine_sluggish (yes_or_no_p "Is the engine sluggish (yes/no)? "))))
   
(defrule determine_misfiring ""
   (runs_normally no)
   (not (repair ?))
   =>
   (assert (engine_misfires (yes_or_no_p "Does the engine misfire (yes/no)? "))))

(defrule determine_knocking ""
   (runs_normally no)
   (not (repair ?))
   =>
   (assert (engine_knocks (yes_or_no_p "Does the engine knock (yes/no)? "))))

(defrule determine_low_output ""
   (runs_normally no)
   (not (repair ?))
   =>
   (assert (engine_output_low
               (yes_or_no_p "Is the output of the engine low (yes/no)? "))))

(defrule determine_gas_level ""
   (engine_starts no)
   (engine_rotates yes)
   (not (repair ?))
   =>
   (assert (tank_has_gas
              (yes_or_no_p "Does the tank have any gas in it (yes/no)? "))))

(defrule determine_battery_state ""
   (engine_rotates no)
   (not (repair ?))
   =>
   (assert (battery_has_charge
              (yes_or_no_p "Is the battery charged (yes/no)? "))))

(defrule determine_point_surface_state ""
   (or (and (engine_starts no)      
            (engine_rotates yes))
       (engine_output_low yes))
   (not (repair ?))
   =>
   (assert (point_surface_state
      (ask_question "What is the surface state of the points (normal/burned/contaminated)? "
                    normal burned contaminated))))

(defrule determine_conductivity_test ""
   (engine_starts no)      
   (engine_rotates no)
   (battery_has_charge yes)
   (not (repair ?))
   =>
   (assert (conductivity_test_positive
              (yes_or_no_p "Is the conductivity test for the ignition coil positive (yes/no)? "))))

;;;****************
;;;* REPAIR RULES *
;;;****************

(defrule normal_engine_state_conclusions ""
   (runs_normally yes)
   (not (repair ?))
   =>
   (assert (repair "No repair needed.")))

(defrule engine_sluggish ""
   (engine_sluggish yes)
   (not (repair ?))
   =>
   (assert (repair "Clean the fuel line."))) 

(defrule engine_misfires ""
   (engine_misfires yes)
   (not (repair ?))
   =>
   (assert (repair "Point gap adjustment.")))     

(defrule engine_knocks ""
   (engine_knocks yes)
   (not (repair ?))
   =>
   (assert (repair "Timing adjustment.")))

(defrule tank_out_of_gas ""
   (tank_has_gas no)
   (not (repair ?))
   =>
   (assert (repair "Add gas.")))

(defrule battery_dead ""
   (battery_has_charge no)
   (not (repair ?))
   =>
   (assert (repair "Charge the battery.")))

(defrule point_surface_state_burned ""
   (point_surface_state burned)
   (not (repair ?))
   =>
   (assert (repair "Replace the points.")))

(defrule point_surface_state_contaminated ""
   (point_surface_state contaminated)
   (not (repair ?))
   =>
   (assert (repair "Clean the points.")))

(defrule conductivity_test_positive_yes ""
   (conductivity_test_positive yes)
   (not (repair ?))
   =>
   (assert (repair "Repair the distributor lead wire.")))

(defrule conductivity_test_positive_no ""
   (conductivity_test_positive no)
   (not (repair ?))
   =>
   (assert (repair "Replace the ignition coil.")))

(defrule no_repairs ""
  (declare (salience -10))
  (not (repair ?))
  =>
  (assert (repair "Take your car to a mechanic.")))

;;;********************************
;;;* STARTUP AND CONCLUSION RULES *
;;;********************************

(defrule system_banner ""
  (declare (salience 10))
  =>
  (printout t crlf crlf)
  (printout t "The Engine Diagnosis Expert System")
  (printout t crlf crlf))

(defrule print_repair ""
  (declare (salience 10))
  (repair ?item)
  =>
  (printout t crlf crlf)
  (printout t "Suggested Repair:")
  (printout t crlf crlf)
  (format t " %s%n%n%n" ?item))

