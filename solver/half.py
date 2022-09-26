from constants import *
import math

class HALF():
	'''Implements consistency algorithm for l1_half_l2 constraint.'''

	def __init__(self, csp):
		self.__csp = csp
	
	def __new_L1_domain(self, d1, d2):
		'''Determines new bounds for L1 W.R.T. l1_half_l2 constraint.
		
		If new consistent bounds exists, it returns the new legal domain.
		This is a mathematical function.'''
		L1_current_size = d1["max"] - d1["min"]
		lowers = {1: d1["min"], 2: d2["min"]}
		uppers = {1: d1["max"], 2: d2["max"]}
		lower1 = max(lowers[1], math.ceil(lowers[2] / 2))
		upper1 = min(uppers[1], math.floor(uppers[2] / 2))
		if upper1 > d1["max"] or lower1 < d1["min"] or L1_new_size < 0:
			return CONTRADICTION
		elif L1_new_size == L1_current_size:
			return DOMAIN_INTACT
		elif L1_new_size < L1_current_size:
			new_domain = {"min": lower1, "max": upper1}
			return new_domain
			
	def __new_L2_domain(self, d1, d2):
		'''Determines new bounds for L2 W.R.T. l1_half_l2 constraint.
		
		If new consistent bounds exists, it returns the new legal domain.
		This is a mathematical function.'''
		L2_current_size = d2["max"] - d2["min"]
		lowers = {1: d1["min"], 2: d2["min"]}
		uppers = {1: d1["max"], 2: d2["max"]}		
		lower2 = max(lowers[2], lowers[1] * 2)
		upper2 = min(uppers[2], uppers[1] * 2)
		if upper2 > d2["max"] or lower2 < d2["min"] or L2_new_size < 0:
			return CONTRADICTION
		elif L2_new_size == L2_current_size:
			return DOMAIN_INTACT
		elif L2_new_size < L2_current_size:
			new_domain = {"min": lower2, "max": upper2}
			return new_domain
		
	def __L2_may_reduce(self, reduced_vars, A):
		'''Decides whether the domain of L2 may reduce or not.
		
		This is a mathematical function.'''
		return "L1" in reduced_vars and not "L2" in A
	
	def __L1_may_reduce(self, reduced_vars, A):
		'''Decides whether the domain of L1 may reduce or not.
		
		This is a mathematical function.'''
		return "L2" in reduced_vars and not "L1" in A
	
	def b_update(self, reduced_vars):
		'''Establishes indirect consistency W.R.T. l1_half_l2 constraint.
		
		If L1 is in the assignment, L2 is already made consistency
		in the establish function; hence, no further reduction would occur.

		These boundary updates happen if the domain of L1 is reduced:		

			lower2 = max(lower2, lower1*2)
			upper2 = min(upper2, upper1*2)
			
		and these updates happen if the domain of L2 is reduced:
		
			lower1 = max(lower1, lower2/2) 
			upper1 = min(upper1, upper2/2)
		
		Note: only one of the above updates happen. In case of
		contradiction, both reduced variables are involved. That's why
		reduced_vars is returned as the conflict set.
		'''
		A = self.__csp.get_assignment()
		D = self.__csp.get_domains()
		impacted = set([])
		res = DOMAI_INTACT
		if self.__L2_can_adjust(reduced_vars, A):
			new_L2_domain = self.__new_L2_domain(D["L1"], D["L2"])
			if new_L2_domain == CONTRADICTION:
				return (CONTRADICTION, reduced_vars, "l1_half_l2")
			elif new_L2_domain != DOMAIN_INTACT:
				impacted.add("L2")
				self.__csp.update_d("L2", new_L2_domain)
		elif self.__L1_can_adjust(reduced_vars, A):
			new_L1_domain = self.__new_L1_domain(D["L1"], D["L2"])
			if new_L1_domain == CONTRADICTION:
				return (CONTRADICTION, reduced_vars, "l1_half_l2")
			elif new_L1_domain != DOMAIN_INTACT:		
				impacted.add("L1")
				self.__csp.update_d("L1", new_L1_domain)
		if res == DOMAIN_INTACT:
			return (DOMAINS_INTACT, set([]))
		return (DOMAINS_REDUCED, impacted)
	
	def __has_impact(self, curvar):
		'''Checkes whether establishing consistency is possible.
		
		Upon assigning L1, there is an opportunity to reduce the domain of 
		L2.
		This is a mathematical function.'''
		return curvar == "L1"
		
	def establish(self, curvar, value):
		'''Establishes direct consistency W.R.T. l1_half_l2 constraint.
		
		The domain of L2 reduces to L1 * 2.
	
		If L1 is assigned a value, L2 reduces to one value only. However,
		the domain of L2 will still be represented via bounds, now with
		equal min & max.'''
		if not self.__has_impact(curvar):
			return (DOMAINS_INTACT, set([]))
		d1 = {"min": value, "max": value}
		D = self.__csp.get_domains()
		new_L2_domain = self.__new_L2_domain(d1, D["L2"])
		if new_L2_domain == CONTRADICTION:
			return (CONTRADICTION, {"L1"}, "l1_half_l2")
		elif new_L2_domain == DOMAIN_INTACT:
			return (DOMAINS_INTACT, set([]))
		self.__csp.update_d("L2", new_L2_domain)
		return (DOMAINS_REDUCED, {"L2"})
