from constants import *
from base import BASE

class STOCK(BASE):
	'''Establishes consistency W.R.T. in_stock constraint.'''

	def __init__(self, csp):
		self.__csp = csp
		self.__node_vars = {
			1: {"R1", "TH1", "D1"},
			2: {"R2", "TH2", "D2"},
			3: {"R3", "TH3", "D3"},
			4: {"R4", "TH4", "D4"},
			5: {"R5", "TH5", "D5"},
			6: {"R6", "TH6", "D6"},
			7: {"R7", "TH7", "D7"},
		}
	
	def __filters(self, A, node_vars):
		'''Build filters using the assigned var/value pairs.
		
		This is a mathematical function.'''
		filters = {}
		for node_var in node_vars:
			if node_var in A:
				filters[node_var] = A[node_var]
		return filters
	
	def __impactables(self, A, var_i, node_vars, filters):
		'''Returns the set of vars whose domains might reduce.
		
		This is a mathematical function.'''
		ims = {}
		Lvar = "L" + var_i
		if not Lvar in A:
			ims.add(Lvar)
		ims.update(node_vars.difference(filters))
		return ims
		
	def __var_in_stock(self, var, D, filters, catalog):
		'''Checkes whether the domain of var exhausts W.R.T. in stock.
		
		If some values remain, the new legal domain is returned.
		This is a mathematical function.'''
		cur_domain = D[var]
		if var[0] == "L":
			new_L = catalog.get_l(filters)
			if new_L < cur_domain["min"]:
				return CONTRADICTION
			if new_L == cur_domain["max"]:
				return DOMAIN_INTACT
			new_domain = {"min": cur_domain["min"], "max": new_L}
		else:
			new_domain = catalog.values(var, filters)
			new_domain = new_domain.intersection(cur_domain)
			if len(new_domain) == 0:
				return CONTRADICTION			
			if len(new_domain) == len(current_domain):
				return DOMAIN_INTACT
		return new_domain
		
	def __establish(self, curvar):
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
		A = self.__csp.get_assignment()
		D = self.__csp.get_domains()
		catalog = self.csp.catalog
		var_i = self.var_i(curvar)
		node_vars = self.__node_vars[var_i]
		filters = self.__filters(A, node_vars)
		impactables = self.__impactables(A, var_i, node_vars, filters)
		impacted = set([])
		for var in impactables:
			new_domain = self.__var_in_stock(var, D, filters, catalog)
			if new_domain == CONTRADICTION:
				return (CONTRADICTION, filters, "in_stock")
			if new_domain != DOMAIN_INTACT:
				self.__csp.update_d(var, new_domain)
				impacted.add(var)
		if len(impacted) == 0:
			return (DOMAINS_INTACT, set([]))
		return (DOMAINS_REDUCED, impacted)
		
	def b_update(self, reduced_vars):
		'''Establishes indirect consistency for in_stock constraint.
		
		If the domain of D, R, or TH variables are reduced, it checks 
		the reduction impacts on other dependent variables.
		
		For example, if the domain of TH1 is reduced, the domain of R1, D1
		and L1 might reduce as well.
		
		However, L variables do not impact any varaible W.R.T. this
		constant.
		'''
		return self._establish(reduced_vars[0])		
	
	def establish(self, curvar, value):
		'''Makes sure the given chunk exists in the stock using catalog.
		
		catalog needs a filter consists of a combinations of D, TH, and R
		varaibles to make enquiry.
		
		The filter parameter is built using the values in the assignments.
		'''
		return self._establish(curvar)
