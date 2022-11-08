from constants import *

class ROUND_STOCK():
	'''Implements consistency for higher-order round_stock contrains.

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
	
	def establish(self, csp, curvar, value, participants):
		'''Establishes consistency after curvar: value assignment.'''
		i = curvar[1]
		Ri = "R"+i
		if curvar == Ri:
			return REVISED_NONE
		assigned_vars = csp.get_assigned_vars()
		participants = participants.intersection(assigned_vars)
		if len(participants) == 0:
			raise Exception("curvar looks wrong", curvar)
		A = csp.get_assignment()
		D = csp.get_domains()
		catalog = self.__catalog
		Di, Ti = ("D"+i, "T"+i)
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

	def propagate(self, csp, reduced_vars, participants):
		return REVISED_NONE        

class THICK_STOCK():
	'''Implements consistency for higher_order thick_stock contrains.

	Details and descriptions of round_stock apply here too.'''

	def __init__(self, catalog):
		self.__catalog = catalog
	
	def establish(self, csp, curvar, value, participants):
		'''Establishes consistency after curvar: value assignment.'''
		i = curvar[1]
		Ti = "T"+i
		if curvar == Ti:
			return REVISED_NONE
		assigned_vars = csp.get_assigned_vars()
		participants = participants.intersection(assigned_vars)
		if len(participants) == 0:
			raise Exception("curvar looks wrong", curvar)
		A = csp.get_assignment()
		D = csp.get_domains()
		catalog = self.__catalog
		Di, Ri = ("D"+i, "R"+i)
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

	def propagate(self, csp, reduced_vars, participants):
		return REVISED_NONE

class DIAM_STOCK():
	'''Implements consistency for higher_order diam_stock contrains.

	Details and descriptions of round_stock apply here too.'''

	def __init__(self, catalog):
		self.__catalog = catalog
	
	def establish(self, csp, curvar, value, participants):
		'''Establishes consistency after curvar: value assignment.'''
		i = curvar[1]
		Di = "D"+i
		if curvar == Di:
			return REVISED_NONE
		assigned_vars = csp.get_assigned_vars()
		participants = participants.intersection(assigned_vars)
		if len(participants) == 0:
			raise Exception("curvar looks wrong", curvar)
		A = csp.get_assignment()
		D = csp.get_domains()
		catalog = self.__catalog
		Ti, Ri = ("T"+i, "R"+i)
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

	def propagate(self, csp, reduced_vars, participants):
		return REVISED_NONE

class PIECE_STOCK():
	'''Implements consistency for higher_order piece_stock contrains.

	Details and descriptions of round_stock apply here too.'''

	def __init__(self, catalog):
		self.__catalog = catalog
	
	def establish(self, csp, curvar, value, participants):
		'''Establishes consistency after curvar: value assignment.'''
		i = curvar[1]
		Pi = "P"+i
		if curvar == Pi:
			return REVISED_NONE
		assigned_vars = csp.get_assigned_vars()
		participants = participants.intersection(assigned_vars)
		if len(participants) == 0:
			raise Exception("curvar looks wrong", curvar)
		A = csp.get_assignment()
		D = csp.get_domains()
		catalog = self.__catalog
		Di, Ri, Ti = ("D"+i, "R"+i, "T"+i)
		filters = {key[0]: A[key] for key in {Di, Ri, Ti}.intersection(A.keys())}
		found_values = catalog.pieces(filters)
		if found_values == NODE_NOT_FOUND:
			return CONTRADICTION
		new_domain = D[Pi].intersection(found_values)
		if len(new_domain) < len(D[Pi]):
			reduced_vars = {Pi}
			csp.update_domain(Pi, new_domain)
			return (MADE_CONSISTENT, reduced_vars)
		return ALREADY_CONSISTENT

	def propagate(self, csp, reduced_vars, participants):
		return REVISED_NONE