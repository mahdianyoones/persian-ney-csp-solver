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
		self.__node_vars = {
			1: {"T1", "R1", "D1", "L1"},
			2: {"T2", "R2", "D2", "L2"},
			3: {"T3", "R3", "D3", "L3"},
			4: {"T4", "R4", "D4", "L4"},
			5: {"T5", "R5", "D5", "L5"},
			6: {"T6", "R6", "D6", "L6"},
			7: {"T7", "R7", "D7", "L7"},
		}
	
	def establish(self, csp, curvar, value):
		'''Establishes consistency after curvar: value assignment.'''
		A = csp.get_assignment()
		D = csp.get_domains()
		catalog = self.__catalog
		i = int(curvar[1])
		filters = self.__filters(A, self.__node_vars[i])
		examined = set([])
		reduced_vars = set([])
		confset = {v+str(i) for v in filters.keys()}
		for var in self.__node_vars[i]:
			if var in A:
				continue
			examined.add(var)
			if var[0] == "L":
				new_L = catalog.l(filters)
				if new_L == NODE_NOT_FOUND or new_L < D[var]["min"]:
					return (CONTRADICTION, set([]), confset)
				if new_L >= D[var]["min"] and new_L < D[var]["max"]:
					reduced_vars.add(var)
					csp.update_domain(var, {"min": D[var]["min"], "max": new_L})
			else:
				new_values = catalog.values(var[0], filters)
				if new_values == NODE_NOT_FOUND:
					return (CONTRADICTION, set([]), confset)
				new_values = D[var].intersection(new_values)
				if len(new_values) == 0:
					return (CONTRADICTION, set([]), confset)
				if new_values != D[var]:
					reduced_vars.add(var)
					csp.update_domain(var, new_values)
		if len(reduced_vars) == 0:
			return (DOMAINS_INTACT, examined)
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