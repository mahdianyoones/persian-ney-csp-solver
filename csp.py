class CSP():
	
	def getC(self):
		return self.C
	
	def getVars(self):
		return self.X
		
	def varDomain(self, var):
		return self.D[var].copy()
	
	def Dsize(self, var):
		if var[1] == "L":
			return self.D[var]["max"] - self.D[Lvar]["min"]
		return len(self.D[var])
			
	def initC(self):
		self.C["inStock"] = self.X
		self.C["len"] = {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}
		self.C["sameTH"] = {"TH1", "TH2", "TH3", "TH4", "TH5", "TH6", "TH7"}
		self.C["sameR"] = {"R1", "R2", "R3", "R4", "R5", "R6", "R7"}
		self.C["Ldec"] = {"L2", "L3", "L4", "L5", "L6", "L7"}
		self.C["Ddec"] = {"D1", "D2", "D3", "D4", "D5", "D6", "D7"}
		self.C["L1_half_L2"] = {"L1", "L2"}
		self.C["h1"] = {"L1", "L2", "L3"}
		self.C["h2"] = {"L1", "L2", "L3"}
		self.C["h3"] = {"L1", "L2", "L3", "L4"}
		self.C["h4"] = {"L1", "L2", "L3", "L4"}
		self.C["h5"] = {"L1", "L2", "L3", "L4"}
		self.C["h6"] = {"L1", "L2", "L3", "L4", "L5"}
			
	def unary(self):
		'''Makes variables unary consistent.'''
		for diam in self.D["D1"]:
			if diam < spec["topd"]["min"] or diam > spec["topd"]["max"]:
				self.D["D1"].remove(diam)
		for Lvar in self.Lvars:
			self.D[Lvar]["min"] = spec["minl"]
		self.D["L6"]["min"] = spec["hmarg"] * 2 + spec["holed"] * 1 # 1 hole
		self.D["L5"]["min"] = spec["hmarg"] * 4 + spec["holed"] * 3 # 3 holes
		self.D["L4"]["min"] = spec["hmarg"] * 3 + spec["holed"] * 2 # 2 holes
	
	def initD(self):
		for Lvar in self.Lvars:
			self.D[Lvar] = {"min": 0, "max": float("inf")}
		ds = self.catalog.values("D")
		ths = self.catalog.values("TH")
		rs = self.catalog.values("R")
		for Dvar in self.Dvars:
			self.D[Dvar] = ds
		for Rvar in self.Rvars:
			self.D[Rvar] = rs
		for THvar in self.THvars:
			self.D[THvar] = ths

	def __init__(self, spec, catalog):
		self.catalog = catalog
		self.spec = spec
		self.Lvars = {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}
		self.Dvars = {"D1", "D2", "D3", "D4", "D5", "D6", "D7"}
		self.Rvars = {"R1", "R2", "R3", "R4", "R5", "R6", "R7"}
		self.THvars = {"TH1", "TH2", "TH3", "TH4", "TH5", "TH6", "TH7"}
		self.X = self.Lvars.union(self.Dvars, self.THvars, self.Rvars)
		self.C = {}
		self.learnedC = set([])
		self.D = {}
		self.R = {} # Relations for learned constraints
		self.initD()
		self.unary()
		self.initC()
