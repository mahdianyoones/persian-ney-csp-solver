class CSP():

	def __init__(self, catalog, spec):
		self.catalog = catalog
		self.spec = spec
		self.l_vars = {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}
		self.d_vars = {"D1", "D2", "D3", "D4", "D5", "D6", "D7"}
		self.r_vars = {"R1", "R2", "R3", "R4", "R5", "R6", "R7"}
		self.th_vars = {"TH1", "TH2", "TH3", "TH4", "TH5", "TH6", "TH7"}
		self.X = self.l_vars.union(self.d_vars, self.th_vars, self.r_vars)
		self.C = {}
		self.D = {}
		self.d_backup = [] # order matters
		self.R = {} 		# Relations for learned constraints
		self.init_d()
		self.unary()
		self.init_c()
	
	def update_d(self, var, new_domain):
		self.D[var] = new_domain
		
	def backup_d(self):
		self.d_backup = self.D.copy()
		
	def revert_d(self):
		self.D = self.d_backup.copy()
	
	def print_ds(self, _vars):
		print()
		for var in sorted(_vars):
			if var[0] == "L":
				print(var, ": [", self.D[var]["min"], "...", self.D[var]["max"], "]")
			else:
				print(var, ": ", sorted(self.D[var]))
		print()
	
	def unary(self):
		'''Makes variables unary consistent.'''
		topd = self.spec["topd"]
		holed = self.spec["holed"]
		hmarg = self.spec["hmarg"]
		for diam in self.D["D1"].copy():
			if diam < topd["min"] or diam > topd["max"]:
				self.D["D1"].remove(diam)
		for l_var in self.l_vars:
			self.D[l_var]["min"] = self.spec["minl"]
		self.D["L6"]["min"] = hmarg * 2 + holed * 1 # 1 hole
		self.D["L5"]["min"] = hmarg * 4 + holed * 3 # 3 holes
		self.D["L4"]["min"] = hmarg * 3 + holed * 2 # 2 holes
	
	def init_d(self):
		for l_var in self.l_vars:
			self.D[l_var] = {"min": 0, "max": float("inf")}
		diameters = self.catalog.values("D")
		thicknesses = self.catalog.values("TH")
		roundnesses = self.catalog.values("R")
		for d_var in self.d_vars:
			self.D[d_var] = diameters.copy()
		for r_var in self.r_vars:
			self.D[r_var] = roundnesses.copy()
		for th_var in self.th_vars:
			self.D[th_var] = thicknesses.copy()
	
	def init_c(self):
		self.C["in_stock"] = self.X
		self.C["len"] = {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}
		self.C["same_th"] = {"TH1", "TH2", "TH3", "TH4", "TH5", "TH6", "TH7"}
		self.C["same_r"] = {"R1", "R2", "R3", "R4", "R5", "R6", "R7"}
		self.C["l_dec"] = {"L2", "L3", "L4", "L5", "L6", "L7"}
		self.C["d_dec"] = {"D1", "D2", "D3", "D4", "D5", "D6", "D7"}
		self.C["l1_half_l2"] = {"L1", "L2"}
		self.C["h1"] = {"L1", "L2", "L3"}
		self.C["h2"] = {"L1", "L2", "L3"}
		self.C["h3"] = {"L1", "L2", "L3", "L4"}
		self.C["h4"] = {"L1", "L2", "L3", "L4"}
		self.C["h5"] = {"L1", "L2", "L3", "L4"}
		self.C["h6"] = {"L1", "L2", "L3", "L4", "L5"}	
