from constants import *

class L1_HALF_L2():
	'''Reduces L1 and L2 domains so that L1 = L2 * 2.
	
	If L1 is assigned a value, L2 reduces to one value only. However,
	the domain of L2 will still be represented via bounds--now with
	equal min & max.
	
	Example: 
	'''

	def __init__(self, csp):
		self.csp = csp
		
	def establish(self, asmnt, curvar, value):
		dl1 = self.csp.D["L1"]
		dl2 = self.csp.D["L2"]
		impacted = {}
		if value == None:
			lower22 = dl2["min"] / 2
			if lower22 >= dl1["max"] or lower22 <= dl2["min"]:
				return (DOMAINS_INTACT, None)
			if lower22 < dl1["max"]:
				dl1["max"] = lower22
				impacted.add("L1")
			if lower22 > dl2["min"]:
				dl2["min"] = lower22
				impacted.add("L2")
			if dl1["min"] < dl1["max"] or dl2["min"] < dl2["max"]:
				return (CONTRADICTION, None)
		else:
			new_val = value * 2
			if new_val >= dl2["max"] or new_val <= dl2["min"]:
				return (CONTRADICTION, None)
			if new_val == dl2["max"] and new_val == dl2["min"]:
				return (DOMAINS_INTACT, None)			
			dl2 = {"min": new_val, "max": new_val}
			impacted.add("L2")
		if len(impacted) == 0:
			return (DOMAINS_INTACT, None)
		return (DOMAINS_REDUCED, impacted)	
	
