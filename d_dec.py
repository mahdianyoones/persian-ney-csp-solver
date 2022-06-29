from constants import *

class D_DEC():
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
	
	def var_i(self, var):
		if var[0] in {"R", "D"}:
			return int(var[1])
		else:
			return int(var[2])
	
	def var_name(self, var):
		if len(var) == 2:
			return var[0]
		else:
			return var[0:2]
	
	def _establish(self, last_max, start):
		impacted = set([])
		ddiff = self.csp.spec["ddiff"]	
		for i in range(start, 8): # curvar up to D7
			di = "D"+str(i)
			for v in self.csp.D[di].copy():
				upper = last_max - ddiff["min"]
				if v > upper:
					impacted.add(di)
					self.csp.D[di].remove(v)
			if len(impacted) == 0:
				break # stop propagating nothing!
			if len(self.csp.D[di]) == 0:
				return (CONTRADICTION, set([]))
			last_max = max(self.csp.D[di])
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, None)
		
	def b_update(self, asmnt):
		d = sorted(self.csp.D["D1"])
		last_max = max(self.csp.D["D1"])
		return self._establish(last_max, 2)		
					
	def establish(self, asmnt, curvar, value):
		last_max = value
		var_i = self.var_i(curvar)
		return self._establish(last_max, var_i+1)
