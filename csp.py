import copy

class CSP():

	def __init__(self, catalog, spec):
		self.__catalog = catalog
		self.__spec = spec
		self.__l_vars = {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}
		self.__d_vars = {"D1", "D2", "D3", "D4", "D5", "D6", "D7"}
		self.__r_vars = {"R1", "R2", "R3", "R4", "R5", "R6", "R7"}
		self.__th_vars = {"TH1", "TH2", "TH3", "TH4", "TH5", "TH6", "TH7"}
		self.__X = self.l_vars.union(self.d_vars, self.th_vars, self.r_vars)
		self.__C = {}
		self.__D = {}
		self.__domains_backup = [] # order matters
		self.__init_domains()
		self.__unary()
		self.__init_constraints()
		self.__assignment = {}
		self.__unassigned = copy.deepcopy(self.__X)
		self.__assigned = [] # order matters
		self.__nodes = {}
		for i in [1, 2, 3, 4, 5, 6, 7]:			
			self.__nodes[str(i)] = {
				"D": 	FEATURE_IS_NOT_SET, 
				"R": 	FEATURE_IS_NOT_SET, 
				"TH": 	FEATURE_IS_NOT_SET,
				"L": 	FEATURE_IS_NOT_SET
			}
	
	def get_spec(self, key):
		return self.__spec[key]
	
	def get_node(self, i):
		return self.__nodes[i]
		
	def update_domain(self, var, new_domain):
		self.__D[var] = new_domain
	
	def backup_domains(self):
		self.__domains_backups.append(copy.deepcopy(self.__D))
	
	def revert_domains(self):
		self.__D = copy.deepcopy(self.__domains_backups.pop())
	
	def get_assignment(self):
		return self.__assignment
	
	def assigned_count(self):
		return len(self.__assigned)
	
	def unassigned_count(self):
		return len(self.__unassigned)
		
	def assign(self, var, val):
		self.__assignment[var] = val
		self.__unassigned.remove(var)
		self.__assigned.append(var) # order matters
		var_i = self.var_i(var)
		var_name = self.var_name(var)
		self.__nodes[str(var_i)][var_name] = FEATURE_IS_SET
	
	def unall(self):
		self.assignment = {}
		self.unassigned = copy.deepcopy(self.csp.X)
		self.assigned = [] # order matters
		self.nodes = {}
		for i in [1, 2, 3, 4, 5, 6, 7]:			
			self.__nodes[str(i)] = {
				"D": 	FEATURE_IS_NOT_SET, 
				"R": 	FEATURE_IS_NOT_SET, 
				"TH": 	FEATURE_IS_NOT_SET,
				"L": 	FEATURE_IS_NOT_SET
			}
	
	def get_variables(self):
		return self.__X
	
	def get_domains(self):
		return self.__D
	
	def get_domain(self, var):
		return self.__D[var]
	
	def get_participants(self, constraint):
		return self.__C[constraint]
	
	def unassign(self, var):
		if var in self.unassigned:
			raise Exception(var, " is already unassigned.")
		del self.assignment[var]
		self.unassigned.add(var)
		del self.assigned[self.assigned.index(var)]
		var_i = self.var_i(var)
		var_name = self.var_name(var)
		self.nodes[str(var_i)][var_name] = FEATURE_IS_NOT_SET
		
		self.__assignment = {}
		self.__unassigned = copy.deepcopy(self.csp.X)
		self.__assigned = [] # order matters
		self.__nodes = {}
		for i in [1, 2, 3, 4, 5, 6, 7]:			
			self.__nodes[str(i)] = {
				"D": 	FEATURE_IS_NOT_SET, 
				"R": 	FEATURE_IS_NOT_SET, 
				"TH": 	FEATURE_IS_NOT_SET,
				"L": 	FEATURE_IS_NOT_SET
			}
				
	def __d1_diameters(self, d1, topd):
		'''Returns the diameters allowed for D1.
		
		This is a mathematical function.'''
		diameters = set([])
		for diam in d1:
			if diam >= topd["min"] and diam <= topd["max"]:
				diameters.add(diam)
		return diameters		
	
	def __unary(self):
		'''Makes variables unary consistent.'''
		holed = self.spec["holed"]
		hmarg = self.spec["hmarg"]
		topd = self.spec["topd"]
		self.D["D1"] = self.__d1_diameters(self.D["D1"], topd)
		# minimum chunk length
		for l_var in self.l_vars:
			self.D[l_var]["min"] = self.spec["minl"]
		# nodes should contain holes and margins
		self.D["L6"]["min"] = hmarg * 2 + holed * 1 # 1 hole
		self.D["L5"]["min"] = hmarg * 4 + holed * 3 # 3 holes
		self.D["L4"]["min"] = hmarg * 3 + holed * 2 # 2 holes
	
	def __init_domains(self):
		for l_var in self.l_vars:
			self.D[l_var] = {"min": 0, "max": float("inf")}
		diameters = self.catalog.values("D")
		thicknesses = self.catalog.values("TH")
		roundnesses = self.catalog.values("R")
		for d_var in self.d_vars:
			self.D[d_var] = copy.deepcopy(diameters)
		for r_var in self.r_vars:
			self.D[r_var] = copy.deepcopy(roundnesses)
		for th_var in self.th_vars:
			self.D[th_var] = copy.deepcopy(thicknesses)

	def __init_constraints(self):
		self.C["same_th"] = {"TH1", "TH2", "TH3", "TH4", "TH5", "TH6", "TH7"}
		self.C["same_r"] = {"R1", "R2", "R3", "R4", "R5", "R6", "R7"}
		self.C["d_dec"] = {"D1", "D2", "D3", "D4", "D5", "D6", "D7"}
		self.C["in_stock"] = self.d_vars.union(self.th_vars, self.r_vars)
		self.C["l1_half_l2"] = {"L1", "L2"}
		self.C["l_dec"] = {"L2", "L3", "L4", "L5", "L6", "L7"}
		self.C["h1"] = {"L1", "L2", "L3"}
		self.C["h2"] = {"L1", "L2", "L3"}
		self.C["h3"] = {"L1", "L2", "L3", "L4"}
		self.C["h4"] = {"L1", "L2", "L3", "L4"}
		self.C["h5"] = {"L1", "L2", "L3", "L4"}
		self.C["h6"] = {"L1", "L2", "L3", "L4", "L5"}
		self.C["len"] = {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}
		self.constraint_orders = {
			"same_th": 1, # goes frist
			"same_r": 2,
			"d_dec": 3,
			"in_stock": 4,
			"l1_half_l2": 5,
			"l_dec": 6,
			"h1": 7,
			"h2": 8,
			"h3": 9,
			"h4": 10,
			"h5": 11,
			"h6": 12,
			"len": 13
		}
