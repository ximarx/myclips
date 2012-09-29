
;;;======================================================
;;;   Monkees and Bananas Sample Problem
;;;
;;;     This is an extended version of a
;;;     rather common AI planning problem.
;;;     The point is for the monkee to find
;;;     and eat some bananas.
;;;
;;;     CLIPS Version 6.0 Example
;;;
;;;     To execute, merely load, reset and run.
;;;======================================================
             
;;;*************
;;;* TEMPLATES *
;;;*************

(deftemplate monkey 
   (slot location 
      (type SYMBOL) 
      (default green_couch))
   (slot on_top_of 
      (type SYMBOL) 
      (default floor)) 
   (slot holding 
      (type SYMBOL) 
      (default blank)))

(deftemplate thing 
   (slot name 
      (type SYMBOL)
      ) 
   (slot location 
      (type SYMBOL)
      ) 
   (slot on_top_of 
      (type SYMBOL) 
      (default floor))
   (slot weight 
      (type SYMBOL) 
      (default light)))
                    
(deftemplate chest 
   (slot name 
      (type SYMBOL)
      ) 
   (slot contents 
      (type SYMBOL)
      ) 
   (slot unlocked_by 
      (type SYMBOL)
      ))
               
(deftemplate goal_is_to 
   (slot action 
      (type SYMBOL)
      ) 
   (multislot arguments 
      (type SYMBOL)
      ))
             
;;;*************************
;;;* CHEST UNLOCKING RULES *
;;;*************************

(defrule hold_chest_to_put_on_floor "" 
  (goal_is_to (action unlock) (arguments ?chest))
  (thing (name ?chest) (on_top_of ~floor) (weight light))
  (monkey (holding ~?chest))
  (not (goal_is_to (action hold) (arguments ?chest)))
  =>
  (assert (goal_is_to (action hold) (arguments ?chest))))

(defrule put_chest_on_floor "" 
  (goal_is_to (action unlock) (arguments ?chest))
  ?monkey <- (monkey (location ?place) (on_top_of ?on) (holding ?chest))
  ?thing <- (thing (name ?chest))
  =>
  (printout t "Monkey throws the " ?chest " off the " 
              ?on " onto the floor." crlf)
  (modify ?monkey (holding blank))
  (modify ?thing (location ?place) (on_top_of floor)))

(defrule get_key_to_unlock "" 
  (goal_is_to (action unlock) (arguments ?obj))
  (thing (name ?obj) (on_top_of floor))
  (chest (name ?obj) (unlocked_by ?key))
  (monkey (holding ~?key))
  (not (goal_is_to (action hold) (arguments ?key)))
  =>
  (assert (goal_is_to (action hold) (arguments ?key))))

(defrule move_to_chest_with_key "" 
  (goal_is_to (action unlock) (arguments ?chest))
  (monkey (location ?mplace) (holding ?key))
  (thing (name ?chest) (location ?cplace&~?mplace) (on_top_of floor))
  (chest (name ?chest) (unlocked_by ?key))
  (not (goal_is_to (action walk_to) (arguments ?cplace)))
  =>
  (assert (goal_is_to (action walk_to) (arguments ?cplace))))

(defrule unlock_chest_with_key "" 
  ?goal <- (goal_is_to (action unlock) (arguments ?name))
  ?chest <- (chest (name ?name) (contents ?contents) (unlocked_by ?key))
  (thing (name ?name) (location ?place) (on_top_of ?on))
  (monkey (location ?place) (on_top_of ?on) (holding ?key))
  =>
  (printout t "Monkey opens the " ?name " with the " ?key 
              " revealing the " ?contents "." crlf)
  (modify ?chest (contents nothing))
  (assert (thing (name ?contents) (location ?place) (on_top_of ?name)))
  (retract ?goal))

;;;*********************
;;;* HOLD OBJECT RULES * 
;;;*********************

(defrule unlock_chest_to_hold_object ""
  (goal_is_to (action hold) (arguments ?obj))
  (chest (name ?chest) (contents ?obj))
  (not (goal_is_to (action unlock) (arguments ?chest)))
  =>
  (assert (goal_is_to (action unlock) (arguments ?chest))))

(defrule use_ladder_to_hold ""
  (goal_is_to (action hold) (arguments ?obj))
  (thing (name ?obj) (location ?place) (on_top_of ceiling) (weight light))
  (not (thing (name ladder) (location ?place)))
  (not (goal_is_to (action move) (arguments ladder ?place)))
  =>
  (assert (goal_is_to (action move) (arguments ladder ?place))))

(defrule climb_ladder_to_hold ""
  (goal_is_to (action hold) (arguments ?obj))
  (thing (name ?obj) (location ?place) (on_top_of ceiling) (weight light))
  (thing (name ladder) (location ?place) (on_top_of floor))
  (monkey (on_top_of ~ladder))
  (not (goal_is_to (action on) (arguments ladder)))
  =>
  (assert (goal_is_to (action on) (arguments ladder))))

