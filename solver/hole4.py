from constants import *
import copy

class HOLE4():
	'''Establishes L1 + L2 + L3 + L4 + S < h4.
	
	S = hole_margin * 2 + hole_diameter * 1
	
	This constraint guarantees that the 4th hole falls somewhere AFTER the 
	3rd hole and on node 5.
	
	From the relation, the following inequalities can be derived:
	
	1) L1_max < h4 - L2_min - L3_min - L4_min - S
	2) L2_max < h4 - L1_min - L3_min - L4_min - S
	3) L3_max < h4 - L1_min - L2_min - L4_min - S
	4) L4_max < h4 - L1_min - L2_min - L3_min - S
	
	Note that on the right side of the inequalities, L1_min, L2_min, L3_min, 
	and L4_min may be replaced with the assigned value for L1, L2, L3, and L4 
	respectively.
	
	However, when neither of them are assigned (or is being assigned), their
	current lower bound is used.

	The algorithm performs the following assignments to make the boundaries
	consistent:
		
 	from 1,	L1_max = h4 - L2_min - L3_min - L4_min - S - 1
	from 2,	L2_max = h4 - L1_min - L3_min - L4_min - S - 1
	from 3,	L3_max = h4 - L1_min - L2_min - L4_min - S - 1
	from 4,	L4_max = h4 - L1_min - L2_min - L3_min - S - 1
		
	h4 is the length of hole 3 from top, and S is the minimum hole junction
	space between nodes 4 & 5 and the 3st hole.

	Note that we do not enforce any exact length for nodes. As long as
	the sum of all nodes add up to the desired length of the Ney, and 
	that the location of holes are gauranteed not to fall on
	the junctions between the nodes, we are able to make holes
	on their exact location.'''

	def __init__(self, spec):
		self.__h = spec["h4"]
		self.__space = spec["hmarg"] * 2
		self.__space += spec["holed"] * 1
		self.__impact_map = {
			"L1": {"L2", "L3", "L4"},
			"L2": {"L1", "L3", "L4"},
			"L3": {"L1", "L2", "L4"},
			"L4": {"L1", "L2", "L3"}		
		}

	def establish(self, csp, curvar, value):
		'''Establishes hole4 domain consistency.

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
		'''Maintains bounds consistency for hole4 due to propagation.'''
		A = csp.get_assignment()
		ims = set([])
		for reduced_var in reduced_vars:
			_ims = self.__impactables(A, reduced_var, self.__impact_map)
			ims.update(_ims)
		if len(ims) == 0:
			return (DOMAINS_INTACT, set([]))
		D = csp.get_domains()
		lowers = self.__lowers(A, D)
		h = self.__h
		s = self.__space
		if self.__lowers_inconsistent(lowers, h, s):
			return (CONTRADICTION, ims, set([]))
		new_domains = self.__new_domains(D, lowers, ims, h, s)
		return self.__update(csp, new_domains, ims)
	
	def __lowers_inconsistent(self, lows, h, s):
		'''Checks the consistency of variables' lower bounds.
		
		If the lower bounds are inconsistent, it is a contradiction.

		This is a mathematical function.'''
		if lows["L1"] >= h - lows["L2"] - lows["L3"] - lows["L4"] - s:
			return True
		if lows["L2"] >= h - lows["L1"] - lows["L3"] - lows["L4"] - s:
			return True
		if lows["L3"] >= h - lows["L1"] - lows["L2"] - lows["L4"] - s:
			return True
		if lows["L4"] >= h - lows["L1"] - lows["L2"] - lows["L3"] - s:
			return True
		return False
			
	def __lowers(self, A, D, curvar=None, value=None):
		'''A mathematical function.'''
		lowers = {}
		for var in {"L1", "L2", "L3", "L4"}:
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
 	
	def __new_domains(self, D, lows, ims, h, s):
		'''Carries out the assignments.
		
		This is a mathematical function.'''
		ups = {}
		if "L1" in ims:
			ups["L1"] = h - lows["L2"] - lows["L3"] - lows["L4"] - s - 1
		if "L2" in ims:
			ups["L2"] = h - lows["L1"] - lows["L3"] - lows["L4"] - s - 1
		if "L3" in ims:
			ups["L3"] = h - lows["L1"] - lows["L2"] - lows["L4"] - s - 1
		if "L4" in ims:
			ups["L4"] = h - lows["L1"] - lows["L2"] - lows["L3"] - s - 1
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
			return (CONTRADICTION, ims)
		elif len(new_domains) > 0:
			for var, new_domain in new_domains.items():
				csp.update_domain(var, new_domain)
			return (DOMAINS_REDUCED, ims, set(new_domains.keys()))
		else:
			return (DOMAINS_INTACT, ims)