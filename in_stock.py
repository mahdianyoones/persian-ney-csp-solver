from constants import *

class IN_STOCK():
	'''Establishes consistency W.R.T. in_stock constraint.'''

	def __init__(self, csp):
		self.csp = csp
	
	def filters_impacted(self, asmnt, curvar, value):
		'''Builds filters dictionary and detects impacted variables.'''
		i = curvar[1]
		_vars = {"R"+i, "TH"+i, "D"+i}
		node = asmnt.nodes[i]
		asmnt = asmnt.assignment
		assignment = set([])
		for var in _vars:
			if var == curvar:
				filters[var] = value
			elif node[var[0]] == FEATURE_IS_SET:
				filters[var] = assignment(var)
			else:
				impacted.add(var)
		return (filters, impacted)
	
	def update_thrd(self, filters, impacted):
		'''Updates impacted variables and returns success/contradiction.'''
		for var in impacted:
			new_d = self.csp.catalog.values(var, filters)
			if len(new_d) == 0:
				return (CONTRADICTION, set(filters.keys()))
			self.csp.update_d(var, new_d)
		return (DOMAINS_REDUCED)
		
	def update_l(self, filters, i, node):
		'''Updates an L variable using the given filters.'''
		if node["L"] == FEATURE_IS_NOT_SET:
			last_d = self.csp.D["L"+i]
			new_d = last_d.copy()
			new_d["max"] = self.csp.catalog.get_l(filters)
			if new_d["max"] < new_d["min"]:
				return (CONTRADICTION, set(filters.keys()))
			if new_d["max"] < last_d["max"]:			
				self.csp.update_d("L"+i, new_d)
				return (DOMAINS_REDUCED, "L"+i)
		return (DOMAINS_INTACT, None)
	
	def b_update(self, asmnt):
		return (DOMAINS_INTACT, None)
	
	def establish(self, asmnt, curvar, value):
		if curvar[0] in ["R", "D", "TH"]:
			return (DOMAINS_INTACT, None)
		(filters, impacted) = self.filters_impacted(asmnt, curvar, value)
		i = curvar[1]
		node = self.asmnt.nodes[curvar[1]]
		self.asmnt = asmnt
		confset = filters.keys()
		thrd_res = self.update_thrd(filters, impacted)
		if thrd_res[0] == CONTRADICTION:
			return thrd_res
		l_res = self.update_l(filters)
		if l_res[0] == CONTRADICTION:
			return l_res
		if l_res[0] == DOMAINS_REDUCED:
			impacted.add(l_res[1]) # impacted l
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)
		else:
			return (DOMAINS_INTACT, None)
