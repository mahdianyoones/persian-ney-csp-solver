from constants import *
from base import BASE
import copy

class D_DEC(BASE):
	'''Implements diameter decrement consistency.
	
	 0.5 <= D2 - D1 <= 1
	 0.5 <= D3 - D2 <= 1
	 0.5 <= D4 - D3 <= 1
	 0.5 <= D5 - D4 <= 1
	 0.5 <= D6 - D5 <= 1
	 0.5 <= D7 - D6 <= 1
	 
	 0.5 and 1 are subject to ney_spec.
	 
	 Inconsistent values can be removed from all D variables in one go.		
	 
	 Bound propagation is done this way:
	 	remove from Di if 
	 		value < min(Di-1) - 1 
	 		or 
	 		value > max(Di-1) - 0.5
	'''

	def __init__(self, csp):
		self.csp = csp
		self.ddiff = csp.spec["ddiff"]	

	def remove_illegals(self, di, last_max):
		dcopy = self.csp.D[di].copy()
		for diameter in dcopy:
			if diameter > last_max - self.ddiff["min"]:
				self.csp.remove_val(di, diameter)
		if len(dcopy) > len(self.csp.D[di]):
			return DOMAIN_REDUCED
		return DOMAIN_INTACT
		
	def _establish(self, asmnt, last_max, start):
		impacted = set([])
		for i in range(start, 8): # curvar up to D7
			di = "D"+str(i)
			if di in asmnt.assigned:
				break 							# the rest are OK
			if self.remove_illegals(di, last_max) == DOMAIN_REDUCED:
				impacted.add(di)
			if len(impacted) == 0:
				break 							# the rest won't change
			if len(self.csp.D[di]) == 0:
				return (CONTRADICTION, set([]))
			last_max = max(self.csp.D[di])
		if len(impacted) == 0:
			return (DOMAINS_INTACT, set([]))
		return (DOMAINS_REDUCED, impacted)
		
	def b_update(self, asmnt):
		if "D1" in asmnt.assigned:
			last_max = asmnt.assignment["D1"]
		else:
			last_max = max(self.csp.D["D1"])
		return self._establish(asmnt, last_max, 2)		
					
	def establish(self, asmnt, curvar, value):
		last_max = value
		var_i = self.var_i(curvar)
		res = self._establish(asmnt, last_max, var_i+1)
		return res
