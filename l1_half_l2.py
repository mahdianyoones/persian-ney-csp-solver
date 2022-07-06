from constants import *
import math

class L1_HALF_L2():
	'''Reduces L1 and L2 domains so that L1 = L2 * 2.
	
	If L1 is assigned a value, L2 reduces to one value only. However,
	the domain of L2 will still be represented via bounds--now with
	equal min & max.
	
	Updates:
		lower1 = max(lower1, lower2/2) 
		lower2 = max(lower2, lower1*2)
		upper1 = min(upper1, upper2/2)
		upper2 = min(upper2, upper2*2)	
	'''

	def __init__(self, csp):
		self.csp = csp
		
	def b_update(self, asmnt):
		'''Updates the bounds of L1 and L2 W.R.T. l1_half_l2.
		
		If L1 is in the assignment, L2 is already made consistency
		in the establish function.
		'''
		if "L1" in asmnt.assigned:
			return (DOMAINS_INTACT, set([]))
		# Adjust L2 if possible
		d1 = self.csp.D["L1"]
		d2 = self.csp.D["L2"]
		lower2 = d1["min"] * 2
		upper2 = d1["max"] * 2
		impacted = set([])
		if lower2 > d2["min"] and lower2 <= d2["max"]:
			d2["min"] = lower2
			impacted.add("L2")
		if upper2 < d2["max"] and upper2 >= d2["min"]:
			d2["max"] = upper2
			impacted.add("L2")
		# Else try adjusting L1
		if not "L2" in impacted:
			inf = float("inf")
			lower1 = math.ceil(d2["min"] / 2) if d2["min"] != inf else inf
			upper1 = math.floor(d2["max"] / 2) if d2["max"] != inf else inf
			if lower1 > d1["min"] and lower1 <= d1["max"]:
				d1["min"] = lower1
				impacted.add("L1")
			if upper1 < d1["max"] and upper1 >= d1["min"]:
				d1["max"] = upper1
				impacted.add("L1")
		if len(impacted) == 0:
			if not (d1["min"]*2==d2["min"] and d1["max"]*2==d2["max"]):
				return (CONTRADICTION, {"L1", "L2"}, "l1_half_l2")
			return (DOMAINS_INTACT, set([]))
		self.csp.update_d("L1", d1)
		self.csp.update_d("L2", d2)
		return (DOMAINS_REDUCED, impacted)
							
	def establish(self, asmnt, curvar, value):
		'''Reduces L2 to only one value: L1 * 2.'''
		if curvar == "L2" or "L2" in asmnt.assigned:
			return (DOMAINS_INTACT, None)
		new_val = value * 2
		d1 = self.csp.D["L1"]
		d2 = self.csp.D["L2"]
		if new_val < d2["min"] or new_val > d2["max"]:
			return (CONTRADICTION, set([]), "l1_half_l2")
		if d2["max"] == d2["min"]:
			return (DOMAINS_INTACT, None)
		self.csp.update_d("L2", {"min": new_val, "max": new_val})
		return (DOMAINS_REDUCED, {"L2"})
