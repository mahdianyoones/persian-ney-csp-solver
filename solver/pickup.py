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
		self.__init_degree(csp)
		self.__impact = {
			"T1": 100,
			"T2": 100,
			"T3": 100,
			"T4": 100,
			"T5": 100,
			"T6": 100,
			"T7": 100,
			"R1": 100,
			"R2": 100,
			"R3": 100,
			"R4": 100,
			"R5": 100,
			"R6": 100,
			"R7": 100,
			"D1": 50,
			"D2": 50,
			"D3": 50,
			"D4": 50,
			"D5": 50,
			"D6": 50,
			"D7": 50,
			"L1": 25,
			"L2": 25,
			"L3": 25,
			"L4": 25,
			"L5": 25,
			"L6": 25,
			"L7": 25
		}
	
	def nextvar(self, csp):
		'''Selects next variable to assign using degree and impact heuristics.
	
		MRV is used as a tie breaker.'''
		D = csp.get_domains()
		ua = csp.get_unassigned_vars()
		degree = self.__degree
		impact = self.__impact		
		best = {"var": None, "size": float("inf"), "rank": float("-inf")}
		for unassigned_var in ua:
			size = self.__domain_size(unassigned_var, D)
			rank = impact[unassigned_var] + degree[unassigned_var]
			but_better_mrv = best["size"] > size
			have_equal_ranks = rank == best["rank"]
			if rank > best["rank"] or have_equal_ranks and but_better_mrv:
				best = {"var": unassigned_var, "size": size, "rank": rank}
		return best["var"]
		
	def nextval(self, curvar, domain):
		'''Returns the next value in the domain of curvar.'''		
		if curvar[0] == "L":
			if domain["min"] > domain["max"]:
				return DOMAIN_EXHAUSTED
			val = domain["min"]
			if curvar == "L2":
				domain["min"] += 2
			else:
				domain["min"] += 1
			return val
		elif len(domain) == 0: # D, T, and R variables
			return DOMAIN_EXHAUSTED
		return domain.pop()

	def __init_degree(self, csp):
		'''Determines the degree of variables'''
		constraints = csp.get_constraints()
		for v in csp.get_variables():
			d = 0
			for _vars in constraints.values():
				if v in _vars:
					d += 1
			self.__degree[v] = d

	def __domain_size(self, var, D):
		if var[0] == "L":
			return D[var]["max"] - D[var]["min"]
		return len(D[var])