from constants import *
import copy

class HOLE1B():
	'''Establishes L1 + L2 + L3 + L4 - S > h1.
	
	This constraint gauranteed that hole 1 falls somewhere BEFORE 
	the junction of nodes 4 & 5, and not on the junction.

	If possible, we can only update the lower bounds on the domains. 
	
	From the relation, the following inequalities can be derived:
	
	1) L1_min > h1 - (L2_max + L3_max + L4_max - S)
	2) L2_min > h1 - (L1_max + L3_max + L4_max - S)
	3) L3_min > h1 - (L2_max + L1_max + L4_max - S)
	4) L4_min > h1 - (L2_max + L3_max + L1_max - S)
	
	The algorithm performs the following assignments to make the boundaries
	consistnet:
	
	from 1, 	L1_min = h1 - (L2_max + L3_max + L4_max - S) + 1
	from 2, 	L2_min = h1 - (L1_max + L3_max + L4_max - S) + 1 
	from 3, 	L3_min = h1 - (L2_max + L1_max + L4_max - S) + 1
	from 4, 	L4_min = h1 - (L2_max + L3_max + L1_max - S) + 1
				
	h1 in the above relations is the length of hole 1 from top, and S is the
	minimum hole junction space between nodes 4 & 5 and the 1st hole.

	Note that we do not enforce any exact length for nodes. As long as
	the sum of all nodes add up to the desired length of the Ney, and 
	that the location of holes are gauranteed not to fall on
	the junctions between the nodes, we are able to build holes
	on their exact location.
	
	This constraint works with hole1A hand-in-hand to make sure that the
	first hole falls on node 4 and not on any junction.'''
	def __init__(self, spec):
		self.__h = spec["h1"]
		self.__space = spec["hmarg"] * 1
		self.__impact_map = {
			"L1": {"L2", "L3", "L4"},
			"L2": {"L1", "L3", "L4"},
			"L3": {"L1", "L2", "L4"},
			"L4": {"L1", "L2", "L3"}
		}
	
	def establish(self, csp, curvar, value):
		'''Establishes hole1B domain consistency.
		
		w.r.t. the assignment curvar: value.'''
		A = csp.get_assignment()
		ims = self.__impactables(A, curvar, self.__impact_map)
		if len(ims) == 0:
			return (DOMAINS_INTACT, set([]))
		D = csp.get_domains()
		uppers = self.__uppers(A, D, curvar, value)
		h = self.__h
		s = self.__space
		new_domains = self.__new_domains(D, uppers, ims, h, s)		
		return self.__update(csp, new_domains, ims)
		
	def propagate(self, csp, reduced_vars):
		'''Maintains bounds consistency for hole1B due to propagation.'''
		A = csp.get_assignment()
		ims = set([])
		for reduced_var in reduced_vars:
			_ims = self.__impactables(A, reduced_var, self.__impact_map)
			ims.update(_ims)
		if len(ims) == 0:
			return (DOMAINS_INTACT, set([]))
		D = csp.get_domains()
		uppers = self.__uppers(A, D)
		h = self.__h
		s = self.__space
		if self.__uppers_inconsistent(D, uppers, h, s):
			return (CONTRADICTION, ims)		
		new_domains = self.__new_domains(D, uppers, ims, h, s)
		return self.__update(csp, new_domains, ims)
	
	def __uppers_inconsistent(self, D, ups, h, s):
		'''Checks the consistency of variables' upper bounds.'''
		if ups["L1"] <= h - ups["L2"] - ups["L3"] - ups["L4"] - s:
			return True
		if ups["L2"] <= h - ups["L1"] - ups["L3"] - ups["L4"] - s:
			return True
		if ups["L3"] <= h - ups["L1"] - ups["L2"] - ups["L4"] - s:
			return True
		if ups["L4"] <= h - ups["L1"] - ups["L2"] - ups["L3"] - s:
			return True
		return False
	
	def __uppers(self, A, D, curvar=None, value=None):
		'''A mathematical function.'''
		uppers = {}
		for var in {"L1", "L2", "L3", "L4"}:
			if var in A:
				uppers[var] = A[var]
			else:
				uppers[var] = D[var]["max"]
		if curvar != None:
			uppers[curvar] = value
		return uppers
	
	def __impactables(self, A, curvar, imap):
		'''A mathematical function.'''
		ims = set([])
		for var in imap[curvar]:
			if not var in A:
				ims.add(var)
		return ims
	
	def __inbounds(self, val, bounds):
 		return val >= bounds["min"] and val <= bounds["max"]
	
	def __new_domains(self, D, ups, ims, h, s):
		'''Carries out the assignments.
		
		This is a mathematical function.'''
		lows = {}
		if "L1" in ims:
			lows["L1"] = h - ups["L2"] - ups["L3"] - ups["L4"] - s + 1
		if "L2" in ims:
			lows["L2"] = h - ups["L1"] - ups["L3"] - ups["L4"] - s + 1
		if "L3" in ims:
			lows["L3"] = h - ups["L1"] - ups["L2"] - ups["L4"] - s + 1
		if "L4" in ims:
			lows["L4"] = h - ups["L1"] - ups["L2"] - ups["L3"] - s + 1
		new_domains = {}
		for var, new_lower in lows.items():
			if not self.__inbounds(new_lower, D[var]):
				return CONTRADICTION
			if new_lower > D[var]["min"]:
				new_domain = {"min": new_lower, "max": D[var]["max"]}
				new_domains[var] = new_domain
		return new_domains
	
	def __update(self, csp, new_domains, ims):
		'''Carries out the final domain updates.'''
		if new_domains == CONTRADICTION:
			return (CONTRADICTION, ims)
		elif len(new_domains) > 0:
			for var, new_domain in new_domains.items():
				csp.update_domain(var, new_domain)
			return (DOMAINS_REDUCED, ims, set(new_domains.keys()))
		else:
			return (DOMAINS_INTACT, ims)	
