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
		'''Removes inconsistent values from all D variables W.R.T. d_dec.
		
		(CONTRADICTION, i) means Di variable has run out of values.'''
		impacted = set([])
		for i in range(start, 8): # curvar up to D7
			di = "D"+str(i)
			rresult = self.remove_illegals(di, last_max)
			if rresult == DOMAIN_INTACT:
				break
			if rresult == DOMAIN_REDUCED:
				if len(self.csp.D[di]) == 0:
					return (CONTRADICTION, i)
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
		
	def establish(self, curvar, value):
		'''Establishes direct d_dec consistency after assignment.
		
		e.g.
		
		If D1 and D2 are assigned and contradiction occurs for D5 (it runs 
		out of values), confset = {D1, D2}.
		
		We cannot tell whether other variables (Rs, Ths, and Ls) are
		responsible for this contradiction or not.
		'''
		last_max = value
		var_i = self.var_i(curvar)
		res = self._establish(last_max, var_i+1)
		if res[0] != CONTRADICTION:
			return res
		confset = set([])
		for i in range(1, res[1]):
			di = "D"+str(i)
			if di in self.asmnt.assigned:
				confset.add(di)
		return (CONTRADICTION, confset, "d_dec")
