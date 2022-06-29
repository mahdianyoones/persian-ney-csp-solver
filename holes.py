from constants import *

class HOLES():
	'''Establishes consistency W.R.T h1, h2, h3, h4, h5, h6 constraints.
	
	These relations must hold:
	
	 1. L1 + L2 + L3 + 10 < h1	
	 
	 	1st hole must fall on node 4
	 
	 2. L1 + L2 + L3 + 30 < h2
	 
	 	2nd hole must fall on node 4 below 1st hole

	 3. L1 + L2 + L3 + L4 + 10 < h3
	 
	 	3rd hole must fall at the beginning of node 5

	 4. L1 + L2 + L3 + L4 + 30 < h4

		4th hole must fall on node 5 below 3rd hole

	 5. L1 + L2 + L3 + L4 + 50 < h5
	 
	 	5th hole must fall on node 5 below 4th hole

	 6. L1 + L2 + L3 + L4 + L5 + 10 < h6
	 
	 	6th hole must fall on node 6
	 	
	 Updates:
	 
			1. h1		 	

			 	upper1 = h1 - (lower2 + lower3 + 10)
				upper2 = h1 - (lower1 + lower3 + 10)
				upper3 = h1 - (lower1 + lower2 + 10)

			2. h2

				upper1 = h2 - (lower2 + lower3 + 30)
				upper2 = h2 - (lower1 + lower3 + 30)
				upper3 = h2 - (lower1 + lower2 + 30)
			
			3. h3
			
				upper1 = h3 - ( lower2 + lower3 + lower4 + 10)
				upper2 = h3 - ( lower1 + lower3 + lower4 + 10)
				upper3 = h3 - ( lower1 + lower2 + lower4 + 10)
				upper4 = h3 - ( lower1 + lower2 + lower3 + 10)
			
			4. h4
			
				upper1 = h4 - ( lower2 + lower3 + lower4 + 30)
				upper2 = h4 - ( lower1 + lower3 + lower4 + 30)
				upper3 = h4 - ( lower1 + lower2 + lower4 + 30)
				upper4 = h4 - ( lower1 + lower2 + lower3 + 30)
					
			5. h5
			
				upper1 = h5 - ( lower2 + lower3 + lower4 + 50)
				upper2 = h5 - ( lower1 + lower3 + lower4 + 50)
				upper3 = h5 - ( lower1 + lower2 + lower4 + 50)
				upper4 = h5 - ( lower1 + lower2 + lower3 + 50)
			
			6. h6
			
				upper1 = h6 - (lower2+lower3+lower4+lower5+10)
				upper2 = h6 - (lower1+lower3+lower4+lower5+10)
				upper3 = h6 - (lower1+lower2+lower4+lower5+10)
				upper4 = h6 - (lower1+lower2+lower3+lower5+10)
				upper5 = h6 - (lower1+lower2+lower3+lower4+10)
			
 	Propagations:

			due to h1, h2

				lower1 -> 	   upper2, upper3
				lower2 -> upper1,         upper3
				lower3 -> upper1, upper2
			
			due to h3, h4, h5
			
		 		lower1 ->         upper2, upper3, upper4
		 		lower2 -> upper1,         upper3, upper4
		 		lower3 -> upper1, upper2,         upper4
		 		lower4 -> upper1, upper2, upper3

			due to h6
			
		 		lower1 ->         upper2, upper3, upper4, upper5
		 		lower2 -> upper1,         upper3, upper4, upper5
		 		lower3 -> upper1, upper2,         upper4, upper5
		 		lower4 -> upper1, upper2, upper3,	       upper5
		 		lower5 -> upper1, upper2, upper3, upper4
	
	Note: "lower1 -> upper2, upper3" means if lower1 changes, upper2 and
	upper3 are impacted hence must be updated.
	
	When the lower bound of an L variable (L1 to L5) reduces, the upper
	bound of other L variables (L1 to L5) are impacted.
	
	All relations together:
	
	L1 + L2 + L3 + 10 			< h1
	L1 + L2 + L3 + 30 			< h2
	L1 + L2 + L3 + L4 + 10 		< h3
	L1 + L2 + L3 + L4 + 30 		< h4
	L1 + L2 + L3 + L4 + 50 		< h5
	L1 + L2 + L3 + L4 + L5 + 10 	< h6
	'''
	
	def __init__(self, csp):
		self.csp = csp
		spec = csp.spec
		hmarg = spec["hmarg"]
		holed = self.csp.spec["holed"]
		self.spaces = [ None, hmarg * 1, hmarg * 2 + holed * 1, hmarg * 1, 
			hmarg * 2 + holed * 1, hmarg * 3 + holed * 2, hmarg * 1]
		self.holes = [None, spec["h1"], spec["h2"], spec["h3"], spec["h4"], 
			spec["h5"], spec["h6"]]
	
	def update_uppers(self, n, var_i, uppers, lows, ds, h, s):
		confset = set([])	
		for k in range(1, n+1):
			lk = "L"+str(k)
			# update all except kth L
			if var_i != k and not lk in self.asmnt.assigned:
				old = ds[k]["max"]
				_sum = sum([lows[u] for u in range(1, n+1) if u != k])
				uppers[k] = min(uppers[k], old, h-(_sum + s))
				confset.update(set(["L"+str(v) for v in range(1, n+1) if v != k]))
		return confset

	def var_i(self, var):
		if var[0] in {"R", "D", "L"}:
			return var[1]
		else:
			return var[2]
	
	def var_name(self, var):
		if len(var) == 2:
			return var[0]
		else:
			return var[0:2]
		
	def domains(self, curvar, value):
		'''Returns the domain of variables participating in the constraints.
		
		Before any assignment, this consistency algorithm modifies upper
		bounds using the lower bounds of variables. And, when an assignment
		happens, the value of that variable is used instead.
		'''
		assignment = self.asmnt.assignment
		domains = [None, 0, 0, 0, 0, 0, 0]
		var_i = self.var_i(curvar)
		for i in range(1, 7):
			li = "L"+str(i)
			if var_i == i and value != None:
				domains[i] = {"min": value, "max": value}
			elif li in self.asmnt.assigned:
				domains[i] = {"min": assignment[li],"max": assignment[li]}
			else:
				domains[i] = self.csp.D[li]
		return domains
	
	def b_update(self, asmnt):
		'''Updates bounds of L1 to L7.
		
		Because of the way h1, h2, h3, ... functions work, passing L0
		as the curvar makes them update upper bound of all L variables.
		'''
		self.asmnt = asmnt		
		domains = self.domains("L0", None)
		return self._establish(domains, "L0")
	
	def do_update(self, uppers, lowers, domains, _confset):
		impacted = set([])
		asnd = self.asmnt.assigned
		for i in range(1, 6):
			li = "L"+str(i)
			if uppers[i] < lowers[i]:
				confset = set([cv for cv in _confset if cv in asnd])
				return (CONTRADICTION, confset)
			if uppers[i] < domains[i]["max"]:
				domains[i]["max"] = uppers[i]
				self.csp.update_d(li, domains[i])
				impacted.add(li)
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, None)	

	def _establish(self, ds, curvar):
		lowers = [None, 0, 0, 0, 0, 0, 0, 0]	# lowers
		for i in range(1, 7):
			lowers[i] = ds[i]["min"]
		inf = float("inf")
		uppers = [None, inf, inf, inf, inf, inf, inf, inf] # new uppers
		_confset = set([])
		nn = [None, 3, 3, 4, 4, 4, 5]
		var_i = self.var_i(curvar)
		for ci in [1, 2, 3, 4, 5, 6]:		
			s = self.spaces[ci]
			h = self.holes[ci]
			confset = self.update_uppers(nn[ci], var_i, uppers, lowers, ds, h, s)
			_confset.update(confset)
		return self.do_update(uppers, lowers, ds, _confset)		
		
	def establish(self, asmnt, curvar, value):
		self.asmnt = asmnt
		domains = self.domains(curvar, value)	# domains
		return self._establish(domains, curvar)
