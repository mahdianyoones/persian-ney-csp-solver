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
	
	def __init__(self, csp):
		self.__csp = csp		
		self.__h = csp.get_spec("h1")
		self.__space = csp.get_spec["hmarg"] * 1
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
		return {"h1", "h2", "h3"}.difference(ims)	
	
	def b_update(self, reduced_vars):
		'''Establishes h1 indirect consistency.'''
		A = self.__csp.get_assignment()
		ims = set([])
		for reduced_var in reduced_vars:
			_ims = self.__impactables(A, reduced_var, self.__impact_map)
			ims.update(_ims)
		return self.__establish(A, ims)
	
	def __establish(A, ims):
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
				return (CONTRADICTION, self.__confset(ims), "h1")
			if new_upper < D[var]["max"]:
				impacted.add(var)
				new_domain = {"min": D[var]["min"], "max": new_upper}
				self.__csp.update_d(var, new_domain)
		if len(impacted) == 0:
			return (DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, set([]))
				
	def establish(self, curvar, value):
		'''Establishes h1 direct consistency.

		The following inequality must hold:
		L1 + L2 + L3 + 10 < h1.
		
		From the above, the following updates are done:
		
	 	upper1 = h1 - (lower2 + lower3 + 10)
		upper2 = h1 - (lower1 + lower3 + 10)
		upper3 = h1 - (lower1 + lower2 + 10)
		'''
		A = self.__csp.get_assignment()
		ims = self.__impactables(A, curvar, self.__impact_map)
		return self.__establish(A, ims)
