from constants import *

class DIAM_STOCK():
	'''Implements consistency for diam_stock contrains.

	Details and descriptions of round_stock apply here too.'''

	def __init__(self, catalog):
		self.__catalog = catalog
	
	def establish(self, csp, curvar, value):
		'''Establishes consistency after curvar: value assignment.'''
		A = csp.get_assignment()
		D = csp.get_domains()
		catalog = self.__catalog
		Di = "D"+curvar[1]
		if curvar == Di:
			return REVISED_NONE
		Ti, Ri = ("T"+curvar[1], "R"+curvar[1])
		filters = {key[0]: A[key] for key in {Ti, Ri}.intersection(A.keys())}
		found_values = catalog.values("D", filters)
		if found_values == NODE_NOT_FOUND:
			return CONTRADICTION
		new_domain = D[Di].intersection(found_values)
		if len(new_domain) < len(D[Di]):
			reduced_vars = {Di}
			csp.update_domain(Di, new_domain)
			return (MADE_CONSISTENT, reduced_vars)
		return ALREADY_CONSISTENT

	def propagate(self, csp, reduced_vars):
		return REVISED_NONE