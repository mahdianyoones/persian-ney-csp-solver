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
		
	def var_i(self, var):
		if var[0] in {"R", "D", "L"}:
			return var[1]
		else:
			return var[2]
	
	def var_name(self, var):
		if len(var) == 2:
			return var[0]
		else:
			return var[0:2]
	
	def impacted(self, asmnt, var_name, curvar):
		impacted = set([])
		for i, node in asmnt.nodes.items():
			if node[var_name] == FEATURE_IS_SET:
				return set([])
			var = var_name+str(i)
			if var != curvar:
				impacted.add(var)
		return impacted
		
	def establish(self, asmnt, curvar, value):
		var_name = self.var_name(curvar)
		impacted = self.impacted(asmnt, var_name, curvar)
		if len(impacted) < 6:
			return (DOMAINS_INTACT, None)
		for imvar in impacted.copy():
			domain = self.csp.D[imvar]
			if not value in domain:
				return (CONTRADICTION, set([]))
			if len(domain) == 1: # no change
				impacted.remove(imvar)
				continue
			self.csp.update_d(imvar, set([value]))
		if len(impacted) == 0:
			return (DOMAINS_INTACT, None)
		return (DOMAINS_REDUCED, impacted)	
