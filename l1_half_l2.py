from constants import *
from base import BASE
import math

class L1_HALF_L2(BASE):
	'''Implements consistency algorithm for l1_half_l2 constraint.'''

	def __init__(self, csp, asmnt):
		self.__csp = csp
		self.__asmnt = asmnt
	
	def __adjust_L2(self, d1):
		d2 = self.csp.D["L2"]
		lowers = {1: d1["min"], 2: d2["min"]}
		uppers = {1: d1["max"], 2: d2["max"]}
		impacted = False
		contradiction = False
		L2_current_size = d2["max"] - d2["min"]
		lower2 = max(lowers[2], lowers[1] * 2)
		upper2 = min(uppers[2], uppers[1] * 2)
		L2_new_size = upper2 - lower2
		if upper2 > d2["max"] or lower2 < d2["min"] or L2_new_size < 0:
			contradiction = True
		elif L2_new_size < L2_current_size:
			self.csp.D["L2"] = {"min": lower2, "max": upper2}
			impacted = True
		return (contradiction, impacted)

	def __adjust_L1(self, d2):
		d1 = self.csp.D["L1"]	
		lowers = {1: d1["min"], 2: d2["min"]}
		uppers = {1: d1["max"], 2: d2["max"]}
		impacted = False
		contradiction = False	
		L1_current_size = d1["max"] - d1["min"]
		lower1 = max(lowers[1], math.ceil(lowers[2] / 2))
		upper1 = min(uppers[1], math.floor(uppers[2] / 2))
		L1_new_size = upper1 - lower1
		if upper1 > d1["max"] or lower1 < d1["min"] or L1_new_size < 0:
			contradiction = True
		elif L1_new_size < L1_current_size:
			self.csp.D["L1"] = {"min": lower1, "max": upper1}
			impacted = True
		return (contradiction, impacted)
	
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
		if ‌"L1" in reduced_vars:
			if "L2" in self.asmnt.assigned:
				raise Exception("L2 is already in the assignment.")			
			d1 = self.csp.D["L1"]
			(contradiction, impacted) = self.adjust_L2(d1)
			impacted = set(["L2"])
		elif "L2" in reduced_vars:
			if "L1" in self.asmnt.assigned:
				raise Exception("L1 is already in the assignment.")			
			d2 = self.csp.D["L2"]
			(contradiction, impacted) = self.adjust_L1(d2)
			impacted = set(["L1"])
		if contradiction:
			return (CONTRADICTION, set([]), "l1_half_l2")
		if impacted:
			return (DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, set([]))
									
	def establish(self, curvar, value):
		'''Establishes direct consistency W.R.T. l1_half_l2 constraint.
		
		The domain of L2 reduces to L1 * 2.
	
		If L1 is assigned a value, L2 reduces to one value only. However,
		the domain of L2 will still be represented via bounds, now with
		equal min & max.'''
		if curvar == "L2":
			return (DOMAINS_INTACT, set([]))
		if "L2" in self.asmnt.assigned:
			raise Exception("L2 is already in the assignment.")
		d1 = {"min": value, "max": value}
		(contradiction, impacted) = self.adjust_L2(d1)
		if contradiction:
			return (CONTRADICTION, set(["L1"]), "l1_half_l2")
		if impacted:
			return (DOMAINS_REDUCED, set(["L2"]))
		return (DOMAINS_INTACT, set([]))
