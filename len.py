from constants import *

class LEN():
	'''Makes L variables consistent W.R.T. len constraint.
	
	This is probably the last constraint before a solution can
	be found. It enforces the overall length of the Ney.'''

	def __init__(self, csp):
		self.__csp = csp
	
	def b_update(self, reduced_vars):
		return (DOMAINS_INTACT, set([]))
	
	def __L7(self, A, D, total_len):
		'''Calculates the length of L7.
		
		This is a mathematical function.'''
		L7 = total_len - A["L1"]+A["L2"]+A["L3"]+A["L4"]+A["L5"]+A["L6"]
		if L7 < D["L7"]["min"] or L7 > D["L7"]["max"]:
			return CONTRADICTION
		return L7	
	
	def __has_impact(self, curvar):
		return curvar == "L6"
	
	def establish(self, curvar, value):
		'''Establishes direct consistency for len.

		The following update happens:
		
		L7 = len - (L1 + L2 + L3 + L4 + L5 + L6)
		
		where len is the length of the Ney.'''
		if not self.__has_impact(curvar):
			return (DOMAINS_INTACT, set([]))
		total_len = self.csp.get_spec("len")
		A = self.csp.get_assignment()
		D = self.csp.get_domains()
		L7 = self.__L7(A, D, total_len)
		if L7 == CONTRADICTION:
			confset = {"L1", "L2", "L3", "L4", "L5", "L6"}
			return (CONTRADICTION, confset, "len")
		if D["L7"]["min"] == L7:
			return (DOMAINS_INTACT, set([]))
		self.csp.update_d("L7", {"min": L7, "max": L7})
		return (DOMAINS_REDUCED, {"L7"})
