from constants import *

class THICK_STOCK():
	'''Implements consistency for piece_stock contrains.

	Details and descriptions of round_stock apply here too.'''

	def __init__(self, catalog):
		self.__catalog = catalog
	
	def establish(self, csp, curvar, value):
		'''Establishes consistency after curvar: value assignment.'''
		A = csp.get_assignment()
		D = csp.get_domains()
		catalog = self.__catalog
		i = curvar[1]
		Pi = "P"+i
		if curvar == Pi:
			return REVISED_NONE
		Di, Ri, Ti = ("D"+i, "R"+i, "T"+i)
		filters = {key[0]: A[key] for key in {Di, Ri, Ti}.intersection(A.keys())}
		found_values = catalog.pieces(filters)
		if found_values == NODE_NOT_FOUND:
			return CONTRADICTION
		new_domain = D[Ti].intersection(found_values)
		if len(new_domain) < len(D[Pi]):
			reduced_vars = {Pi}
			csp.update_domain(Pi, new_domain)
			return (MADE_CONSISTENT, reduced_vars)
		return ALREADY_CONSISTENT

	def propagate(self, csp, reduced_vars):
		return REVISED_NONE