(defrule grab_object_from_ladder "" 
  ?goal <- (goal_is_to (action hold) (arguments ?name))
  ?thing <- (thing (name ?name) (location ?place) 
                     (on_top_of ceiling) (weight light))
  (thing (name ladder) (location ?place))
  ?monkey <- (monkey (location ?place) (on_top_of ladder) (holding blank))
  =>
  (printout t "Monkey grabs the " ?name "." crlf)
  (modify ?thing (location held) (on_top_of held))
  (modify ?monkey (holding ?name))
  (retract ?goal))

(defrule climb_to_hold "" 
  (goal_is_to (action hold) (arguments ?obj))
  (thing (name ?obj) (location ?place) (on_top_of ?on&~ceiling) (weight light))
  (monkey (location ?place) (on_top_of ~?on))
  (not (goal_is_to (action on) (arguments ?on)))
  =>
  (assert (goal_is_to (action on) (arguments ?on))))

(defrule walk_to_hold ""
  (goal_is_to (action hold) (arguments ?obj))
  (thing (name ?obj) (location ?place) (on_top_of ~ceiling) (weight light))
  (monkey (location ~?place))
  (not (goal_is_to (action walk_to) (arguments ?place)))
  =>
  (assert (goal_is_to (action walk_to) (arguments ?place))))

(defrule drop_to_hold ""
  (goal_is_to (action hold) (arguments ?obj))
  (thing (name ?obj) (location ?place) (on_top_of ?on) (weight light))
  (monkey (location ?place) (on_top_of ?on) (holding ~blank))
  (not (goal_is_to (action hold) (arguments blank)))
  =>
  (assert (goal_is_to (action hold) (arguments blank))))

(defrule grab_object "" 
  ?goal <- (goal_is_to (action hold) (arguments ?name))
  ?thing <- (thing (name ?name) (location ?place) 
                     (on_top_of ?on) (weight light))
  ?monkey <- (monkey (location ?place) (on_top_of ?on) (holding blank))
  =>
  (printout t "Monkey grabs the " ?name "." crlf)
  (modify ?thing (location held) (on_top_of held))
  (modify ?monkey (holding ?name))
  (retract ?goal))

(defrule drop_object ""  
  ?goal <- (goal_is_to (action hold) (arguments blank))
  ?monkey <- (monkey (location ?place) 
                     (on_top_of ?on) 
                     (holding ?name&~blank))
  ?thing <- (thing (name ?name))
  =>
  (printout t "Monkey drops the " ?name "." crlf)
  (modify ?monkey (holding blank))
  (modify ?thing (location ?place) (on_top_of ?on))
  (retract ?goal))

;;;*********************
;;;* MOVE OBJECT RULES * 
;;;*********************

(defrule unlock_chest_to_move_object "" 
  (goal_is_to (action move) (arguments ?obj ?))
  (chest (name ?chest) (contents ?obj))
  (not (goal_is_to (action unlock) (arguments ?chest)))
  =>
  (assert (goal_is_to (action unlock) (arguments ?chest))))

(defrule hold_object_to_move ""  
  (goal_is_to (action move) (arguments ?obj ?place))
  (thing (name ?obj) (location ~?place) (weight light))
  (monkey (holding ~?obj))
  (not (goal_is_to (action hold) (arguments ?obj)))
  =>
  (assert (goal_is_to (action hold) (arguments ?obj))))

(defrule move_object_to_place "" 
  (goal_is_to (action move) (arguments ?obj ?place))
  (monkey (location ~?place) (holding ?obj))
  (not (goal_is_to (action walk_to) (arguments ?place)))
  =>
  (assert (goal_is_to (action walk_to) (arguments ?place))))

(defrule drop_object_once_moved "" 
  ?goal <- (goal_is_to (action move) (arguments ?name ?place))
  ?monkey <- (monkey (location ?place) (holding ?obj))
  ?thing <- (thing (name ?name) (weight light))
  =>
  (printout t "Monkey drops the " ?name "." crlf)
  (modify ?monkey (holding blank))
  (modify ?thing (location ?place) (on_top_of floor))
  (retract ?goal))

(defrule already_moved_object ""
  ?goal <- (goal_is_to (action move) (arguments ?obj ?place))
  (thing (name ?obj) (location ?place))
  =>
  (retract ?goal))

;;;***********************
;;;* WALK TO PLACE RULES *
;;;***********************

(defrule already_at_place "" 
  ?goal <- (goal_is_to (action walk_to) (arguments ?place))
  (monkey (location ?place))
  =>
  (retract ?goal))

