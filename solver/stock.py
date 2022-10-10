from distutils.command.config import config
from constants import *

class STOCK():
	'''Implements stock consistency.
	
	This constraint ensures that reeds with selected properties exist in the
	stock of reeds. 

	Each reed piece has these properties: Length, thickness, roundness, and 
	diameter.

	Variables with the same postfix index together must represent a real piece
	in the database. For example, a reed piece with T1=1mm, D1=18mm, R1=0 might
	exist in the database, while a reed piece with T1=2mm, D1=18mm, R1=0,
	L1 = 200mm may not. 

	This constraint checks if assigned values to Ti, Di, and Ri represent
	pieces in the database or not.'''

	def __init__(self, catalog):
		self.__catalog = catalog
	
	def establish(self, csp, curvar, value):
		'''Establishes consistency after curvar: value assignment.'''
		A = csp.get_assignment()
		D = csp.get_domains()
		catalog = self.__catalog
		node_index = int(curvar[1])
		node_vars = {v+str(node_index) for v in {"T", "R", "D", "L"}}
		filters = self.__filters(A, node_vars)
		examined = set([])
		reduced_vars = set([])
		new_domains = {}
		confset = set(filters.keys())
		for var in {v+str(node_index) for v in {"T", "R", "D", "L"}}:
			if var in A:
				continue
			examined.add(var)
			if var[0] == "L":
				new_L = catalog.l(filters)
				if new_L < D[var]["min"]:
					return (CONTRADICTION, examined, confset) 
				if new_L < D[var]["max"]:
					reduced_vars.add(var)
					new_domains[var] = {"min": D[var]["min"], "max": new_L}
			else:
				new_values = catalog.values(var[0], filters)
				if new_values == CONTRADICTION:
					return (CONTRADICTION, examined, confset)
				if len(new_values) < len(D[var]):
					reduced_vars.add(var)
					new_domains[var] = new_values
		if len(reduced_vars) == 0:
			return (DOMAINS_INTACT, examined)
		for v in reduced_vars:
			csp.update_domain(v, new_domains[v])
		return (DOMAINS_REDUCED, examined, reduced_vars)

	def propagate(self, csp, reduced_vars):
		return (DOMAIN_INTACT, set([]))		

	def __filters(self, A, node_vars):
		'''Builds filters using the assigned var/value pairs.'''
		filters = {}
		for node_var in node_vars:
			if node_var in A:
				filters[node_var[0]] = A[node_var]
		return filters