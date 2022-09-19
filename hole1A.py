from constants import *
import copy

class HOLE1A():
	''' Establishes L1 + L2 + L3 + S < h1.
	
	This constraint guarantees that the 1st hole falls somewhere AFTER the 
	junction of nodes 3 & 4, and not on the junction itself.

	From the relation, the following inequalities can be derived:
	
	1) L1_max < h1 - (L2_min + L3_min + S)
	2) L2_max < h1 - (L1_min + L3_min + S)
	3) L3_max < h1 - (L1_min + L2_min + S)
	
	Note that on the right side of the inequalities, L1_min, L2_min, 
	and L3_min may be replaced with the assigned value for L1, L2, and 
	L3 respectively. However, when neither of them are assigned (or 
	is being assigned), their current lower bound is used.
	
	The algorithm performs the following assignments to make the boundaries
	consistnet:
		
 	from 1,	L1_max = h1 - (L2_min + L3_min + S) - 1
	from 2,	L2_max = h1 - (L1_min + L3_min + S) - 1
	from 3,	L3_max = h1 - (L1_min + L2_min + S) - 1
		
	h1 is the length of hole 1 from top, and S is the	minimum hole junction
	space between nodes 3 & 4 and the 1st hole.

	Note that we do not enforce any exact length for nodes. As long as
	the sum of all nodes add up to the desired length of the Ney, and 
	that the location of holes are gauranteed not to fall on
	the junctions between the nodes, we are able to make holes
	on their exact location.
	
	This constraint works with hole1B hand-in-hand to make sure that the
	first hole falls on node 4 and not no any junction.'''
	def __init__(self, spec):
		self.__h = spec["h1"]
		self.__space = spec["hmarg"] * 1
		self.__impact_map = {
			"L1": {"L2", "L3"},
			"L2": {"L1", "L3"},
			"L3": {"L1", "L2"}
		}
	
	def establish(self, csp, curvar, value):
		'''Establishes hole1A domain consistency.

		w.r.t. the assignment curvar: value.'''
		A = csp.get_assignment()
		ims = self.__impactables(A, curvar, self.__impact_map)
		if len(ims) == 0:
			return (DOMAINS_INTACT, set([]))
		D = csp.get_domains()
		lowers = self.__lowers(A, D, curvar, value)
		h = self.__h
		s = self.__space
		new_domains = self.__new_domains(D, lowers, ims, h, s)		
		return self.__update(csp, new_domains, ims)
	
	def propagate(self, csp, reduced_vars):
		'''Maintains bounds consistency for hole1A due to propagation.'''
		A = csp.get_assignment()
		ims = set([])
		for reduced_var in reduced_vars:
			_ims = self.__impactables(A, reduced_var, self.__impact_map)
			ims.update(_ims)
		if len(ims) == 0:
			return (DOMAINS_INTACT, set([]), set([]))
		D = csp.get_domains()
		lowers = self.__lowers(A, D)
		h = self.__h
		s = self.__space
		if self.__lowers_inconsistent(D, lowers, h, s):
			return (CONTRADICTION, ims, set([]))
		new_domains = self.__new_domains(D, lowers, ims, h, s)
		return self.__update(csp, new_domains, ims)
	
	def __lowers_inconsistent(self, D, lowers, h, s):
		'''Checks the consistency of variables' lower bounds.'''
		if lowers["L1"] >= h - lowers["L2"] - lowers["L3"] - s:
			return True
		if lowers["L2"] >= h - lowers["L1"] - lowers["L3"] - s:
			return True
		if lowers["L3"] >= h - lowers["L1"] - lowers["L2"] - s:
			return True
		return False
			
	def __lowers(self, A, D, curvar=None, value=None):
		'''A mathematical function.'''
		lowers = {}
		for var in {"L1", "L2", "L3"}:
			if var in A:
				lowers[var] = A[var]
			else:
				lowers[var] = D[var]["min"]
		if curvar != None:
			lowers[curvar] = value
		return lowers
		
	def __impactables(self, A, curvar, imap):
		'''A mathematical function.'''
		ims = set([])
		for var in imap[curvar]:
			if not var in A:
				ims.add(var)
		return ims
	
	def __inbounds(self, val, bounds):
 		return val >= bounds["min"] and val <= bounds["max"]
 	
	def __new_domains(self, D, lowers, ims, h, s):
		'''Carries out the assignments.
		
		This is a mathematical function.'''
		ups = {}
		if "L1" in ims:
			ups["L1"] = h - lowers["L2"] - lowers["L3"] - s - 1
		if "L2" in ims:
			ups["L2"] = h - lowers["L1"] - lowers["L3"] - s - 1
		if "L3" in ims:
			ups["L3"] = h - lowers["L1"] - lowers["L2"] - s - 1
		new_domains = {}			
		for var, new_upper in ups.items():
			if not self.__inbounds(new_upper, D[var]):
				return CONTRADICTION
			if new_upper < D[var]["max"]:
				new_domain = {"min": D[var]["min"], "max": new_upper}
				new_domains[var] = new_domain
		return new_domains
			
	def __update(self, csp, new_domains, ims):
		'''Carries out the final domain updates.'''
		if new_domains == CONTRADICTION:
			return (CONTRADICTION, ims, set([]), set([]))
		elif len(new_domains) > 0:
			for var, new_domain in new_domains.items():
				csp.update_domain(var, new_domain)
			return (DOMAINS_REDUCED, ims, set(new_domains.keys()))
		else:
			return (DOMAINS_INTACT, ims, set([]))
