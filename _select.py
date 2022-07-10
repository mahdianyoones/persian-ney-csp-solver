class SELECT():
	'''Selects next variable to assign using impact and degree heurisitcs.
	
	MRV is used as a tie breaker.'''
	
	def init_degree(self):
		'''Fills the degrees dictionary dynamically.'''
		self.degree = {}
		for v in self.csp.X:
			d = 0
			for _vars in self.csp.C.values():
				if v in _vars:
					d += 1
			self.degree[v] = d
	
	def init_impact(self):
		'''Defines how big is the reduction impact of variables.
		
		These numbers are based on the nature of constraints and 
		consistency algorithms.'''
		self.impact = {}
		for i in range(1, 8):
			self.impact["TH"+str(i)] = 7 * 10    # due to same_thr
			self.impact["R"+str(i)] = 7 * 10     # due to same_thr
			self.impact["D"+str(i)] = (8 - i) * 5 # due to d_dec
			self.impact["L"+str(i)] = 8 - i # due to l_dec, len, and holes
			
	def __init__(self, csp, asmnt):
		self.asmnt = asmnt
		self.csp = csp
		self.init_degree()
		self.init_impact()
			
	def next(self):
		max_rank = float("-inf")
		best_var_d_size = float("inf")
		best_var = None
		u = self.asmnt.unassigned
		for v in u:
			if v[0] == "L":
				d_size = self.csp.D[v]["max"] - self.csp.D[v]["min"]
			else:
				d_size = len(self.csp.D[v])
			rank = self.impact[v] + self.degree[v]
			if rank > max_rank:
				max_rank = rank
				best_var = v
				best_var_d_size = d_size
			elif rank == max_rank and best_var_d_size > d_size:
				max_rank = rank
				best_var = v
				best_var_d_size = d_size
		return best_var
