from constants import *
import copy

class HOLE2():
	'''Establishes h2 consistency for L1, L2, and L3.
	
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

		that is, if lower bound of L1 (i.e. D["L1"]["min"]) is reduced
		then, upper bounds of L2 and L3 could be impacted.		
	'''
	def __init__(self, csp):
		self.__csp = csp		
		self.__h = csp.get_spec("h2")
		self.__space = csp.get_spec["hmarg"] * 2
		self.__space += self.csp.spec["holed"] * 1
		self.__impact_map = {
			"L1": {"L2", "L3"},
			"L2": {"L1", "L3"},
			"L3": {"L1", "L2"}
		}
	
	def __lowers(self, A, D):
		'''A mathematical function.'''
		lowers = {}
		for var in {"L1", "L2", "L3"}:
			if var in A:
				lowers[var] = A[var]
			else:
				lowers[var] = D[var]["min"]
		return lowers
	
	def __impactables(self, A, curvar, imap):
		'''A mathematical function.'''
		ims = {}
		for var in imap[curvar]:
			if not var in A:
				ims.add(var)
		return ims
	
	def __new_uppers(self, lowers, ims, h, s):
		'''A mathematical function.'''
		ups = {}
		if "L1" in ims:
			ups["L1"] = h - (lowers["L2"] + lowers["L3"] + s)
		if "L2" in ims:
			ups["L2"] = h - (lowers["L1"] + lowers["L3"] + s)
		if "L3" in ims:
			ups["L3"] = h - (lowers["L1"] + lowers["L2"] + s)
		return ups
	
	def __confset(self, ims):
		return {"L1", "L2", "L3"}.difference(ims)	
	
	def b_update(self, reduced_vars):
		'''Establishes h2 indirect consistency.'''
		A = self.__csp.get_assignment()
		ims = set([])
		for reduced_var in reduced_vars:
			_ims = self.__impactables(A, reduced_var, self.__impact_map)
			ims.update(_ims)
		return self.__establish(A, ims)
	
	def __establish(A, ims):
		'''Implements both direct and indirect consistency for h2.'''
		if len(ims) == 0:
			return (DIMAINS_INTACT, set([]))
		D = self.__csp.get_domains()
		lowers = self.__lowers(A, D)
		h = self.__h
		s = self.__space
		new_uppers = self.__new_uppers(lowers, ims, h, s)
		impacted = set([])
		for var, new_upper in new_uppers.items():
			if new_upper < D[var]["min"]:
				return (CONTRADICTION, self.__confset(ims), "h2")
			if new_upper < D[var]["max"]:
				impacted.add(var)
				new_domain = {"min": D[var]["min"], "max": new_upper}
				self.__csp.update_d(var, new_domain)
		if len(impacted) == 0:
			return (DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, set([]))
				
	def establish(self, curvar, value):
		'''Establishes h2 direct consistency.'''
		A = self.__csp.get_assignment()
		ims = self.__impactables(A, curvar, self.__impact_map)
		return self.__establish(A, ims)		
