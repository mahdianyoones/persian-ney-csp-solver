from constants import *
from base import BASE
from holes import HOLES
import copy

class H1(HOLES):
	''' Establishes h1 consistency for L1, L2, and L3.
	
	This constraints guarantees that the 1st hole falls on node 4.The 
	relation L1 + L2 + L3 + 10 < h1 must hold for a consistent assignment.
	
	h1 in the above relation is the length of hole 1 from top, and 10 is the
	minimum hole junction space between nodes 3&4 and the 1st hole.

	Direct updates:
	
	 	upper1 = h1 - (lower2 + lower3 + 10)
		upper2 = h1 - (lower1 + lower3 + 10)
		upper3 = h1 - (lower1 + lower2 + 10)
			
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
		h = self.csp.spec["h1"]
		space = self.csp.spec["hmarg"] * 1
		p = {"L1", "L2", "L3"} 	# participants
		o = {				# others_map
			"L1": {"L2", "L3"},
			"L2": {"L1", "L3"},
			"L3": {"L1", "L2"}		
		}
		self.plowers = pl = {"L1": 0, "L2": 0, "L3": 0}
		super().__init__(csp, asmnt, h, space, p, o, self.plowers, "h1")
