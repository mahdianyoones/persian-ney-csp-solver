import copy

class UNARY():
	
	def unarify(self, csp, catalog, spec):
		'''Initiates the domain of vars and makes them unary consistent.'''
		X = csp.get_variables()
		self.__establish_L(csp, spec, X)
		self.__establish_holes_space(csp, spec)
		self.__establish_RTD(csp, catalog, X)
		self.__establish_D1(csp, spec)
		self.__establish_L4(csp, spec)
		self.__establish_L5(csp, spec)

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

	def __establish_L4(self, csp, spec):
		'''Implements a length constraint on L4.
			
			The goal is to ensure holes 1 and 2 fall on node 4.

			The following relation helps achieve this goal:
			
			L4 >= 2*hole_margin + 2*hole_diameter + h2 - h1 - hole_diameter
			
			which defines a minimum length for L4.'''
		h2_h1_dist = spec["h2"] - spec["h1"]
		new_min = 2*spec["hmarg"] + spec["holed"] + h2_h1_dist
		# TODO: Should we check for contradiction here or not?
		L4 = csp.get_domain("L4")
		csp.update_domain("L4", {"min": new_min, "max": L4["max"]})

	def __establish_L5(self, csp, spec):
		'''Implements a length constraint on L5.
			
			The goal is to ensure holes 3, 4, and 5 falls on node 5.

			The following relation helps achieve this goal:
			
			L5 >= two distances from top and bottom + distance between holes
			3 & 5 + 3 hole diameters
			
			which defines a minimum length for L5.'''
		h3_h5_dist = spec["h5"] - spec["h3"]
		new_min = 2*spec["hmarg"] + spec["holed"] + h3_h5_dist
		# TODO: Should we check for contradiction here or not?
		L5 = csp.get_domain("L5")
		csp.update_domain("L5", {"min": new_min, "max": L5["max"]})