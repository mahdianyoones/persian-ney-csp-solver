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

	def __init__(self, csp, asmnt):
		self.csp = csp
		self.ddiff = csp.spec["ddiff"]
		self.asmnt = asmnt	

	def remove_illegals(self, di, last_max):
		reduced = False
		for diameter in self.csp.D[di].copy():
			if diameter > last_max - self.ddiff["min"]:
				self.csp.D[di].remove(diameter)
				reduced = True
		return DOMAIN_REDUCED if reduced else DOMAIN_INTACT
		
	def _establish(self, last_max, start):
		impacted = set([])
		for i in range(start, 8): # curvar up to D7
			di = "D"+str(i)
			rresult = self.remove_illegals(di, last_max)
			if rresult == DOMAIN_INTACT:
				break
			if rresult == DOMAIN_REDUCED:
				if len(self.csp.D[di]) == 0:
					return (CONTRADICTION, None)
				impacted.add(di)
			last_max = max(self.csp.D[di])
		if len(impacted) == 0:
			return (DOMAINS_INTACT, set([]))
		return (DOMAINS_REDUCED, impacted)
	
	def b_update(self):
		'''Establishes indirect d_dec consistency.'''
		if "D1" in self.asmnt.assigned:
			last_max = self.asmnt.assignment["D1"]
		else:
			last_max = max(self.csp.D["D1"])
		res = self._establish(last_max, 2)
		if res[0] != CONTRADICTION:
			return res
		return (CONTRADICTION, set([]), "d_dec")

	def confset(self, curvar_i):
		i = str(curvar_i)
		confset = {"D"+i}
		if "TH"+i in self.asmnt.assigned:
			confset.add("TH"+i)
		if "R"+i in self.asmnt.assigned:
			confset.add("R"+i)
		return confset
		
	def establish(self, curvar, value):
		'''Establishes direct d_dec consistency after assignment.
		
		The conflict occurs between assigned variables and the variable
		that is being assigned.
		'''
		last_max = value
		var_i = self.var_i(curvar)
		res = self._establish(last_max, var_i+1)
		if res[0] != CONTRADICTION:
			return res
		return (CONTRADICTION, self.confset(var_i), "d_dec")
