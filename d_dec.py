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
	'''

	def __init__(self, csp):
		self.csp = csp
		self.ddiff = csp.spec["ddiff"]	

	def remove_illegals(self, asmnt, di, last_max):
		reduced = False
		for diameter in self.csp.D[di].copy():
			if diameter > last_max - self.ddiff["min"]:
				self.csp.D[di].remove(diameter)
				reduced = True
		return DOMAIN_REDUCED if reduced else DOMAIN_INTACT
		
	def _establish(self, asmnt, last_max, start):
		impacted = set([])
		for i in range(start, 8): # curvar up to D7
			di = "D"+str(i)
			if di in asmnt.assigned:
				diameter = asmnt.assignment[di]
				if diameter > last_max - self.ddiff["min"]:
					return (CONTRADICTION, set([]), "d_dec")
				break
			rresult = self.remove_illegals(asmnt, di, last_max)
			if rresult == DOMAIN_INTACT:
				break
			if rresult == DOMAIN_REDUCED:
				if len(self.csp.D[di]) == 0:
					return (CONTRADICTION, set([]), "d_dec")
				impacted.add(di)
			last_max = max(self.csp.D[di])
		if len(impacted) == 0:
			return (DOMAINS_INTACT, set([]))
		return (DOMAINS_REDUCED, impacted)
		
	def b_update(self, asmnt):
		'''Establishes indirect d_dec consistency.'''
		if "D1" in asmnt.assigned:
			last_max = asmnt.assignment["D1"]
		else:
			last_max = max(self.csp.D["D1"])
		return self._establish(asmnt, last_max, 2)		

	def establish(self, asmnt, curvar, value):
		'''Establishes direct d_dec consistency after assignment.
		
		The conflict occurs between assigned variables and the variable
		that is being assigned.
		'''
		last_max = value
		var_i = self.var_i(curvar)
		return self._establish(asmnt, last_max, var_i+1)
