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
		self.__csp = csp
		self.__ddiff = csp.spec["ddiff"]
		self.__asmnt = asmnt	
		
	def __establish(self):
		'''Removes inconsistent values from all D variables W.R.T. d_dec.'''
		impacted = set([])
		confset = set([])
		contradiction = False
		for i in range(1, 8):
			di = "D"+str(i)
			if di in self.asmnt.assigned:
				confset.add(di)
				last_max = self.asmnt.assignment[di]
				continue
			reduced = False
			for diameter in self.csp.D[di].copy():
				if diameter > last_max - self.ddiff["min"]:
					self.csp.D[di].remove(diameter)
					impacted.add(di)
					reduced = True
			if not reduced:
				break
			if len(self.csp.D[di]) == 0:
				contradiction = True
				break
			last_max = max(self.csp.D[di])
		return (contradiction, confset, impacted)
	
	def b_update(self):
		'''Establishes indirect d_dec consistency.'''
		(contradiction, confset, impacted) = self._establish()
		if contradiction:
			return (CONTRADICTION, set([]), "d_dec")
		if len(impacted) > 0:
			(DOMAINS_REDUCED, impacted)	
		return (DOMAINS_INTACT, set([]))
		
	def establish(self, curvar, value):
		'''Establishes direct d_dec consistency after assignment.
		
		e.g.
		
		If D1 and D2 are assigned and contradiction occurs for D5 (it runs 
		out of values), confset = {D1, D2}.
		
		We cannot tell whether other variables (Rs, Ths, and Ls) are
		responsible for this contradiction or not.
		'''
		(contradiction, confset, impacted) = self._establish()
		if contradiction:
			return (CONTRADICTION, confset, "d_dec")
		if len(impacted) > 0:
			(DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, set([]))
