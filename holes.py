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
	
	def h1(self, uppers, lows, domains, curvar):
		'''Modifies uppers 1,2&3 vars W.R.T h1 constraint.'''
		s1 = self.spaces[1]
		h1 = self.holes[1]
		confset = set([])
		if curvar[1] != "1":
			old = domains[1]["max"]
			uppers[1] = min(uppers[1], old, h1-(lows[2]+lows[3]+s1))
			confset.update(["L2", "L3"])
		if curvar[1] != "2":
			old = domains[2]["max"]
			uppers[2] = min(uppers[2], old, h1-(lows[1]+lows[3]+s1))
			confset.update(["L1", "L3"])
		if curvar[1] != "3":	
			old = domains[3]["max"]
			uppers[3] = min(uppers[3], old, h1-(lows[1]+lows[2]+s1))
			confset.update(["L1", "L2"])
		return confset
		
	def h2(self, uppers, lows, domains, curvar):
		'''Modifies uppers 1,2&3 vars W.R.T h2 constraint.'''
		s2 = self.spaces[2]
		h2 = self.holes[2]
		confset = set([])
		if curvar[1] != "1":
			old = domains[1]["max"]
			uppers[1] = min(uppers[1], old, h2-(lows[2]+lows[3]+s2))
			confset.update(["L2", "L3"])
		if curvar[1] != "2":
			old = domains[2]["max"]
			uppers[2] = min(uppers[2], old, h2-(lows[1]+lows[3]+s2))
			confset.update(["L1", "L3"])
		if curvar[1] != "3":	
			old = domains[3]["max"]
			uppers[3] = min(uppers[3], old, h2-(lows[1]+lows[2]+s2))
			confset.update(["L1", "L2"])
		return confset
		
	def h3(self, uppers, lows, domains, curvar):
		'''Modifies uppers 1,2,3&4 vars W.R.T h3 constraint.'''
		s3 = self.spaces[3]
		h3 = self.holes[3]
		confset = set([])		
		if curvar[1] != "1":
			old = domains[1]["max"]
			uppers[1] = min(uppers[1], old, h3-(lows[2]+lows[3]+lows[4]+s3))
			confset.update(["L2", "L3", "L4"])
		if curvar[1] != "2":
			old = domains[2]["max"]
			uppers[2] = min(uppers[2], old, h3-(lows[1]+lows[3]+lows[4]+s3))
			confset.update(["L1", "L3", "L4"])
		if curvar[1] != "3":	
			old = domains[3]["max"]
			uppers[3] = min(uppers[3], old, h3-(lows[1]+lows[2]+lows[4]+s3))
			confset.update(["L2", "L1", "L4"])
		if curvar[1] != "4":	
			old = domains[4]["max"]
			uppers[4] = min(uppers[4], old, h3-(lows[1]+lows[2]+lows[3]+s3))
			confset.update(["L2", "L3", "L1"])
		return confset

	def h4(self, uppers, lows, domains, curvar):
		'''Modifies uppers 1,2,3&4 vars W.R.T h4 constraint.'''
		s4 = self.spaces[4]
		h4 = self.holes[4]
		confset = set([])		
		if curvar[1] != "1":
			old = domains[1]["max"]
			uppers[1] = min(uppers[1], old, h4-(lows[2]+lows[3]+lows[4]+s4))
			confset.update(["L2", "L3", "L4"])
		if curvar[1] != "2":
			old = domains[2]["max"]
			uppers[2] = min(uppers[2], old, h4-(lows[1]+lows[3]+lows[4]+s4))
			confset.update(["L1", "L3", "L4"])
		if curvar[1] != "3":	
			old = domains[3]["max"]
			uppers[3] = min(uppers[3], old, h4-(lows[1]+lows[2]+lows[4]+s4))
			confset.update(["L2", "L1", "L4"])
		if curvar[1] != "4":	
			old = domains[4]["max"]
			uppers[4] = min(uppers[4], old, h4-(lows[1]+lows[2]+lows[3]+s4))
			confset.update(["L2", "L3", "L1"])
		return confset
	
	def h5(self, uppers, lows, domains, curvar):
		'''Modifies uppers 1,2,3,4&5 vars W.R.T h5 constraint.'''
		s5 = self.spaces[4]
		h5 = self.holes[4]
		confset = set([])		
		if curvar[1] != "1":
			old = domains[1]["max"]
			uppers[1] = min(uppers[1], old, h5-(lows[2]+lows[3]+lows[4]+lows[5]+s5))
			confset.update(["L2", "L3", "L4", "L5"])
		if curvar[1] != "2":
			old = domains[2]["max"]
			uppers[2] = min(uppers[2], old, h5-(lows[1]+lows[3]+lows[4]+lows[5]+s5))
			confset.update(["L1", "L3", "L4", "L5"])
		if curvar[1] != "3":	
			old = domains[3]["max"]
			uppers[3] = min(uppers[3], old, h5-(lows[1]+lows[2]+lows[4]+lows[5]+s5))
			confset.update(["L2", "L1", "L4", "L5"])
		if curvar[1] != "4":	
			old = domains[4]["max"]
			uppers[4] = min(uppers[4], old, h5-(lows[1]+lows[2]+lows[3]+lows[5]+s5))
			confset.update(["L2", "L3", "L1", "L5"])
		return confset
		
	def h6(self, uppers, lows, domains, curvar):
		'''Modifies uppers 1,2,3,4,5 vars W.R.T h6 constraint.'''
		s6 = self.spaces[6]
		h6 = self.holes[6]
		confset = set([])		
		if curvar[1] != "1":
			old = domains[1]["max"]
			uppers[1] = min(uppers[1], old, h6-(lows[2]+lows[3]+lows[4]+lows[5]+s6))
			confset.update(["L2", "L3", "L4", "L5"])
		if curvar[1] != "2":
			old = domains[2]["max"]
			uppers[2] = min(uppers[2], old, h6-(lows[1]+lows[3]+lows[4]+lows[5]+s6))
			confset.update(["L1", "L3", "L4", "L5"])
		if curvar[1] != "3":	
			old = domains[3]["max"]
			uppers[3] = min(uppers[3], old, h6-(lows[1]+lows[2]+lows[4]+lows[5]+s6))
			confset.update(["L1", "L2", "L4", "L5"])
		if curvar[1] != "4":	
			old = domains[4]["max"]
			uppers[4] = min(uppers[4], old, h6-(lows[1]+lows[2]+lows[3]+lows[5]+s6))
			confset.update(["L1", "L2", "L3", "L5"])
		if curvar[1] != "5":	
			old = domains[5]["max"]
			uppers[5] = min(uppers[5], old, h6-(lows[1]+lows[2]+lows[3]+lows[4]+s6))
			confset.update(["L1", "L2", "L3", "L4"])
		return confset
		
	def domains(self, curvar, value):
		'''Returns the domain of variables participating in the constraints.
		
		Before any assignment, this consistency algorithm modifies upper
		bounds using the lower bounds of variables. And, when an assignment
		happens, the value of that variable is used instead.
		'''
		assignment = self.asmnt.assignment
		domains = [None, 0, 0, 0, 0, 0, 0]
		for i in range(1, 7):
			li = "L"+str(i)
			if curvar[1] == i and value != None:
				domains[i] = {"min": value, "max": value}
			elif li in self.asmnt.assigned:
				domains[i] = {"min": assignment[li],"max": assignment[li]}
			else:
				domains[i] = self.csp.D[li]
		return domains
	
	def b_update(self, asmnt):
		self.asmnt = asmnt
		domains = self.domains("L9", "None")
		return self._establish(domains, curvar)
	
	def _establish(self, domains, curvar):
		lowers = [None, 0, 0, 0, 0, 0, 0, 0]	# lowers
		for i in range(1, 7):
			lowers[i] = domains[i]["min"]
		inf = float("inf")
		uppers = [None, inf, inf, inf, inf, inf, inf, inf] # new uppers
		self.h1(uppers, lowers, domains, curvar)
		self.h2(uppers, lowers, domains, curvar)
		self.h3(uppers, lowers, domains, curvar)
		self.h4(uppers, lowers, domains, curvar)
		self.h5(uppers, lowers, domains, curvar)
		self.h6(uppers, lowers, domains, curvar)
		impacted = set([])
		asmnt = asmnt.assignment
		for i in range(1, 6):
			li = "L"+str(i)
			if uppers[i] < lowers[i]:
				confset = ["L"+str(j) for j in [1,2,3,4,5] if "L"+str(j) in asmnt]
				return (CONTRADICTION, confset)
			if uppers[i] < domains[i]["max"]:
				domains[i]["max"] = uppers[i]
				self.csp.update_d(li, domains[i])
				impacted.add(li)
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, None)	
		
	def establish(self, asmnt, curvar, value):
		self.asmnt = asmnt
		domains = self.domains(curvar, value)	# domains
		return self._establish(domains, curvar)
