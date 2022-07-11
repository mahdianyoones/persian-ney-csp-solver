from constants import *
from base import BASE
import copy

class IN_STOCK(BASE):
	'''Establishes consistency W.R.T. in_stock constraint.'''

	def __init__(self, csp, asmnt):
		self.csp = csp
		self.asmnt = asmnt
			
	def filters_impacted(self, curvar, value):
		'''Builds filters dictionary and detects impacted variables.'''
		i = str(self.var_i(curvar))
		node = self.asmnt.nodes[str(i)]
		filters = {}
		impacted = set([])
		for var in {"R"+i, "TH"+i, "D"+i}:
			var_name = self.var_name(var)
			if var == curvar:
				filters[var_name] = value
			elif node[var_name] == FEATURE_IS_SET:
				filters[var_name] = self.asmnt.assignment[var]
			else:
				impacted.add(var)
		return (filters, impacted)
	
	def update_thrd(self, filters, impacted, i):
		'''Updates impacted variables and returns success/contradiction.'''
		for var in impacted.copy():
			var_name = self.var_name(var)
			new_domain = self.csp.catalog.values(var_name, filters)
			current_domain = self.csp.D[var]
			new_domain = new_domain.intersection(current_domain)
			if len(new_domain) == 0:
				return (CONTRADICTION, None)
			if new_domain == current_domain:
				impacted.remove(var)
			else:
				self.csp.update_d(var, new_domain)
		if len(impacted) == 0:
			return (DOMAINS_INTACT, None)
		else:
			return (DOMAINS_REDUCED, impacted)
	
	def confset(self, curvar):
		curvar_i = self.var_i(curvar)
		i = str(curvar_i)
		confset = set([])
		for v in {"R"+i, "TH"+i, "D"+i}:
			if v in self.asmnt.assigned:
				confset.add(v)
		return confset
		
	def update_l(self, filters, i, node):
		'''Updates an L variable using the given filters.'''
		i = str(i)
		if node["L"] == FEATURE_IS_NOT_SET:
			last_d = self.csp.D["L"+i]
			new_d = copy.deepcopy(last_d)
			new_d["max"] = self.csp.catalog.get_l(filters)
			if new_d["max"] < new_d["min"]:
				return (CONTRADICTION, None)
			if new_d["max"] < last_d["max"]:			
				self.csp.update_d("L"+i, new_d)
				return (DOMAINS_REDUCED, "L"+i)
		return (DOMAINS_INTACT, None)
	
	def b_update(self):
		return (DOMAINS_INTACT, None)
	
	def establish(self, curvar, value):
		if curvar[0] == "L":
			return (DOMAINS_INTACT, None)
		(filters, impacted) = self.filters_impacted(curvar, value)
		i = self.var_i(curvar)
		node = self.	asmnt.nodes[str(i)]
		thrd_res = self.update_thrd(filters, impacted, i)
		if thrd_res[0] == CONTRADICTION:
			return (CONTRADICTION, self.confset(curvar), "in_stock")
		l_res = self.update_l(filters, i, node)
		if l_res[0] == CONTRADICTION:
			return (CONTRADICTION, set([]), "in_stock")
		if l_res[0] == DOMAINS_REDUCED:
			impacted.add(l_res[1]) # impacted l
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)
		else:
			return (DOMAINS_INTACT, None)
