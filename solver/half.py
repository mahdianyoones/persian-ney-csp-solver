from constants import *
import math

class HALF():
	'''Implements consistency algorithm for the half constraint.
	
        The second node must be double the length of the first node. i.e. :

        L1 = L2 / 2     or      L2 = L1 * 2
				
		This algorithm also handles propagation. That is, when L1 or L2 are
		reduced by other constraints, the effect is kept in check.

		If L1 is reduced, the boundary of both L1 and L2 are examined and made
		consistent. If this reduction makes consistency impossible,
		contradiction is reported.'''
	
	def establish(self, csp, curvar, value):
		'''Establishes consistency after assignment curvar: value.
		
		The domain of L2 reduces to L1 * 2. Or, the domain of L1 reduces to
		L2 / 2.
	
		After consistency, L2 or L1 reduces to one value only; however, its
		domain is now represented via bounds with equal min & max.'''
		A = csp.get_assignment()
		D = csp.get_domains()
		if "L1" in A and "L2" in A:
			return (DOMAINS_INTACT, set([]))
		if curvar == "L1": # L2 is not assigned
			new_value = value * 2
			if new_value < D["L2"]["min"] or new_value > D["L2"]["max"]:
				return (CONTRADICTION, {"L2"}, {"L1"})
			if D["L2"]["min"] == D["L2"]["max"]:
				return (DOMAINS_INTACT, {"L2"})
			else:
				csp.update_domain("L2", {"min": new_value, "max": new_value})
				return (DOMAINS_REDUCED, {"L2"}, {"L2"})
		else: # L1 is not assigned
			new_value = math.ceil(value / 2)
			if new_value < D["L1"]["min"] or new_value > D["L1"]["max"]:
				return (CONTRADICTION, {"L1"}, {"L2"})
			if D["L1"]["min"] == D["L1"]["max"]:
				return (DOMAINS_INTACT, {"L1"})
			else:
				csp.update_domain("L1", {"min": new_value, "max": new_value})
				return (DOMAINS_REDUCED, {"L1"}, {"L1"})

	def propagate(self, csp, reduced_vars):
		'''Establishes consistency when L1 andor L2 are reduced elsewhere.'''
		A = csp.get_assignment()
		D = csp.get_domains()
		if self.__consistent(D):
			return (DOMAINS_INTACT, {"L1", "L2"})
		elif self.__contradiction(D):
			return (CONTRADICTION, {"L1", "L2"}, set([]))
		reduced = set([])
		if D["L1"]["min"] * 2 > D["L2"]["min"]: # min of L2 can adjust
			new_domain = {"min": D["L1"]["min"] * 2, "max": D["L2"]["max"]}
			csp.update_domain("L2", new_domain)
			reduced.add("L2")
		elif D["L1"]["min"] * 2 < D["L2"]["min"]: # min of L1 can adjust
			new_min = math.ceil(D["L2"]["min"] / 2)
			csp.update_domain("L1", {"min": new_min, "max": D["L1"]["max"]})
			reduced.add("L1")
		if D["L1"]["max"] * 2 > D["L2"]["max"]: # max of L1 can adjust
			new_max = math.ceil(D["L2"]["max"] / 2)
			csp.update_domain("L1", {"min": D["L1"]["min"], "max": new_max})
			reduced.add("L1")
		elif D["L1"]["max"] * 2 < D["L2"]["max"]: # max of L2 can adjust
			new_domain = {"min": D["L2"]["min"], "max": D["L1"]["max"] * 2}
			csp.update_domain("L2", new_domain)
			reduced.add("L2")
		return (DOMAINS_REDUCED, {"L1", "L2"}, reduced)

	def __contradiction(self, D):
		'''Checkes if the domains are inconsistent but cannot adjust.
		
		A reduction that reduces one of the domains to one value is likely
		causing a contradiction--if the other domain does not match.
		'''
		if D["L1"]["min"] == D["L1"]["max"] or D["L2"]["min"]==D["L2"]["max"]:
			return True
		return False

	def __consistent(self, D):
		'''Checks if the domains are already consistent.'''
		if D["L1"]["min"] * 2 == D["L2"]["min"]:
			if D["L1"]["max"] * 2 == D["L2"]["max"]:
				return True
		return False