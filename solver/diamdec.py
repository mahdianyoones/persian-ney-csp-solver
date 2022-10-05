from functools import reduce
from constants import *
import copy

class DIAMDEC():
	'''Implements diameter decrement consistency.
	
        The constraint makes sure the following relations exist between D
        variables:
    
        0.5 <= D2 - D1 <= 1.5
        0.5 <= D3 - D2 <= 1.5
        0.5 <= D4 - D3 <= 1.5
        0.5 <= D5 - D4 <= 1.5
        0.5 <= D6 - D5 <= 1.5
        0.5 <= D7 - D6 <= 1.5

        i.e. the diamater difference between adjacent nodes must 
        fall into an accepted range.

        The accepted range is defined in specs.py as a configuration option,
        having min and max as lower and upper bounds.

        The algorithm assumes that the order of assignments are in the
        order of variables indices. That is D1, D2, D3, D4, D5, D6, and D7.

        This constraint restricts final solutions to conic-shape ones.'''

	def __init__(self, ddiff):
		self.__ddiff = ddiff

	def establish(self, csp, curvar, value):
		'''Establishes consistency W.R.T. diameter dececrement constraint.'''
		if curvar == "D7":
			return (DOMAINS_INTACT, set([]))
		(D_consistent, examined) = self.__consistent(csp, curvar, value)
		if D_consistent == CONTRADICTION:
			return (CONTRADICTION, examined)
		del D_consistent[curvar]
		reduced = set([])
		D = csp.get_domains()
		for v, new_domain in D_consistent.items():
			if len(new_domain) < len(D[v]):
				csp.update_domain(v, new_domain)
				reduced.add(v)
		if len(reduced) > 0:
			return (DOMAINS_REDUCED, examined, reduced)
		return (DOMAINS_INTACT, examined)

	def propagate(self, csp, reduced_vars):
		'''Establishes boundary consistency w.r.t. diamdec constraint.
		
		It is unclear whether a strong consistency algorithm exists for
		propagation of boundary reductions. Temporarily, the propagate
		in this constraint does nothing to see the performance of the
		algorithm without it.
		
		If the impact is significant, then we shall look for an efficient
		algorithm.'''
		return (DOMAINS_INTACT, set([]))

	def __compare(self, A, B, diff):
		'''Checks if values in B (D_i+1) are consistent W.R.T. A (D_i).
		
		i.e. A and B contain domain values for D1&D2, D2&D3, etc
		'''
		mindiff = diff["min"]
		maxdiff = diff["max"]
		A_consistent = set([])
		B_consistent = set([])
		for val_A in A:
			for val_B in B:
				diff = val_A - val_B
				if diff <= maxdiff and diff >= mindiff:
					A_consistent.add(val_A)
					B_consistent.add(val_B)
		return (A_consistent, B_consistent)

	def __consistent(self, csp, curvar, value):
		'''Evaluates unassigned D variables and returns consistent values.'''
		curvar_index = int(curvar[1])
		D_consistent = {"D"+str(i): set([]) for i in range(curvar_index, 8)}
		D_consistent[curvar] = {value}
		examined = set([])
		for i in range(curvar_index, 7):
			var_A = "D"+str(i)
			var_B = "D"+str(i+1)
			A = D_consistent[var_A]
			B = csp.get_domain(var_B)
			(A_consistent, B_consistent) = self.__compare(A, B, self.__ddiff)
			examined.add(var_B)
			if len(A_consistent) == 0 or len(B_consistent) == 0:
				return (CONTRADICTION, examined)
			D_consistent[var_A] = A_consistent
			D_consistent[var_B] = B_consistent
		return (D_consistent, examined)