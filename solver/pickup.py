class SELECT():
	'''Selects next variable to assign using impact and degree heurisitcs.
	
	MRV is used as a tie breaker.'''
		
	def __init__(self, csp):
		self.__csp = csp
		self.__degree = {}
		self.__impact = {}
		self.__corders = {}
		self.__init_degree()
		self.__init_impact()
		self.__det_corders()
	
	def __det_corders():
		'''Determines the order of constraints.'''
		self.__corders = {
			"same_th": 1, # goes frist
			"same_r": 2,
			"d_dec": 3,
			"in_stock": 4,
			"l1_half_l2": 5,
			"l_dec": 6,
			"h1": 7,
			"h2": 8,
			"h3": 9,
			"h4": 10,
			"h5": 11,
			"h6": 12,
			"len": 13
		}
	
	def __init_degree(self):
		'''Fills the degrees dictionary dynamically.'''
		for v in self.__csp.get_variables():
			d = 0
			constraints = self.__csp.get_constraints()
			for _vars in constraints.values():
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
		A = self.__csp.get_assignment()
		D = self.__csp.get_domains()
		X = self.__csp.get_variables()
		degrees = self.__degree
		impacts = self.__impact
		return self.__nextvar(degrees, impacts, X, D, A)
		
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
				
	def __nextvar(self, degree, impact, X, D, A):
		'''Returns the next variable to be assigned.
		
		This is a mathematical function.'''
		best_rank = float("-inf")
		best_size = float("inf")
		best_var = None
		for var in X:
			if var not in A:
				continue
			if var[0] == "L":
				d_size = D[var]["max"] - D[var]["min"]
			else:
				d_size = len(D[var])
			rank = impact[var] + degree[var]
			if rank > best_rank:
				best_rank = rank
				best_var = var
				best_size = d_size
			elif rank == best_rank and best_size > d_size:
				best_rank = rank
				best_var = var
				best_size = d_size
		return best_var
