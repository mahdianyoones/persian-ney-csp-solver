from constants import *
import copy

class HOLE4():
	''' Establishes h4 consistency for L1, L2, L3, and L4.
	
	This constraints guarantees that the 4th hole falls on the node 5 below the
	3rd hole. The relation L1 + L2 + L3 + L4 + 30 < h4 must hold for a 
	consistent assignment.
	
	h4 in the above relation is the length of hole 4 from top, and 30 is the
	minimum space required between the junction of nodes 4&5 and the 4th
	hole.
	
	Direct updates:

		upper1 = h4 - ( lower2 + lower3 + lower4 + 30)
		upper2 = h4 - ( lower1 + lower3 + lower4 + 30)
		upper3 = h4 - ( lower1 + lower2 + lower4 + 30)
		upper4 = h4 - ( lower1 + lower2 + lower3 + 30)
	
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
	def __init__(self, csp):
		self.__csp = csp		
		self.__h = csp.get_spec("h4")
		self.__space = csp.get_spec["hmarg"] * 2
		self.__space += csp.get_spec["holed"] * 1
		self.__impact_map = {
			"L1": {"L2", "L3", "L4"},
			"L2": {"L1", "L3", "L4"},
			"L3": {"L1", "L2", "L4"},
			"L4": {"L1", "L2", "L3"}		
		}
	
	def __lowers(self, A, D):
		'''A mathematical function.'''
		lowers = {}
		for var in {"L1", "L2", "L3", "L4"}:
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
	
	def __new_uppers(self, lws, ims, h, s):
		'''A mathematical function.'''
		ups = {}
		if "L1" in ims:
			ups["L1"] = h-(lws["L2"]+lws["L3"]+lws["L4"]+s)
		if "L2" in ims:
			ups["L2"] = h-(lws["L1"]+lws["L3"]+lws["L4"]+s)
		if "L3" in ims:
			ups["L3"] = h-(lws["L1"]+lws["L2"]+lws["L4"]+s)
		if "L4" in ims:
			ups["L4"] = h-(lws["L1"]+lws["L2"]+lws["L3"]+s)
		return ups
	
	def __confset(self, ims):
		return {"L1", "L2", "L3", "L4"}.difference(ims)	
	
	def b_update(self, reduced_vars):
		'''Establishes h4 indirect consistency.'''
		A = self.__csp.get_assignment()
		ims = set([])
		for reduced_var in reduced_vars:
			_ims = self.__impactables(A, reduced_var, self.__impact_map)
			ims.update(_ims)
		return self.__establish(A, ims)
	
	def __establish(A, ims):
		'''Implements both direct and indirect consistency for h4.'''	
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
				return (CONTRADICTION, self.__confset(ims), "h4")
			if new_upper < D[var]["max"]:
				impacted.add(var)
				new_domain = {"min": D[var]["min"], "max": new_upper}
				self.__csp.update_d(var, new_domain)
		if len(impacted) == 0:
			return (DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, set([]))
				
	def establish(self, curvar, value):
		'''Establishes h4 direct consistency.'''
		A = self.__csp.get_assignment()
		ims = self.__impactables(A, curvar, self.__impact_map)
		return self.__establish(A, ims)
