from constants import *

class SAME_THR():
	'''Applies same thickness and roundness constraints.
	
	If updatables set contains less than 6 TH or R variables, it means
	TH and R variables are already made consistent and further attempts
	would not further reduce any domain.
	
	Note that conflict set is empty since the algorithm makes all neighbors
	consistent in one-go. There are no direct culpirits in the assignment to 
	return as the conflict set.
	
	Resolving the contradictions due to this constraint are done only via
	backtracking. No backjumping is possible.
	'''

	def __init__(self, csp):
		self.csp = csp
	
	def b_update(self, asmnt):
		'''It might be expensive to check bounds many many times!'''
		return (DOMAINS_INTACT, None)
		
	def establish(self, asmnt, curvar, value):
		impacted_rs = set([])
		impacted_ths = set([])
		for i in range(1, 8):
			if curvar[0] == "R‌" and "R"+i != curvar:
				impacted_rs.add("R"+i)
			elif curvar[0] == "TH" and "TH"+i != curvar:
				impacted_ths.add("TH"+i)
		if len(impacted_rs) == 6:
			impacted = impacted_rs
		elif len(impacted_ths) == 6:
			impacted = impacted_ths
		else:
			return (DOMAINS_INTACT, None)
		asmnt = self.asmnt.assignment
		i = curvar[1]
		impacted = []
		new_d = set([value])
		for var in impacted.copy():
			last_d = self.csp.D[var]
			if not value in last_d:
				return (CONTRADICTION, set([]))
			if len(last_d) == 1: # no change
				impacted.remove(var)
				continue
			self.csp.update_d(curvar, new_d)
		return (DOMAINS_REDUCED, impacted)	