(defrule get_on_floor_to_walk ""
  (goal_is_to (action walk_to) (arguments ?place))
  (monkey (location ~?place) (on_top_of ~floor))
  (not (goal_is_to (action on) (arguments floor)))
  =>
  (assert (goal_is_to (action on) (arguments floor))))

(defrule walk_holding_nothing ""
  ?goal <- (goal_is_to (action walk_to) (arguments ?place))
  ?monkey <- (monkey (location ~?place) (on_top_of floor) (holding blank))
  =>
  (printout t "Monkey walks to " ?place "." crlf)
  (modify ?monkey (location ?place))
  (retract ?goal))

(defrule walk_holding_object ""
  ?goal <- (goal_is_to (action walk_to) (arguments ?place))
  ?monkey <- (monkey (location ~?place) (on_top_of floor) (holding ?obj&~blank))
  =>
  (printout t "Monkey walks to " ?place " holding the " ?obj "." crlf)
  (modify ?monkey (location ?place))
  (retract ?goal))

;;;***********************
;;;* GET ON OBJECT RULES * 
;;;***********************

(defrule jump_onto_floor "" 
  ?goal <- (goal_is_to (action on) (arguments floor))
  ?monkey <- (monkey (on_top_of ?on&~floor))
  =>
  (printout t "Monkey jumps off the " ?on " onto the floor." crlf)
  (modify ?monkey (on_top_of floor))
  (retract ?goal))

(defrule walk_to_place_to_climb "" 
  (goal_is_to (action on) (arguments ?obj))
  (thing (name ?obj) (location ?place))
  (monkey (location ~?place))
  (not (goal_is_to (action walk_to) (arguments ?place)))
  =>
  (assert (goal_is_to (action walk_to) (arguments ?place))))

(defrule drop_to_climb "" 
  (goal_is_to (action on) (arguments ?obj))
  (thing (name ?obj) (location ?place))
  (monkey (location ?place) (holding ~blank))
  (not (goal_is_to (action hold) (arguments blank)))
  =>
  (assert (goal_is_to (action hold) (arguments blank))))

(defrule climb_indirectly "" 
  (goal_is_to (action on) (arguments ?obj))
  (thing (name ?obj) (location ?place) (on_top_of ?on))
  (monkey (location ?place) (on_top_of ~?on&~?obj) (holding blank))
  (not (goal_is_to (action on) (arguments ?on)))
  =>
  (assert (goal_is_to (action on) (arguments ?on))))

(defrule climb_directly ""  
  ?goal <- (goal_is_to (action on) (arguments ?obj))
  (thing (name ?obj) (location ?place) (on_top_of ?on))
  ?monkey <- (monkey (location ?place) (on_top_of ?on) (holding blank))
  =>
  (printout t "Monkey climbs onto the " ?obj "." crlf)
  (modify ?monkey (on_top_of ?obj))
  (retract ?goal))

(defrule already_on_object ""
  ?goal <- (goal_is_to (action on) (arguments ?obj))
  (monkey (on_top_of ?obj))
  =>
  (retract ?goal))

;;;********************
;;;* EAT OBJECT RULES * 
;;;********************

(defrule hold_to_eat ""
  (goal_is_to (action eat) (arguments ?obj))
  (monkey (holding ~?obj))
  (not (goal_is_to (action hold) (arguments ?obj)))
  =>
  (assert (goal_is_to (action hold) (arguments ?obj))))

(defrule satisfy_hunger ""
  ?goal <- (goal_is_to (action eat) (arguments ?name))
  ?monkey <- (monkey (holding ?name))
  ?thing <- (thing (name ?name))
  =>
  (printout t "Monkey eats the " ?name "." crlf)
  (modify ?monkey (holding blank))
  (retract ?goal ?thing))
 
;;;**********************
;;;* INITIAL STATE RULE * 
;;;**********************

(defrule startup ""
  =>
  (assert (monkey (location t5_7) (on_top_of green_couch) (holding blank)))
  (assert (thing (name green_couch) (location t5_7) (weight heavy)))
  (assert (thing (name red_couch) (location t2_2) (weight heavy)))
  (assert (thing (name big_pillow) (location t2_2) (on_top_of red_couch)))
  (assert (thing (name red_chest) (location t2_2) (on_top_of big_pillow)))
  (assert (chest (name red_chest) (contents ladder) (unlocked_by red_key)))
  (assert (thing (name blue_chest) (location t7_7) (on_top_of ceiling)))
  (assert (chest (name blue_chest) (contents bananas) (unlocked_by blue_key)))
  (assert (thing (name blue_couch) (location t8_8) (weight heavy)))
  (assert (thing (name green_chest) (location t8_8) (on_top_of ceiling)))
  (assert (chest (name green_chest) (contents blue_key) (unlocked_by red_key)))
  (assert (thing (name red_key) (location t1_3)))
  (assert (goal_is_to (action eat) (arguments bananas))))
