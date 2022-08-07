class SELECT():
	'''Selects next variable to assign using impact and degree heurisitcs.
	
	MRV is used as a tie breaker.'''
	
	def __init_degree(self):
		'''Fills the degrees dictionary dynamically.'''
		self.degree = {}
		for v in self.csp.X:
			d = 0
			for _vars in self.csp.C.values():
				if v in _vars:
					d += 1
			self.degree[v] = d
	
	def __init_impact(self):
		'''Defines how big is the reduction impact of variables.
		
		These numbers are based on the nature of constraints and 
		consistency algorithms.'''
		self.impact = {}
		for i in range(1, 8):
			self.impact["TH"+str(i)] = 7 * 10    # due to same_th
			self.impact["R"+str(i)] = 7 * 10     # due to same_r
			self.impact["D"+str(i)] = (8 - i) * 5 # due to d_dec
			self.impact["L"+str(i)] = 8 - i # due to l_dec, len, and holes
			
	def __init__(self, csp, asmnt):
		self.__asmnt = asmnt
		self.__csp = csp
		self.__init_degree()
		self.__init_impact()
			
	def next(self):
		best_rank = float("-inf")
		best_size = float("inf")
		best_var = None
		u = self.asmnt.unassigned
		for v in u:
			if v[0] == "L":
				d_size = self.csp.D[v]["max"] - self.csp.D[v]["min"]
			else:
				d_size = len(self.csp.D[v])
			rank = self.impact[v] + self.degree[v]
			if rank > best_rank:
				best_rank = rank
				best_var = v
				best_size = d_size
			elif rank == best_rank and best_size > d_size:
				best_rank = rank
				best_var = v
				best_size = d_size
		return best_var
