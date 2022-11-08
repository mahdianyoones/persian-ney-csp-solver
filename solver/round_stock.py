from constants import *

class ROUND_STOCK():
	'''Implements consistency for round_stock contrains.

	This constraint is defined on groups of variables Di, Ti, Ri; therefore, 
	creating 7 distinct constraints
	{round_stock(T1, R1, D1), ..., round_stock(T7, R7, D7)}.

	These constraints limit the values of Ri variables to those found
	in the dataset with regard to assignments to Di and Ti.

	Note: Depending on various assigned variables, each constraint can
	be further factored into the following constraints.
	
	Ti = filter by Ri			(when Ri is assigned only)
	Ti = filter by Di
	Ti = filter by Ri & Di		(when Ri and Di are assigned only)

	where 1 <= i <= 7
	
	However, this algorithm establushes consistency for all of the above 
	constraints at once since the logic of them all are the same.'''

	def __init__(self, catalog):
		self.__catalog = catalog
	
	def establish(self, csp, curvar, value):
		'''Establishes consistency after curvar: value assignment.'''
		A = csp.get_assignment()
		D = csp.get_domains()
		catalog = self.__catalog
		Ri = "R"+curvar[1]
		if curvar == Ri:
			return REVISED_NONE
		Di, Ti = ("D"+curvar[1], "T"+curvar[1])
		filters = {key[0]: A[key] for key in {Di, Ti}.intersection(A.keys())}
		found_values = catalog.values("R", filters)
		if found_values == NODE_NOT_FOUND:
			return CONTRADICTION
		new_domain = D[Ri].intersection(found_values)
		if len(new_domain) < len(D[Ri]):
			reduced_vars = {Ri}
			csp.update_domain(Ri, new_domain)
			return (MADE_CONSISTENT, reduced_vars)
		return ALREADY_CONSISTENT

	def propagate(self, csp, reduced_vars):
		return REVISED_NONE