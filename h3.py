from constants import *
from base import BASE
from holes import HOLES
import copy

class H3(HOLES):
	''' Establishes h3 consistency for L1, L2, L3, and L4.
	
	This constraints guarantees that the 3st hole falls on the beginning of 
	node 5. The relation L1 + L2 + L3 + L4 + 10 < h3 must hold for a 
	consistent assignment.
	
	h3 in the above relation is the length of hole 3 from top, and 10 is the
	minimum space required between the junction of nodes 4&5 and the 3rd
	hole.
	
	Direct updates:

		upper1 = h3 - ( lower2 + lower3 + lower4 + 10)
		upper2 = h3 - ( lower1 + lower3 + lower4 + 10)
		upper3 = h3 - ( lower1 + lower2 + lower4 + 10)
		upper4 = h3 - ( lower1 + lower2 + lower3 + 10)
	
	Indirect updates:

 		lower1 -> upper2, upper3, upper4
 		lower2 -> upper1, upper3, upper4
 		lower3 -> upper1, upper2, upper4
 		lower4 -> upper1, upper2, upper3

		in that, if lower bound of L1 (i.e. self.csp.D["L1"]["min"]) is reduced
		then, upper bounds of L2, L3, and L4 could be impacted.
		
		However, for the sake of simplicity, this algorithm checks all uppers 
		if any lower changes.
	'''
	
	def __init__(self, csp, asmnt):
		h = self.csp.spec["h3"]
		space = self.csp.spec["hmarg"] * 2
		p = {"L1", "L2", "L3", "L4"} 	# participants
		o = {				# others_map
			"L1": {"L2", "L3", "L4"},
			"L2": {"L1", "L3", "L4"},
			"L3": {"L1", "L2", "L4"},
			"L4": {"L1", "L2", "L3"}		
		}
		self.plowers = pl = {"L1": 0, "L2": 0, "L3": 0, "L4": 0}
		super().__init__(csp, asmnt, h, space, p, o, self.plowers, "h3")
