from constants import *
from base import BASE
import copy

class IN_STOCK(BASE):
	'''Establishes consistency W.R.T. in_stock constraint.'''

	def __init__(self, csp, asmnt):
		self.csp = csp
		self.asmnt = asmnt
		
	def _establish(self, i):
		'''Establishes consistency for node i.
		
		If ith node is consistent W.R.T. in_stock constraint, it means that
		a chunk with a combination of Di, Ri, and THi values exists.
		
		For example, if i = 4, D4: 13, and R4: 0, this callback checks if 
		chunks with diameter 13 and roundness 0 exists or not. If so, it
		updates the domain TH4 (which is not assigned yet) as well as L4.
		
		Henceforth, the solver can rely on values of TH4 and L4 since these
		values come from stock, not speculation!
		
		Conflict set is clearly the assigned variables in the filters.
		
		For instance, in the above example, if TH4 or L4 runs out of values,
		the conflict set is D4 and R4.
		'''
		contradiction = False
		confset = set([])
		impacted = set([])
		a = self.asmnt.assigned
		node = self.asmnt.nodes[i]
		filters = {}
		confset = {}
		for f, fstatus in node.items():
			if f != "L" and fstatus == FEATURE_IS_SET:
				fvar = f+str(i)
				filters[f] = self.asmnt.assignment[fvar]
				set_vars.add(fvar)
		for f, fstatus in node.items():
			if fstatus == FEATURE_IS_SET:
				continue
			notset_var = f+str(i)
			current_domain = self.csp.D[notset_var]
			if f == "L":
				new_L = self.csp.catalog.get_l(filters)
				if new_L < current_domain["min"]:
					contradiction = True
					break
				if new_L < current_domain["max"]:
					self.csp.D[notset_var]["max"] = new_L
					impacted.add(notset_var)
			else:
				new_domain = self.csp.catalog.values(notset_var, filters)
				new_domain = new_domain.intersection(current_domain)
				if len(new_domain) == 0:
					contradiction = True
					break
				elif len(new_domain) < len(current_domain):
					self.csp.D[notset_var] = new_domain
					impacted.add(notset_var)
		if contradiction:
			confset = set_vars
		return (contradiction, confset, impacted)
	
	def b_update(self, reduced_vars):
		'''Establishes indirect consistency for in_stock constraint.
		
		If the domain of D, R, or TH variables are reduced, it checks 
		the reduction impacts on other dependent variables.
		
		For example, if the domain of TH1 is reduced, the domain of R1, D1
		and L1 might reduce as well.
		
		However, L variables do not impact any varaible W.R.T. this
		constant.
		'''
		checked_Is = {}
		_impacted = {}
		for reduced_var in reduced_vars:
			var_name = self.var_name(reduced_var)
			if var_name == "L":
				continue
			var_i = self.var_i(reduced_var)
			if var_i in checked_Is:
				continue
			(contradiction, confset, impacted) = self._establish(var_i)
			if contradiction:
				return (CONTRADICTION, confset, "in_stock")
			if len(impacted) > 0:
				_impacted.update(impacted)
		if len(_impacted) > 0:
			return (DOMAINS_REDUCED, _impacted)
		return (DOMAINS_INTACT, set([]))
	
	def establish(self, curvar, value):
		'''Makes sure the given chunk exists in the stock using catalog.
		
		catalog needs a filter consists of a combinations of D, TH, and R
		varaibles to make enquiry.
		
		The filter parameter is built using the values in the assignments.
		'''
		var_name = self.var_name(curvar)
		if var_name == "L":
			return (DOMAINS_INTACT, None)
		curvar_i = self.var_i(curvar)
		(contradiction, confset, impacted) = self._establish(curvar_i)
		if contradiction:
			return (CONTRADICTION, confset, "in_stock")
		if len(impacted) > 0:
			(DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, set([]))
