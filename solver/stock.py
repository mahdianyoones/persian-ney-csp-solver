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
		Pi, Di, Ri, Ti = ("P"+i, "D"+i, "R"+i, "T"+i)
		assigned_vars = csp.get_assigned_vars()
		if {Pi, Ti, Ri, Di}.issubset(assigned_vars):
			return REVISED_NONE
		A = csp.get_assignment()
		D = csp.get_domains()
		if curvar == Pi:
			assigned_piece_no, L = value
			pieces = self.__catalog.get_pieces({assigned_piece_no})
			return self.__revise_TRD(csp, A, D, pieces, Ti, Di, Ri)
		else:
			catalog = self.__catalog
			return self.__revise_P(csp, catalog, A, D, Pi, Ti, Di, Ri)

	def propagate(self, csp, reduced_vars, participants):
		'''Propagates reduction of P vars to T, R, and D vars.'''
		reduced_P = None
		for reduced_var in reduced_vars:
			if reduced_var[0] == "P":
				reduced_P = reduced_var
				break
		if reduced_P == None:
			return REVISED_NONE
		A = csp.get_assignment()
		i = reduced_P[1]
		Di, Ri, Ti = ("D"+i, "R"+i, "T"+i)
		assigned_vars = csp.get_assigned_vars()
		if {Ti, Ri, Di}.issubset(assigned_vars):
			return REVISED_NONE
		left_numbers = set([])
		D = csp.get_domains()
		for piece in D[reduced_P]:
			no, L = piece
			left_numbers.add(no)
		pieces = self.__catalog.get_pieces(left_numbers)
		return self.__revise_TRD(csp, A, D, pieces, Ti, Di, Ri)

	def __revise_P(self, csp, catalog, A, D, Pi, Ti, Di, Ri):
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

	def __revise_TRD(self, csp, A, D, pieces, Ti, Di, Ri):
		thicks = set([])
		rounds = set([])
		diams = set([])
		for piece in pieces:
			thicks.add(piece["T"])
			rounds.add(piece["R"])
			diams.add(piece["D"])
		new_reduced_vars = set([])
		if not Ti in A:
			new_Ti_domain = D[Ti].intersection(thicks)
			if len(new_Ti_domain) == 0:
				return CONTRADICTION
			if len(new_Ti_domain) < len(D[Ti]):
				csp.update_domain(Ti, new_Ti_domain)
				new_reduced_vars.add(Ti)
		if not Di in A:
			new_Di_domain = D[Di].intersection(diams)
			if len(new_Di_domain) == 0:
				return CONTRADICTION
			if len(new_Di_domain) < len(D[Di]):
				csp.update_domain(Di, new_Di_domain)
				new_reduced_vars.add(Di)
		if not Ri in A:
			new_Ri_domain = D[Ri].intersection(rounds)
			if len(new_Ri_domain) == 0:
				return CONTRADICTION
			if len(new_Ri_domain) < len(D[Ri]):
				csp.update_domain(Ri, new_Ri_domain)
				new_reduced_vars.add(Ri)
		if len(new_reduced_vars) == 0:
			return ALREADY_CONSISTENT
		return MADE_CONSISTENT, new_reduced_vars