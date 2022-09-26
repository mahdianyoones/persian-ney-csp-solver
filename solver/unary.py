import copy

class UNARY():
	
	def unarify(self, csp, catalog, spec):
		'''Initiates the domain of vars and makes them unary consistent.'''
		X = csp.get_variables()
		self.__establish_L(csp, spec, X)
		self.__establish_holes_space(csp, spec)
		self.__establish_RTD(csp, catalog, X)
		self.__establish_D1(csp, spec)

	def __establish_L(self, csp, spec, X):
		'''Sets infinite positive integer values for all L variables.'''
		domain = {"min": spec["minl"], "max": float("inf")}
		for var in X:
			if var[0] == "L":
				csp.update_domain(var, copy.deepcopy(domain))

	def __establish_holes_space(self, csp, spec):
		'''Makes L4, L5, and L6 consistent W.R.T. minimum node length.
		
		Nodes 4, 5, and 6 contain holes. Between the holes and nodes'
		junction with adjacent nodes must be a minumum space. Also,
		between the holes themselves must be a minimum space.
		'''		
		d = csp.get_domain("L4")
		new_d = copy.deepcopy(d)
		new_d["min"] = spec["hmarg"] * 3 + spec["holed"] * 2
		csp.update_domain("L4", new_d)
		
		d = csp.get_domain("L5")
		new_d = copy.deepcopy(d)
		new_d["min"] =  spec["hmarg"] * 4 + spec["holed"] * 3
		csp.update_domain("L5", new_d)
		
		d = csp.get_domain("L6")
		new_d = copy.deepcopy(d)
		new_d["min"] = spec["hmarg"] * 2 + spec["holed"] * 1
		csp.update_domain("L6", new_d)
				
	def __establish_RTD(self, csp, catalog, X):
		diams = catalog.values("D")
		thicks = catalog.values("T")
		rounds = catalog.values("R")
		for var in X:
			if var[0] == "D":
				csp.update_domain(var, copy.deepcopy(diams))
			elif var[0] == "R":
				csp.update_domain(var, copy.deepcopy(rounds))
			elif var[0] == "T":
				csp.update_domain(var, copy.deepcopy(thicks))

	def __establish_D1(self, csp, spec):
		'''Makes D1 consistent W.R.T. minimum d1 minimum diameter.'''
		d1 = csp.get_domain("D1")
		legal_values = set([])
		for diam in d1:
			if diam >= spec["topd"]["min"] and diam <= spec["topd"]["max"]:
				legal_values.add(diam)
		csp.update_domain("D1", legal_values)
