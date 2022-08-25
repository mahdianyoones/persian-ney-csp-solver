class UNARY():

	def __init__(self, csp):
		self.__csp = csp
	
	def unarify(self):
		'''Initiates the domain of vars and makes them unary consistent.'''
		lvars = self.__csp.get_lvars()
		unary.define_L_domains(lvars)
		spec = self.__csp.get_spec()
		self.establish_nodes_min_len(spec)
		self.establish_D1_bound(spec)
		thvars = self.__csp.get_thvars()
		rvars = self.__csp.get_rvars()
		dvars = self.__csp.get_dvars()
		self.define_RTHD_domains(thvars, dvars, rvars)

	def establish_D1_bound(self, spec):
		'''Makes D1 consistent W.R.T. minimum d1 minimum diameter.'''
		d1 = self.__csp.get_domain("D1")
		legal_values = self.__d1_legals(d1, spec["topd"])
		self.update_domain("D1", legal_values)
		for l_var in self.__lvars:
			domain = self.__csp.get_domain(l_var)
			new_domain = copy.deepcopy(domain)
			new_domain["min"] = spec["minl"]
			self.__csp.update_domain(l_var, new_domain)

	def establish_nodes_min_len(self, spec):
		'''Makes L4, L5, and L6 consistent W.R.T. minimum node length.
		
		Nodes 4, 5, and 6 contain holes. Between the holes and nodes'
		junction with adjacent nodes must be a minumum space. Also,
		between the holes themselves must be a minimum space.
		'''
		L4_domain = self.__csp.get_domain("L4")
		L4_new_domain = copy.deepcopy(L4_domain)
		L4_new_domain["min"] = self.__n4_min_len(spec)
		self.__csp.update_domain("L4", L4_new_domain)
		
		L5_domain = self.__csp.get_domain("L5")
		L5_new_domain = copy.deepcopy(L5_domain)
		L5_new_domain["min"] =  self.__n5_min_len(spec)
		self.__csp.update_domain("L5", L5_new_domain)
		
		L6_domain = self.__csp.get_domain("L6")
		L6_new_domain = copy.deepcopy(L6_domain)
		L6_new_domain["min"] = self.__n6_min_len(spec)
		self.__csp.update_domain("L6", L6_new_domain)
		
	def define_L_domains(self, lvars):
		domain = {"min": 1, "max": float("inf")}
		for lvar in lvars:
			self.__csp.update_domain(lvar, domain)
	
	def define_RTHD_domains(self, thvars, dvars, rvars):
		diameters = self.__catalog.values("D")
		thicknesses = self.__catalog.values("TH")
		roundnesses = self.___catalog.values("R")
		for dvar in dvars:
			self.__csp.update_domain(dvar, copy.deepcopy(diameters))
		for rvar in rvars:
			self.__csp.update_domain(rvar, copy.deepcopy(roundnesses))
		for thvar in thvars:
			self.__csp.update_domain(thvar, copy.deepcopy(thicknesses))
			
	def __D1_legals(self, d1, topd):
		'''Returns the diameters allowed for D1.
		
		This is a mathematical function.'''
		diameters = set([])
		for diam in d1:
			if diam >= topd["min"] and diam <= topd["max"]:
				diameters.add(diam)
		return diameters		

	def __n4_min_len(self, spec):
		'''Returns the minimum length for L4 to contain 2 holes.
		
		A mathematical function.'''
		return spec["hmarg"] * 3 + spec["holed"] * 2
		
	def __n5_min_len(self, spec):
		'''Returns the minimum length for L5 to contain 3 holes.
		
		A mathematical function.'''
		return spec["hmarg"] * 4 + spec["holed"] * 3

	def __n6_min_len(self, spec):
		'''Returns the minimum length for L6 to contain 1 holes.
		
		A mathematical function.'''
		return spec["hmarg"] * 2 + spec["holed"] * 1
