from constants import *
import math

class HALF():
	'''Implements consistency algorithm for l1_half_l2 constraint.
	
        There must be this relation between assigned values to L1 and L2:

        L1 = L2 / 2     or      L2 = L1 * 2
		
		Also the boundaries could be made consistent.
		'''
	
	def establish(self, csp, curvar, value):
		'''Establishes consistency W.R.T. l1_half_l2 constraint.
		
		The domain of L2 reduces to L1 * 2.
	
		If L1 is assigned a value, L2 reduces to one value only. However,
		the domain of L2 will still be represented via bounds, now with
		equal min & max.
		
		If the assigned variable is L2, nothing happens. The assumption is
		that L1 is always assigned first.

		L1 = 100
		L2 = {"min": 80,  "max":90}
		'''
		if curvar != "L1":
			return (DOMAINS_INTACT, set([]))
		L2 = csp.get_domain("L2")
		if L2["min"] > value * 2 or L2["max"] < value * 2:
			return (CONTRADICTION, {"L2"})
		if L2["max"] == L2["max"] and value * 2 == L2["max"]:
			return (DOMAINS_INTACT, {"L2"})
		csp.update_domain("L2", {"min": value * 2, "max": value * 2})
		return (DOMAINS_REDUCED, {"L2"}, {"L2"})

	def propagate(self, csp, reduced_vars):
		'''Establishes bounds consistency W.R.T. l1_half_l2 constraint.
		
		Note: only one of the above updates happen. In case of
		contradiction, both reduced variables are involved. That's why
		reduced_vars is returned as the conflict set.
		'''
		L1 = csp.get_domain("L1")
		L2 = csp.get_domain("L2")
		if self.__consistent(L1, L2):
			return (DOMAINS_INTACT, {"L1", "L2"})
		elif self.__contradiction(L1, L2):
				return (CONTRADICTION, {"L1", "L2"})
		reduced = set([])
		if L1["min"] * 2 > L2["min"] + 1: # min of L2 can adjust
			csp.update_domain("L2", {"min": L1["min"] * 2, "max": L2["max"]})
			reduced.add("L2")
		elif L1["min"] * 2 < L2["min"] + 1: # min of L1 can adjust
			new_min = math.ceil(L2["min"] / 2)
			csp.update_domain("L1", {"min": new_min, "max": L1["max"]})
			reduced.add("L1")
		if L1["max"] * 2 > L2["max"] + 1: # max of L1 can adjust
			new_max = math.ceil(L2["max"] / 2)
			csp.update_domain("L1", {"min": L1["min"], "max": new_max})
			reduced.add("L1")
		elif L1["max"] * 2 < L2["max"] + 1: # max of L2 can adjust
			csp.update_domain("L2", {"min": L2["min"], "max": L1["max"] * 2})
			reduced.add("L2")
		return (DOMAINS_REDUCED, {"L1", "L2"}, reduced)

	def __contradiction(self, L1, L2):
		'''Checkes if the domains are inconsistent but cannot adjust.
		
		A reduction that reduces one of the domains to one value is likely
		causing a contradiction--if the other domain does not match.
		'''
		if L1["min"] == L1["max"] or L2["min"] == L2["max"]:
			return True
		return False

	def __consistent(self, L1, L2):
		'''Checks if the domains are already consistent.'''
		if L1["min"] * 2 == L2["min"]:
			if L1["max"] * 2 == L2["max"]:
				return True
		return False