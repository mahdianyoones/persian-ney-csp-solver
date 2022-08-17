class SELECT():
	'''Selects next variable to assign using impact and degree heurisitcs.
	
	MRV is used as a tie breaker.'''
		
	def __init__(self, csp):
		self.__csp = csp
		self.__degree = {}
		self.__impact = {}
		self.__init_degree()
		self.__init_impact()
	
	def __init_degree(self):
		'''Fills the degrees dictionary dynamically.'''
		for v in self.csp.X:
			d = 0
			for _vars in self.csp.C.values():
				if v in _vars:
					d += 1
			self.__degree[v] = d
	
	def __init_impact(self):
		'''Defines how big is the reduction impact of variables.
		
		These numbers are based on the nature of constraints and 
		consistency algorithms.'''
		for i in range(1, 8):
			self.__impact["TH"+str(i)] = 7 * 10    # due to same_th
			self.__impact["R"+str(i)] = 7 * 10     # due to same_r
			self.__impact["D"+str(i)] = (8 - i) * 5 # due to d_dec
			self.__impact["L"+str(i)] = 8 - i # due to l_dec, len, and holes
	
	def nextvar(self):
		assignment = self.csp.get_assignment()
		domains = self.csp.D
		allvars = self.__csp.get_X()
		d = self.__degree
		i = self.__impact
		return self.__nextvar(d, i, allvars, domains, assignment)
		
	def nextval(self, curvar, domain, offset):
		'''Returns the next value in the domain curvar W.R.T. offset.
		
		This is a mathematical function.
		'''		
		if curvar[0] == "L":
			if offset > domain["max"] - domain["min"]:
				value = DOMAIN_EXHAUSTED
			else:
				value = domain["min"] + offset
		else:
			value = DOMAIN_EXHAUSTED if len(domain) == 0 else domain.pop()
		offset += 2 if curvar == "L2" else 1
		return (value, offset)
				
	def __nextvar(self, degree, impact, allvars, domains, assignment):
		'''Returns the next variable to be assigned.
		
		This is a mathematical function.'''
		best_rank = float("-inf")
		best_size = float("inf")
		best_var = None
		for v in allvars:
			if v not in assignment:
				continue
			if v[0] == "L":
				d_size = domains[v]["max"] - domains[v]["min"]
			else:
				d_size = len(domains[v])
			rank = impact[v] + degree[v]
			if rank > best_rank:
				best_rank = rank
				best_var = v
				best_size = d_size
			elif rank == best_rank and best_size > d_size:
				best_rank = rank
				best_var = v
				best_size = d_size
		return best_var
