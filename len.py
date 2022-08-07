from constants import *
from base import BASE

class LEN(BASE):
	'''Makes L variables consistent W.R.T. len constraint.
	
	This is probably the last constraint before a solution can
	be found. It enforces the overall length of the Ney.'''

	def __init__(self, csp, asmnt):
		self.__csp = csp
		self.__asmnt = asmnt
	
	def b_update(self, reduced_vars):
		return (DOMAINS_INTACT, set([]))
	
	def establish(self, curvar, value):
	'''Establishes direct consistency for len.

	The following update happens:
	
	L7 = len - (L1 + L2 + L3 + L4 + L5 + L6)
	
	where len is the length of the Ney.'''
		if curvar != "L6":
			return (DOMAINS_INTACT, set([]))
		_sum = 0
		for i in range(1, 7): # L1 through L6
			li = "L"+str(i)
			if not li in self.asmnt.assigned:
				raise Exception("Problem in select order!")
			_sum += self.asmnt.assignment[li]
		L7 = self.csp.spec["len"] - _sum # L7 = len - (L1+L2+L3+L4+L5+L6)
		d7 = self.csp.D["L7"]
		if L7 < d7["min"] or L7 > d7["max"]:
			confset = {"L1", "L2", "L3", "L4", "L5", "L6"}
			return (CONTRADICTION, confset, "len")
		if d7["min"] == L7:
			return (DOMAINS_INTACT, set([]))
		self.csp.D["L7"] = {"min": L7, "max": L7}
		return (DOMAINS_REDUCED, {"L7"})
