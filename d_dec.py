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

	def remove_illegals(self, asmnt, di, last_max):
		if di in asmnt.assigned:
			diameter = asmnt.assignment[di]
			if diameter > last_max - self.ddiff["min"]:
				return (CONTRADICTION, {di})
			else:
				return (DOMAIN_INTACT, asmnt.assignment[di])
		dcopy = copy.deepcopy(self.csp.D[di])
		for diameter in dcopy:
			if diameter > last_max - self.ddiff["min"]:
				self.csp.remove_val(di, diameter)
		if len(dcopy) > len(self.csp.D[di]):
			return (DOMAIN_REDUCED, max(self.csp.D[di]))
		return (DOMAIN_INTACT, max(self.csp.D[di]))
		
	def _establish(self, asmnt, last_max, start):
		impacted = set([])
		for i in range(start, 8): # curvar up to D7
			di = "D"+str(i)
			rresult = self.remove_illegals(asmnt, di, last_max)
			if rresult[0] == CONTRADICTION or len(self.csp.D[di]) == 0:
				return (CONTRADICTION, rresult[1])
			if rresult[0] == DOMAIN_REDUCED:
				impacted.add(di)
			last_max = rresult[1]
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
		return self._establish(asmnt, last_max, var_i+1)
