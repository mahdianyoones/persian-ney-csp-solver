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
		self.__d_backup = {} # order matters
		self.__init_domains()
		self.__unary()
		self.__init_constraints()
	
	def update_d(self, var, new_domain):
		self.D[var] = new_domain
		
	def print_ds(self, _vars):
		print()
		for var in sorted(_vars):
			if var[0] == "L":
				print(var, ": [", self.D[var]["min"], "...", self.D[var]["max"], "]")
			else:
				print(var, ": ", sorted(self.D[var]))
		print()
	
	def backup_d(self):
		self.d_backup = copy.deepcopy(self.D)
	
	def revert_d(self):
		self.D = copy.deepcopy(self.d_backup)
	
	def __unary(self):
		'''Makes variables unary consistent.'''
		topd = self.spec["topd"]
		holed = self.spec["holed"]
		hmarg = self.spec["hmarg"]
		# Applying diameter range for D1
		for diam in self.D["D1"].copy():
			if diam < topd["min"] or diam > topd["max"]:
				self.D["D1"].remove(diam)
		# Applying minimum chunk length for all L vars
		for l_var in self.l_vars:
			self.D[l_var]["min"] = self.spec["minl"]
		# Increasing min of some Ls to contain holes and margins
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
