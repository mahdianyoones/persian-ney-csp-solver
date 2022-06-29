from constants import *

class IN_STOCK():
	'''Establishes consistency W.R.T. in_stock constraint.'''

	def __init__(self, csp):
		self.csp = csp
	
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
		
	def filters_impacted(self, asmnt, curvar, value):
		'''Builds filters dictionary and detects impacted variables.'''
		i = self.var_i(curvar)
		_vars = {"R"+i, "TH"+i, "D"+i}
		node = asmnt.nodes[i]
		filters = {}
		impacted = set({})
		for var in _vars:
			var_name = self.var_name(var)
			if var == curvar:
				filters[var_name] = value
			elif node[var_name] == FEATURE_IS_SET:
				filters[var_name] = asmnt.assignment[var]
			else:
				impacted.add(var)
		return (filters, impacted)
	
	def update_thrd(self, filters, impacted):
		'''Updates impacted variables and returns success/contradiction.'''
		for var in impacted.copy():
			var_name = self.var_name(var)
			new_domain = self.csp.catalog.values(var_name, filters)
			current_domain = self.csp.D[var]
			new_domain = new_domain.intersection(current_domain)
			if len(new_domain) == 0:
				return (CONTRADICTION, set([]))
			if new_domain == current_domain:
				impacted.remove(var)
			else:
				self.csp.update_d(var, new_domain)
		if len(impacted) == 0:
			return (DOMAINS_INTACT, None)
		else:
			return (DOMAINS_REDUCED, impacted)
		
	def update_l(self, filters, i, node):
		'''Updates an L variable using the given filters.'''
		if node["L"] == FEATURE_IS_NOT_SET:
			last_d = self.csp.D["L"+i]
			new_d = last_d.copy()
			new_d["max"] = self.csp.catalog.get_l(filters)
			if new_d["max"] < new_d["min"]:
				return (CONTRADICTION, set([]))
			if new_d["max"] < last_d["max"]:			
				self.csp.update_d("L"+i, new_d)
				return (DOMAINS_REDUCED, "L"+i)
		return (DOMAINS_INTACT, None)
	
	def b_update(self, asmnt):
		return (DOMAINS_INTACT, None)
	
	def establish(self, asmnt, curvar, value):
		if self.var_name(curvar) == "L":
			return (DOMAINS_INTACT, None)
		(filters, impacted) = self.filters_impacted(asmnt, curvar, value)
		i = self.var_i(curvar)
		node = asmnt.nodes[i]
		self.asmnt = asmnt
		confset = filters.keys()
		thrd_res = self.update_thrd(filters, impacted)
		if thrd_res[0] == CONTRADICTION:
			return thrd_res
		l_res = self.update_l(filters, i, node)
		if l_res[0] == CONTRADICTION:
			return l_res
		if l_res[0] == DOMAINS_REDUCED:
			impacted.add(l_res[1]) # impacted l
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)
		else:
			return (DOMAINS_INTACT, None)
