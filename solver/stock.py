from distutils.command.config import config
from constants import *

class STOCK():
	'''Implements consistency for stock contrains.

	This constraint is defined on groups of variables Di, Ti, Ri, and Pi; therefore, 
	creating 7 distinct constraints
	{stock(T1, R1, D1, P1), ..., stock(T7, R7, D7, P7)}.

	Theses constraints limit the choises for their participants with regard to
	the pieces in the data set. For example, if R4 is assigned 1, D4 gets
	reduced to diameters of the pieces with roundness = 1, T4 gets reduced to
	thickness of the pieces with roundness = 1, and P4 gets reduced to the
	piece number/length of the pieces with roundness = 1.
		
	Note: Depending on various assigned variables, stock(Ti, Ri, Di, Pi) can
	be viewed as one or several of the following constraints.
	
	Ti = filter by Ri			(when Ri is assigned only)
	Ti = filter by Di
	Ti = filter by Ri & Di		(when Ri and Di are assigned only)

	Ri = filter by Ti
	Ri = filter by Di
	Ri = filter by Ti & Di

	Di = filter by T1
	Di = filter by R1
	Di = filter by T1 & R1

	Pi = filter by Ti
	Pi = filter by Ri
	Pi = filter by Ri
	Pi = filter by Ti & Ri
	Pi = filter by Ti & Di
	Pi = filter by Ri & Di
	Pi = filter by Ri & Di & Ti

	where 1 <= i <= 7
	
	However, this algorithm establoshes consistency for all of the above 
	constraints.'''

	def __init__(self, catalog):
		self.__catalog = catalog
	
	def establish(self, csp, curvar, value):
		'''Establishes consistency after curvar: value assignment.'''
		A = csp.get_assignment()
		D = csp.get_domains()
		catalog = self.__catalog
		Pi = "P"+curvar[1]
		if curvar == Pi:
			return REVISED_NONE
		Di = "D"+curvar[1]
		Ri = "R"+curvar[1]
		Ti = "T"+curvar[1]
		found_values = self.__find_values(A, catalog, Di, Ri, Ti, Pi)
		reduced_vars = set([])
		for v, found_values in found_values.items():
			if found_values == NODE_NOT_FOUND:
				return CONTRADICTION
			new_domain = D[v].intersection(found_values)
			if len(new_domain) < len(D[v]):
				reduced_vars.add(v)
				csp.update_domain(v, new_domain)
		if len(reduced_vars) == 0:
			return ALREADY_CONSISTENT
		return (MADE_CONSISTENT, reduced_vars)

	def propagate(self, csp, reduced_vars):
		return REVISED_NONE

	def __find_values(self, A, catalog, Di, Ri, Ti, Pi):
		filters = {key[0]: A[key] for key in {Di, Ri, Ti}.intersection(A.keys())}
		found_values = {}
		found_values[Pi] = catalog.pieces(filters)
		if not Di in A:
			found_values[Di] = catalog.values("D", filters)
		if not Ri in A:
			found_values[Ri] = catalog.values("R", filters)
		if not Ti in A:
			found_values[Ti] = catalog.values("T", filters)
		return found_values