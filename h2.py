from constants import *
from base import BASE
from holes import HOLES
import copy

class H2(HOLES):
	''' Establishes h2 consistency for L1, L2, and L3.
	
	This constraints guarantees that the 2st hole falls on node 4 below 
	hole 1. The relation L1 + L2 + L3 + 30 < h2 must hold for a 
	consistent assignment.
	
	h2 in the above relation is the length of hole 2 from top, and 30 is the
	minimum space required between the junction of nodes 3&4 and the 2nd hole.

	Direct updates:

		upper1 = h2 - (lower2 + lower3 + 30)
		upper2 = h2 - (lower1 + lower3 + 30)
		upper3 = h2 - (lower1 + lower2 + 30)	

	Indirect updates:

		lower1 -> upper2, upper3
		lower2 -> upper1, upper3
		lower3 -> upper1, upper2

		that is, if lower bound of L1 (i.e. self.csp.D["L1"]["min"]) is reduced
		then, upper bounds of L2 and L3 could be impacted.
		
		However, for the sake of simplicity, this algorithm checks all uppers 
		if any lower changes.
	'''
	
	def __init__(self, csp, asmnt):
		h = self.csp.spec["h2"]
		space = self.csp.spec["hmarg"] * 2
		space += self.csp.spec["holed"] * 1
		p = {"L1", "L2", "L3"} 	# participants
		o = {				# others_map
			"L1": {"L2", "L3"},
			"L2": {"L1", "L3"},
			"L3": {"L1", "L2"}		
		}
		self.plowers = pl = {"L1": 0, "L2": 0, "L3": 0}
		super().__init__(csp, asmnt, h, space, p, o, self.plowers, "h2")
