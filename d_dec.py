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
		
	def establish(self, asmnt, curvar, value):
		impacted = set([])
		if value != None:
			last_max = value
			last_min = value
		else:
			d = sorted(self.csp.D[curvar], reverse=True)
			last_max = d[-1]
			last_min = d[0]
		ddiff = self.csp.spec["ddiff"]
		for i in range(int(curvar[1])+1, 8): # curvar up to D7
			di = "D"+str(i)
			d = self.csp.D[di]
			new_max = float("-inf")
			new_min = float("+inf")
			for v in d.copy():
				if v < last_min - ddiff["max"] or v > last_max - ddiff["min"]:
					impacted.add(di)
					d.remove(v)
				elif v > new_max:
					new_max = v
				elif v < new_min:
					new_min = v
			if len(impacted) == 0:
				break # stop propagating nothing!
			if len(d) == 0:
				return (CONTRADICTION, set([]))
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)
		else:
			return (DOMAINS_INTACT, None)
