CONTRADICTION = None
FAILURE = False
SUCCESS = True
FEATURE_IS_NOT_SET = False
FEATURE_IS_SET = True
DOMAINS_REDUCED = 0
DOMAINS_INTACT = 1

class MAC():
	'''Implements MAC through special consistency algorithms.
				
	Impacts due to {D1: 18}: 
	
	<<Direct>>
	
		D1 ---------------------> R1, TH1, L1
		      due to in_stock

		D1 ---------------------> D2, D3, D4, D5, D6, D7
		       due to d_dec
	
	<<Indirect>>
	
		L1 ----------------------> L2 
	          due to l1_half_l2
	          
	     L1 -----------------------------------------> a subset of {L2, L3, L4, L5}
	     	  due to h1, h2, h3, h4, h5, and h6 

		R1 ---------------------> R2, R3, R4, R5, R6, R7
	     	  due to same_r
	        
		TH1 ---------------------> TH2, TH3, TH4, TH5, TH6, TH7
			  due to same_th
	
	Impacts due to {D1: 18, TH1: 2}: (TH1 is assigned after D1)
	
	<<Direct>>
	
		TH1 ---------------------> R1, L1
		      due to in_stock

		TH1 ---------------------> TH2, TH3, TH4, TH5, TH6, TH7
		       due to same_th
		       
	<<Indirect>>
	
		L1 ----------------------> L2
	          due to l1_half_l2
	          
	     L1 -----------------------------------------> a subset of {L2, L3, L4, L5}
	     	due to h1, h2, h3, h4, h5, and h6 

		R1 ---------------------> R2, R3, R4, R5, R6, R7
	     	  due to same_r
	     	  
	Impacts due to {D2: 17}

	<<Direct>>
	
		D2 ---------------------> R2, TH2, L2
		      due to in_stock

		D2 ---------------------> D3, D4, D5, D6, D7
		       due to d_dec
	
	<<Indirect>>
	
		L2 --------------------------> L3, L4, L5, L6, L7
	             due to l1_half_l2

	     L2 -----------------------------------------> a subset of {L1, L3, L4, L5}
	     	due to h1, h2, h3, h4, h5, and h6 

		R2 ------------------------> R3, R4, R5, R6, R7
	     	     due to same_r
	        
		TH2 -------------------------> TH3, TH4, TH5, TH6, TH7
			    due to same_th


	'''
	def __init__(self, csp, asmnt, confset):
		self.csp = csp
		self.asmnt = asmnt
		self.confset = confset
		self.neighbors = {}
		self.alg_ref = {
			"h1":		self.apply_holes,
			"h2":		self.apply_holes,
			"h3":		self.apply_holes,
			"h4":		self.apply_holes,
			"h5":		self.apply_holes,
			"h6":		self.apply_holes,
			"l1_half_l2":	self.apply_l1_half_l2,
			"in_stock": 	self.apply_in_stock,
			"same_th":	self.apply_same_thr,
			"same_r":		self.apply_same_thr,
			"l_dec":		self.apply_l_dec,
			"d_dec":		self.apply_d_dec,
			"len":		self.apply_len
		}

	def neighborhood(self, curvar):
		'''Returns variables that share a constraint with curvar.
		
		Returns a dictionary of this format:
		{
			"constraint 1": {a set of neighbors connected via constraint 1},
			"constraint 2": {a set of neighbors connected via constraint 2},
			...
		}
		
		To boost performace, neighbors are cached in self.neighbors.
		'''
		if not curvar in self.neighbors:
			self.neighbors[curvar] = set([])
			C = self.csp.getC()
			for constraint, _vars in C.items():
				if curvar in _vars:
					self.neighbors[curvar][constraint] = _vars
		return self.neighbors[curvar]

	def maintain(self, curvar, value):
		'''Establishes consistency for curvar neighbors and returns a conflict set.
		
		If the domain of a neighbor changes, neighbors of that neighbor are also
		checked for reduction.
		
		curvar is the variable which neighbors are to be made consistent.
		Before search, bounds on varaibles needs to be made consistent.
		Therefore, this method is called for all variables one by one with
		value = None. 
		
		Individual consistency algorithms (i.e. other methods of this class),
		detect if there is an oppotunity to reduce the domain of variables
		W.R.T. curvar.
		'''
		reduced = set([curvar])
		self.csp.backupD()
		while len(reduced) > 0:
			curvar = reduced.pop()
			neighborhood = self.neighborhood(curvar)
			my_cs = neighborhood.keys()
			for c in my_cs:
				cresult = self.alg_ref[c](curvar, value)
				if cresult[0] == CONTRADICTION:
					self.csp.revert_d()
					return (FAILURE, cresult[1])
				elif cresult[0] == DOMAINS_INTACT:
					continue
				elif cresult[0] == DOMAINS_REDUCED:
					reduced.update(cresult[1])
		# All domains have survived consistency.
		return (SUCCESS)
		
	def apply_in_stock(self, curvar, value):
		'''Updates variables in the updatables set W.R.T. in_stock constraint.
		
		Returns 
		(CONTRADICTION, confset),
		(DOMAINS_INTACT, impacted variables), or 
		(domains intact, None).
		
		"Domains intact" means an L variable is newly assigned. We 
		intuitively know that L variables do not impact TH, R, and D
		variables.'''
		i = curvar[1]
		if not curvar[0] in ["R", "D", "TH"]:
			return (DOMAINS_INTACT, None)
		impacting = {"R"+i, "TH"+i, "D"+i}
		impacting.remove(curvar)
		impacted = {"R"+i, "TH"+i, "D"+i}
		impacted.remove(curvar)
		filters = {curvar: value}
		node = self.asmnt.nodes[curvar[1]]
		asmnt = self.asmnt.asmnt
		for var in [v for v in impacting if node[v] == FEATURE_IS_SET]:
			impacted.remove(var)
			filters[var] = asmnt(var)
		confset = filters.keys()
		for var in impacted:
			newD = self.csp.catalog.values(var, filters)
			if len(newD) == 0:
				return (CONTRADICTION, confset)
			self.csp.updateD(var, newD)
		if node["L"] == FEATURE_IS_NOT_SET:
			Dprev = self.csp.varDomain("L"+i)
			newD = {
				"min": Dprev["min"],
				"max": self.csp.catalog.get_l(filters)
			}
			if new_domains["L"+i]["max"] < new_domains["L"+i]["min"]:
				return (CONTRADICTION, confset)
			impacted.add("L"+i)
			self.csp.updateD("L"+i, newD)
		return (DOMAINS_REDUCED, impacted)
	
	def apply_len(self, curvar, value):
		'''Makes L variables consistent W.R.T len constraint.
		
		This is probably the last constraint before a solution can
		be found. It enforces the overall length of the Ney.
		
		The following updates can occur:
		
		L1 = len - (L2+L3+L4+L5+L6+L7)
		L2 = len - (L1+L3+L4+L5+L6+L7)
		L3 = len - (L1+L2+L4+L5+L6+L7)
		L4 = len - (L1+L2+L3+L5+L6+L7)
		L6 = len - (L1+L2+L3+L4+L5+L7)
		L7 = len - (L1+L2+L3+L4+L5+L6)
		
		where h1 is the length of the Ney.
		'''
		asmnt = self.asmnt.asmnt
		assignedLs = []
		unassignedL = None
		_sum = 0
		for i in range(1, 8):
			if "L"+i in asmnt:
				assignedLs.add("L"+i)
				_sum += asmnt["L"+i]
			else:
				unassignedL = "L"+i
		if len(assignedLs < 6):
			return (DOMAINS_INTACT, None)
		newL = self.csp.spec["len"] - _sum # L1 = h1 - (L2+L3+L4+L5+L6+L7)
		D = self.csp.D[impact]
		if newL < D["min"] or newL > D["max"]:
			confset = assignedLs
			return (CONTRADICTION, confset)
		newD = {"min": newL, "max": newL}
		self.csp.update_d(unassignedL, newD)
		return (DOMAINS_REDUCED, set([unassignedL]))
	
	def apply_same_thr(self, curvar, value):
		'''Applies same thickness and roundness constraints.
		
		If updatables set contains less than 6 TH or R variables, it means
		TH and R variables are already made consistent and further attempts
		would not further reduce any domain.
		
		Note that conflict set is empty since the algorithm makes all neighbors
		consistent in one-go. There are no direct culpirits in the assignment to 
		return as the conflict set.
		
		Resolving the contradictions due to this constraint are done only via
		backtracking. No backjumping is possible.
		'''
		impacted_Rs = set([])
		for i in range(1, 8):
			if curvar[0] == "R‌" and "R"+i != curvar:
				impacted_Rs.add("R"+i)
			elif curvar[0] == "TH" and "TH"+i != curvar:
				impacted_THs.add("TH"+i)
		if len(impacted_Rs) == 6:
			impacted = impacted_Rs
		elif len(impacted_THs) == 6:
			impacted = impacted_THs
		else
			return (DOMAINS_INTACT, None)
		asmnt = self.assignment.getAssignment()
		i = curvar[1]
		impacted = []
		newD = set([value])
		for var in impacted.copy():
			Dprev = self.csp.varDomain(var)
			if not value in Dprev:
				return (CONTRADICTION, set([]))
			if len(Dprev) == 1: # no change
				impacted.remove(var)
				continue
			self.csp.updateD(curvar, newD)
		return (DOMAINS_REDUCED, impacted)

	def apply_l_dec(self, curvar, value):
		'''Applies length decrement consistency.
		
		The following relations must hold:
			L2 > L3 > 2/3 L2
			L3 > L4 > 2/3 L3
			L4 > L5 > 2/3 L4
			L5 > L6 > 2/3 L5
			L6 > L7
		
		If value == None, this is an indirect bound propagation:
		
			upper3 = min(upper3, upper2 - 1)
			upper4 = min(upper4, upper3 - 1)
			upper5 = min(upper5, upper4 - 1)
			upper6 = min(upper6, upper5 - 1)
			upper7 = min(upper7, upper6 - 1)
			
			lower3 = max(lower3, 2/3 lower2)
			lower4 = max(lower4, 2/3 lower3)
			lower5 = max(lower5, 2/3 lower4)
			lower6 = max(lower6, 2/3 lower5)

		if value != None, an L variable is assigned the impact is direct:
		
			upper3 = min(upper3, L2 - 1)
			upper4 = min(upper4, upper3 - 1)
			upper5 = min(upper5, upper4 - 1)
			upper6 = min(upper6, upper5 - 1)
			upper7 = min(upper7, upper6 - 1)
			
			lower3 = max(lower3, 2/3 * L2)
			lower4 = max(lower4, 2/3 lower3)
			lower5 = max(lower5, 2/3 lower4)
			lower6 = max(lower6, 2/3 lower5)
				
		This consistency function is called on two occasions:
			1- An L variable is assigned a value
			2- Domain of an L variable has been reduced
			
			In case 1, we use the assigned value to determine a new 
			consistent range for further variables. For example, if L3 
			is assigned, say, 100, upper bound on L4, L5, L6 reduce to 
			99, 98, 97, and 96 respectively. Furthermore, the lower bounds
			of L4, L5, and L6 reduce to around 66, 44, and 29 respectively.
			i.e. {L3: 100} propagates to
			
				L4 -> [66, 99] 
				L5 -> [44, 98]
				L6 -> [29, 96]
			
			In case 2, we use new bounds on the variable whose domain has
			been reduced. That variable is curvar. For example, if the 
			domain of L3 has reduced to, say, [80, 120], the domain of 
			L4, L5, and L6 change as such:
			
				L4 -> [53, 119]
				L5 -> [35, 118]
				L6 -> [23, 117]
			
			From the two examples above, we can observe that assigning
			values to variables can trigger strongger domain reduction
			in propagation.
		'''
		impacted = {}
		self.csp.backupD()
		for i in range(curvar[1]+1, 8): # curvar up to L7
			if value != None:
				D = {"min": value, "max": value}
			else:
				D = self.csp.varDomain(curvar)
			Dprev = self.csp.varDomain(impact)
			newMax = D["max"] - 1
			newMin = D["min"] * 2/3 if i < 7 else Dprev["min"]
			if newMax < newMin:
				self.csp.revertD()
				return (CONTRADICTION, set([]))
			newD = Dprev.copy()
			reduced = False
			if newMax < Dprev["max"]:
				newD["max"] = newMax
				impacted.add("L"+i)
				reduced = True
			if newMin > Dprev["min"]:
				newD[impact]["min"] = newMin
				impacted.add("L"+i)
				reduced = True
			if reduced:
				curvar = "L"+i
			else:
				break # stop propagating nothing!
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)
		else:
			return (DOMAINS_INTACT, None)
	
	def apply_d_dec(self, curvar, value):
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
		impacted = {}
		self.csp.backupD()
		if value != None:
			maxPrev = value
			minPrev = value
		else:
			D = sorted(self.csp.varDomain(curvar), reverse=True)
			maxPrev = D[-1]
			minPrev = D[0]
		ddiffmin = self.csp.spec["ddiff"]["min"]
		ddiffmax = self.csp.spec["ddiff"]["max"]
		for i in range(curvar[1]+1, 8): # curvar up to D7
			D = self.csp.varDomain("D"+i)
			newMaxPrev = float("-inf")
			newMinPrev = float("+inf")
			for v in D.copy():
				if v < minPrev - ddiffmax or v > maxPrev - ddiffmin:
					impacted.add("D"+i)
					D.remove(v)
				elif v > newMaxPrev:
					newMaxPrev = v
				elif v < newMinPrev:
					newMinPrev = v
			if len(impacted) == 0:
				self.csp.revertD()
				break # stop propagating nothing!
			if len(D) == 0:
				self.csp.revertD()
				return (CONTRADICTION, set([]))
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)
		else:
			return (DOMAINS_INTACT, None)

	def apply_l1_half_l2(self, L1, value):
		'''Reduces L1 and L2 domains so that L1 = L2 * 2.
		
		If L1 is assigned a value, L2 reduces to one value only. However,
		the domain of L2 will still be represented via bounds--now with
		equal min & max.
		
		Example: 
		'''
		DL1 = self.csp.varDomain("L1")
		DL2 = self.csp.varDomain("L2")
		impacted = {}
		self.csp.backupD()
		if value == None:
			lower22 = DL2["min"] / 2
			if lower22 >= DL1["max"] or lower22 <= DL2["min"]:
				return (DOMAINS_INTACT, None)
			if lower22 < DL1["max"]:
				DL1["max"] = lower22
				impacted.add("L1")
			if lower22 > DL2["min"]:
				DL2["min"] = lower22
				impacted.add("L2")
			if DL1["min"] < DL1["max"] or DL2["min"] < DL2["max"]:
				return (CONTRADICTION, None)
		else:
			newValue = value * 2
			if newValue >= DL2["max"] or newValue <= DL2["min"]:
				return (CONTRADICTION, None)
			if newValue == DL2["max"] and newValue == DL2["min"]:
				return (DOMAINS_INTACT, None)			
			DL2 = {"min": value * 2, "max": value * 2}
			impacted.add("L2")
		if len(impacted) == 0:
			return (DOMAINS_INTACT, None)
		return (DOMAINS_REDUCED, impacted)
		
	def apply_holes(self, curvar, value):
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

				h1, h2

					lower1 -> 	   upper2, upper3
					lower2 -> upper1,         upper3
					lower3 -> upper1, upper2
				
				h3, h4, h5
				
			 		lower1 ->         upper2, upper3, upper4
			 		lower2 -> upper1,         upper3, upper4
			 		lower3 -> upper1, upper2,         upper4
			 		lower4 -> upper1, upper2, upper3

				h6
				
			 		lower1 ->         upper2, upper3, upper4, upper5
			 		lower2 -> upper1,         upper3, upper4, upper5
			 		lower3 -> upper1, upper2,         upper4, upper5
			 		lower4 -> upper1, upper2, upper3,	       upper5
			 		lower5 -> upper1, upper2, upper3, upper4
		
		Note: "lower1 -> upper2, upper3" means if lower1 changes, upper2 and
		upper3 are impacted hence must be updated.
		
		When the lower bound of an L variable (L1 to L5) reduces, the upper
		bound of other variables L variables (L1 to L5) are impacted.
		
		L1 + L2 + L3 + 10 			< h1
		L1 + L2 + L3 + 30 			< h2
		L1 + L2 + L3 + L4 + 10 		< h3
		L1 + L2 + L3 + L4 + 30 		< h4
		L1 + L2 + L3 + L4 + 50 		< h5
		L1 + L2 + L3 + L4 + L5 + 10 	< h6
		'''
		S = [
			None,
			spec["hmarg"] * 1,
			spec["hmarg"] * 2 + spec["holed"] * 1,
			spec["hmarg"] * 1,
			spec["hmarg"] * 2 + spec["hold"] * 1,
			spec["hmarg"] * 3 +‌ spec["hold"] * 2,
			spec["hmarg"] * 1
		]
		asmnt = self.csp.getAssignment()
		M = Ds = [None, 0, 0, 0, 0, 0, 0]
		impacted = {}
		for i in range(1, 7):
			if curvar[1] == i and value != None:
				Ds[i] = {"min": value, "max": value}
			else if "L"+i in asmnt:
				Ds[i] = {"min": asmnt["L"+i], "max": asmnt["L"+i]}
			else:
				Ds[i] = self.csp.varDomain("L"+i)
				impacted.add("L"+i)
			M[i] = Ds[i]["min"]
		H = [None, spec["h1"], spec["h2"], spec["h3"], spec["h4"], 
			spec["h5"], spec["h6"], spec["h7"]]
		maxs = [None, 0, 0, 0, 0, 0]
		if curvar[1] != "1" and "L1" in impacted:
		 	maxs[1] = min(Ds[1]["max"], H[1] - (M[2] + M[3] + S[1]))	# h1 - upper1
			maxs[1] = min(max1, H[2] - (M[2] + M[3] + S[2]))			# h2 - upper1
			maxs[1] = min(max1, H[3] - (M[2] + M[3] + M[4] + S[3]))	# h3 - upper1
			maxs[1] = min(max1, H[4] - (M[2] + M[3] + M[4] + S[4]))	# h4 - upper1
			maxs[1] = min(max1, H[5] - (M[2] + M[3] + M[4] + S[5]))	# h5 - upper1
			maxs[1] = min(max1, H[6] - (M[2] + M[3] + M[4] + M[5] + S[6]))	# h6 - upper1
			confset = ["L"+i for i in [2, 3, 4, 5] if "L"+i in asmnt]
			if M[1] > maxs[1]:
				return (CONTRADICTION, confset)
		if curvar[1] != "2" and "L2" in impacted:
			maxs[2] = min(Ds[2]["max"], H[1] - (M[1] + M[3] + S[1]))	# h1 - upper2
			maxs[2] = min(max2, H[2] - (M[1] + M[3] + S[2]))			# h2 - upper2
			maxs[2] = min(max2, H[3] - (M[1] + M[3] + M[4] + S[3]))		# h3 - upper2
			maxs[2] = min(max2, H[4] - (M[1] + M[3] + M[4] + S[4]))		# h4 - upper2
			maxs[2] = min(max2, H[5] - (M[1] + M[3] + M[4] + S[5]))		# h5 - upper2
			maxs[2] = min(max2, H[6] - (M[1] + M[3] + M[4] + M[5] + S[6]))	# h6 - upper2
			confset = ["L"+i for i in [1, 3, 4, 5] if "L"+i in asmnt]
			if M[2] > maxs[2]:
				return (CONTRADICTION, confset)
		if curvar[1] != "3" and "L3" in impacted:
			maxs[3] = min(Ds[3]["max"], H[1] - (M[1] + M[2] + S[1]))	# h1 - upper3
			maxs[3] = min(max3, H[2] - (M[1] + M[2] + S[2]))			# h2 - upper3
			maxs[3] = min(max3, H[3] - (M[1] + M[2] + M[4] + S[3]))	# h3 - upper3
			maxs[3] = min(max3, H[4] - (M[1] + M[2] + M[4] + S[4]))	# h4 - upper3
			maxs[3] = min(max3, H[5] - (M[1] + M[2] + M[4] + S[5]))	# h5 - upper3
			maxs[3] = min(max3, H[6] - (M[1] + M[2] + M[4] + M[5] + S[6]))	# h6 - upper3
			confset = ["L"+i for i in [1, 2, 4, 5] if "L"+i in asmnt]
			if M[3] > maxs[3]:
				return (CONTRADICTION, confset)
		if curvar[1] != "4" and "L4" in impacted:
			maxs[4] = min(Ds[4]["max"], H[3] - (M[1] + M[2] + M[3] + S[3]))	# h3 - upper4
			maxs[4] = min(max4, H[4] - (M[1] + M[2] + M[3] + S[4]))		# h4 - upper4
			maxs[4] = min(max4, H[5] - (M[1] + M[2] + M[3] + S[5]))		# h5 - upper4
			maxs[4] = min(max4, H[6] - (M[1] + M[2] + M[3] + M[5] + S[6]))	# h6 - upper4
			confset = ["L"+i for i in [1, 2, 3, 5] if "L"+i in asmnt]
			if M[4] > maxs[4]:
				return (CONTRADICTION, confset)
		if curvar[1] != "5" and "L5" in impacted:
			maxs[5] = min(Ds[5]["max"], H[6] - (M[1] + M[2] + M[3] + M[4] + S[6])) # h6 - upper5		
			confset = ["L"+i for i in [1, 2, 3, 4] if "L"+i in asmnt]
			if M[5] > maxs[5]:
				return (CONTRADICTION, confset)
		for i in range(1, 7):
			if maxs[i] == Ds[i]["max"]:
				impacted.remove("L"+i)
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, None)
