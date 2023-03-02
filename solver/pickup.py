from constants import *
import copy

class SELECT():
	'''Helps select next variable and next value for assignment.'''
			
	def __init__(self):
		self.__degree = {}
		self.__impact = {}

	def nextvar(self, csp):
		'''Selects next variable to assign using degree and impact heuristics.
	
		MRV is used as a tie breaker.'''
		self.__init_degree(csp)
		self.__init_impact(csp)
		D = csp.get_domains()
		ua = csp.get_unassigned_vars()
		if len(ua) == 1:
			return copy.copy(ua).pop()
		degrees = self.__degree
		impacts = self.__impact		
		best = {
			"var": None, 
			"size": 10000000000, # an arbitrary very big number 
			"degree": -1,
			"impact": -1
		}
		for unassigned_var in ua:
			size = self.__domain_size(unassigned_var, D)
			impact = impacts[unassigned_var]
			degree = degrees[unassigned_var]
			is_better = False
			if impact > best["impact"]:
				is_better = True
			elif impact == best["impact"]:
				if size < best["size"]:
					is_better = True
				elif size == best["size"] and degree > best["degree"]:
					is_better = True
			if is_better:
				best = {
					"var": unassigned_var, 
					"size": size, 
					"degree": degree, 
					"impact": impact
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
		pass

	def __init_impact(self, csp):
		'''Determines the impact of selecting variables: impact heuristic.
		
		P variables are made consistent very strongly. Therefore, making them
		consistent first helps detect failure or prune a significant amount of
		the search tree upfront.
		
		Upon arrival of a new CSP, only if the number of variables differ
		will the impacts be reinitiated.'''
		X = csp.get_variables()
		if self.__impact != {} and len(self.__impact.keys()) >= len(X):
			return
		for v in csp.get_variables():
			if v[0] == "P":
				self.__impact[v] = 1
			else:
				self.__impact[v] = 0

	def __domain_size(self, var, D):
		if var[0] == "L":
			return D[var]["max"] - D[var]["min"]
		return len(D[var])