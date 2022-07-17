from constants import *
from base import BASE
from holes import HOLES
import copy

class H6(HOLES):
	''' Establishes h6 consistency for L1, L2, L3, L4, L5.
	
	This constraints guarantees that the 6th hole falls on the beginning of
	node 6. The relation L1 + L2 + L3 + L4 + L5 + 10 < h6 must hold for a
	consistent assignment.
	
	h5 in the above relation is the length of hole 5 from top, and 50 is the
	minimum space required between the junction of nodes 4&5 and the 5th 
	hole.
	
	Direct updates:

		upper1 = h6 - (lower2 + lower3 + lower4 + lower5 + 10)
		upper2 = h6 - (lower1 + lower3 + lower4 + lower5 + 10)
		upper3 = h6 - (lower1 + lower2 + lower4 + lower5 + 10)
		upper4 = h6 - (lower1 + lower2 + lower3 + lower5 + 10)
		upper5 = h6 - (lower1 + lower2 + lower3 + lower4 + 10)
	
	Indirect updates:

 		lower1 -> upper2, upper3, upper4, upper5
 		lower2 -> upper1, upper3, upper4, upper5
 		lower3 -> upper1, upper2, upper4, upper5
 		lower4 -> upper1, upper2, upper3, upper5
 		lower5 -> upper1, upper2, upper3, upper4

		in that, if lower bound of L1 (i.e. self.csp.D["L1"]["min"]) is reduced
		then, upper bounds of L2, L3, L4, and L5 could be impacted.
		
		However, for the sake of simplicity, this algorithm checks all uppers 
		if any lower changes.
	'''
	
	def __init__(self, csp, asmnt):
		h = self.csp.spec["h6"]
		space = self.csp.spec["hmarg"] * 1
		p = {"L1", "L2", "L3", "L4", "L5"} 	# participants
		o = {				# others_map
			"L1": {"L2", "L3", "L4", "L5"},
			"L2": {"L1", "L3", "L4", "L5"},
			"L3": {"L1", "L2", "L4", "L5"},
			"L4": {"L1", "L2", "L3", "L5"},
			"L5": {"L1", "L2", "L3", "L4"},
		}
		self.plowers = pl = {"L1": 0, "L2": 0, "L3": 0, "L4": 0, "L5"}
		super().__init__(csp, asmnt, h, space, p, o, self.plowers, "h6")
