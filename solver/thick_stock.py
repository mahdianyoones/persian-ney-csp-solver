from constants import *

class THICK_STOCK():
	'''Implements consistency for thick_stock contrains.

	Details and descriptions of round_stock apply here too.'''

	def __init__(self, catalog):
		self.__catalog = catalog
	
	def establish(self, csp, curvar, value):
		'''Establishes consistency after curvar: value assignment.'''
		A = csp.get_assignment()
		D = csp.get_domains()
		catalog = self.__catalog
		Ti = "T"+curvar[1]
		if curvar == Ti:
			return REVISED_NONE
		Di, Ri = ("D"+curvar[1], "R"+curvar[1])
		filters = {key[0]: A[key] for key in {Di, Ri}.intersection(A.keys())}
		found_values = catalog.values("T", filters)
		if found_values == NODE_NOT_FOUND:
			return CONTRADICTION
		new_domain = D[Ti].intersection(found_values)
		if len(new_domain) < len(D[Ti]):
			reduced_vars = {Ti}
			csp.update_domain(Ti, new_domain)
			return (MADE_CONSISTENT, reduced_vars)
		return ALREADY_CONSISTENT

	def propagate(self, csp, reduced_vars):
		return REVISED_NONE