from constants import *
from base import BASE
from holes import HOLES
import copy

class H5(HOLES):
	''' Establishes h5 consistency for L1, L2, L3, and L4.
	
	This constraints guarantees that the 5th hole falls on the node 5 below the
	3rd and 4th holes. The relation L1 + L2 + L3 + L4 + 50 < h5 must hold for a 
	consistent assignment.
	
	h5 in the above relation is the length of hole 5 from top, and 50 is the
	minimum space required between the junction of nodes 4&5 and the 5th 
	hole.
	
	Direct updates:

		upper1 = h5 - ( lower2 + lower3 + lower4 + 30)
		upper2 = h5 - ( lower1 + lower3 + lower4 + 30)
		upper3 = h5 - ( lower1 + lower2 + lower4 + 30)
		upper4 = h5 - ( lower1 + lower2 + lower3 + 30)
	
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
		h = self.csp.spec["h5"]
		space = self.csp.spec["hmarg"] * 3
		space += self.csp.spec["holed"] * 2
		p = {"L1", "L2", "L3", "L4"} 	# participants
		o = {				# others_map
			"L1": {"L2", "L3", "L4"},
			"L2": {"L1", "L3", "L4"},
			"L3": {"L1", "L2", "L4"},
			"L4": {"L1", "L2", "L3"}		
		}
		self.plowers = pl = {"L1": 0, "L2": 0, "L3": 0, "L4": 0}
		super().__init__(csp, asmnt, h, space, p, o, self.plowers, "h5")
