from constants import *
import copy

class SELECT():
	'''Helps select next variable and next value for assignment.'''
			
	def __init__(self):
		self.__degree = {}

	def nextvar(self, csp):
		'''Selects next variable to assign using degree and mrv heuristics.
	
		MRV is used as a tie breaker.'''
		self.__init_degree(csp)
		D = csp.get_domains()
		ua = csp.get_unassigned_vars()
		if len(ua) == 1:
			return copy.copy(ua).pop()
		degrees = self.__degree
		best = {
			"var": None, 
			"size": 10000000000, # an arbitrary large number
			"degree": -1,
		}
		for unassigned_var in ua:
			size = self.__domain_size(unassigned_var, D)
			degree = degrees[unassigned_var]
			is_better = False
			if size < best["size"]:
				is_better = True
			elif size == best["size"] and degree > best["degree"]:
				is_better = True
			if is_better:
				best = {
					"var": unassigned_var, 
					"size": size, 
					"degree": degree, 
				}
		return best["var"]		

	def __init_degree(self, csp):
		'''Determines the degree of variables.
		
		Selecting more constraind variables first for assignment is a natural
		heuristic that helps detect failure or prune large unpromising amounts 
		of search tree upfront.

		Upon arrival of a new CSP, only if the number of variables differ
		will the degrees be reinitiated.'''
		X = csp.get_variables()
		if self.__degree != {} and len(self.__degree.keys()) >= len(X):
			return
		constraints = csp.get_constraints()
		for v in csp.get_variables():
			d = 0
			for _vars in constraints.values():
				if v in _vars:
					d += 1
			self.__degree[v] = d

	def __domain_size(self, var, D):
		if var[0] == "L":
			return D[var]["max"] - D[var]["min"] + 1
		return len(D[var])