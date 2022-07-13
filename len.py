from constants import *

class LEN():
	'''Makes L variables consistent W.R.T len constraint.
	
	This is probably the last constraint before a solution can
	be found. It enforces the overall length of the Ney.
	
	The following updates can occur:
	
	L1 = len - (L2+L3+L4+L5+L6+L7)
	L2 = len - (L1+L3+L4+L5+L6+L7)
	L3 = len - (L1+L2+L4+L5+L6+L7)
	L4 = len - (L1+L2+L3+L5+L6+L7)
	L6 = len - (L1+L2+L3+L4+L5+L7)
	L7 = len - (L1+L2+L3+L4+L5+L6)
	
	where h1 is the length of the Ney.
	'''

	def __init__(self, csp, asmnt):
		self.csp = csp
		self.asmnt = asmnt
	
	def b_update(self):
		return (DOMAINS_INTACT, None)
	
	def establish(self, curvar, value):
		assigned_ls = set([])
		unassigned_l = None
		_sum = 0
		for i in range(1, 8):
			li = "L"+str(i)
			if li == curvar:
				assigned_ls.add(curvar)
				_sum += value
			elif li in self.asmnt.assigned:
				assigned_ls.add(li)
				_sum += self.asmnt.assignment[li]
			else:
				unassigned_l = li
		if len(assigned_ls) < 6:
			return (DOMAINS_INTACT, None)
		if len(assigned_ls) == 7:
			return (DOMAINS_INTACT, None)
		new_l = self.csp.spec["len"] - _sum # L1 = h1 - (L2+L3+L4+L5+L6+L7)
		old_d = self.csp.D[unassigned_l]
		if new_l < old_d["min"] or new_l > old_d["max"]:
			confset = assigned_ls
			return (CONTRADICTION, confset, "len")
		new_d = {"min": new_l, "max": new_l}
		self.csp.D[unassigned_l] = new_d
		return (DOMAINS_REDUCED, set([unassigned_l]))
