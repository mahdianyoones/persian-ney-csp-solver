import copy

class UNARY():
	'''Implements unary constraints.'''

	def unarify(self, csp, catalog, spec):
		'''Executes all unary consistency methods.'''
		self.__initial_domains(csp, catalog)
		self.__nodes_min_len(csp, spec)
		self.__sixth_node_min_len(csp, spec)
		self.__first_node_diameter(csp, spec)
		self.__fourth_node_two_holes(csp, spec)
		self.__fifth_node_three_holes(csp, spec)

	def __nodes_min_len(self, csp, spec):
		'''All nodes initially have a minimum lower and no upper bound.'''
		X = csp.get_variables()
		_min = spec["minl"]
		_inf = float("inf")
		for var in X:
			if var[0] == "L":
				csp.update_domain(var, {"min": _min, "max": _inf})

	def __sixth_node_min_len(self, csp, spec):
		'''Node 6 must be long enough to contain at least one hole.'''		
		X = csp.get_variables()
		L6 = csp.get_domain("L6")
		new_d = copy.deepcopy(L6)
		new_d["min"] = spec["hmarg"] * 2 + spec["holed"] * 1
		csp.update_domain("L6", new_d)
				
	def __initial_domains(self, csp, catalog):
		'''Defines initial values for domains of all vars except Ls.'''
		X = csp.get_variables()
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

	def __first_node_diameter(self, csp, spec):
		'''Node 1 cannot have a diameter below a certain value (e.g. 18mm).'''
		D1 = csp.get_domain("D1")
		legal_values = set([])
		for diam in D1:
			if diam >= spec["topd"]["min"] and diam <= spec["topd"]["max"]:
				legal_values.add(diam)
		csp.update_domain("D1", legal_values)

	def __fourth_node_two_holes(self, csp, spec):
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

	def __fifth_node_three_holes(self, csp, spec):
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