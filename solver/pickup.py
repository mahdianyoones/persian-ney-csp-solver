from asyncio import constants
from constants import *

class SELECT():
	'''Helps select next variable and next value for assignment.'''
		
	def __init__(self, csp):
		'''Initiates impact heuristic.
		
		This heuristic prioritizes the selection of TH and R variables over
		others, since samethick and sameround algorithms reduce all
		participating variables to 1 value all at once.
		
		Fourthermore, due to the constraint diamdec, D variables with higher
		indices have higher impacts, in that selecting D1 first makes 6 other
		variables shed values, and selecting D2 then makes 5 other variables
		shed values, adn so on.
		
		The numbers are chosen by trial and error. More analysis is required.'''
		self.__degree = {}
		self.__impact = {}
		self.__init_degree(csp)
		self.__init_impact(csp)
	
	def nextvar(self, csp):
		'''Selects next variable to assign using degree and impact heuristics.
	
		MRV is used as a tie breaker.'''
		D = csp.get_domains()
		ua = csp.get_unassigned_vars()
		degrees = self.__degree
		impacts = self.__impact		
		best = {
			"var": None, 
			"size": float("inf"), 
			"degree": float("-inf"),
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
				if degree > best["degree"]:
					is_better = True
				elif degree == best["degree"] and best["size"] > size:
					is_better = True
			if is_better:
				best = {
					"var": unassigned_var, 
					"size": size, 
					"degree": degree, 
					"impact": impact
				}
		return best["var"]
		
	def nextval(self, curvar, domain):
		'''Returns the next value in the domain of curvar.'''		
		if curvar[0] == "L":
			val = domain["min"]
			if curvar == "L2":
				domain["min"] += 2
			else:
				domain["min"] += 1
		else:
			val = domain.pop()		
		return val

	def domain_exhausted(self, curvar, domain):
		if curvar[0] == "L":
			if domain["min"] > domain["max"]:
				return True
		elif len(domain) == 0: # D, T, and R variables
			return True
		return False			

	def __init_degree(self, csp):
		'''Determines the degree of variables'''
		constraints = csp.get_constraints()
		for v in csp.get_variables():
			d = 0
			for _vars in constraints.values():
				if v in _vars:
					d += 1
			self.__degree[v] = d

	def __init_impact(self, csp):
		'''Determines the impact of selecting variables.
		
		T and R variables are made consistent very strongly'''
		for v in csp.get_variables():
			if v[0] == "T" or v[0] == "R":
				self.__impact[v] = 1
			else:
				self.__impact[v] = 0

	def __domain_size(self, var, D):
		if var[0] == "L":
			return D[var]["max"] - D[var]["min"]
		return len(D[var])