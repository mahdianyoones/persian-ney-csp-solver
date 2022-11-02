import copy

from solver.constants import CONTRADICTION

class UNARY():
	'''Implements unary constraints.
	
	The algorithms in this class are fairly simple and testing them
	is deemed unnecessary.'''

	def unarify(csp, catalog, spec):
		'''Executes all unary consistency methods.'''
		res = UNARY.__initial_domains(csp, catalog)
		if res == CONTRADICTION:
			return CONTRADICTION
		res = UNARY.__nodes_min_len(csp, spec)
		if res == CONTRADICTION:
			return CONTRADICTION
		res = UNARY.__sixth_node_min_len(csp, spec)
		if res == CONTRADICTION:
			return CONTRADICTION
		res = UNARY.__first_node_diameter(csp, spec)
		if res == CONTRADICTION:
			return CONTRADICTION
		res = UNARY.__fourth_node_two_holes(csp, spec)
		if res == CONTRADICTION:
			return CONTRADICTION
		res = UNARY.__fifth_node_three_holes(csp, spec)
		if res == CONTRADICTION:
			return CONTRADICTION

	def __nodes_min_len(csp, spec):
		'''Defines a minimum length for nodes.'''
		X = csp.get_variables()
		D = csp.get_domains()
		_min = spec["minl"]
		for var in X:
			if var[0] == "L":
				csp.update_domain(var, {"min": _min, "max": D[var]["max"]})

	def __sixth_node_min_len(csp, spec):
		'''Node 6 must be long enough to contain at least one hole.'''		
		X = csp.get_variables()
		L6 = csp.get_domain("L6")
		new_d = copy.deepcopy(L6)
		new_d["min"] = spec["hmarg"] * 2 + spec["holed"] * 1
		if new_d["min"] > L6["max"]:
			return CONTRADICTION
		csp.update_domain("L6", new_d)
				
	def __initial_domains(csp, catalog):
		'''Defines initial values for domains of all vars except Ls.
		
		Contradiction cannot occur at this stage unless the dataset contains
		no pieces.'''
		X = csp.get_variables()
		diams = catalog.values("D")
		if len(diams) == 0:
			return CONTRADICTION
		thicks = catalog.values("T")
		if len(thicks) == 0:
			return CONTRADICTION
		rounds = catalog.values("R")
		if len(rounds) == 0:
			return CONTRADICTION
		l = catalog.l()
		if l == 0:
			return CONTRADICTION
		for var in X:
			if var[0] == "D":
				csp.update_domain(var, copy.deepcopy(diams))
			elif var[0] == "R":
				csp.update_domain(var, copy.deepcopy(rounds))
			elif var[0] == "T":
				csp.update_domain(var, copy.deepcopy(thicks))
			else:
				csp.update_domain(var, {"min": 1, "max": l})

	def __first_node_diameter(csp, spec):
		'''Node 1 cannot have a diameter below a certain value (e.g. 18mm).'''
		D1 = csp.get_domain("D1")
		legal_values = set([])
		for diam in D1:
			if diam >= spec["topd"]["min"] and diam <= spec["topd"]["max"]:
				legal_values.add(diam)
		if len(legal_values) == 0:
			return CONTRADICTION
		csp.update_domain("D1", legal_values)

	def __fourth_node_two_holes(csp, spec):
		'''Implements a length constraint on L4.
			
			The goal is to ensure holes 1 and 2 fall on node 4.

			The following relation helps achieve this goal:
			
			L4 >= 2*hole_margin + 2*hole_diameter + h2 - h1 - hole_diameter
			
			which defines a minimum length for L4.'''
		h2_h1_dist = spec["h2"] - spec["h1"]
		new_min = 2*spec["hmarg"] + spec["holed"] + h2_h1_dist
		L4 = csp.get_domain("L4")
		if new_min > L4["max"]:
			return CONTRADICTION
		csp.update_domain("L4", {"min": new_min, "max": L4["max"]})

	def __fifth_node_three_holes(csp, spec):
		'''Implements a length constraint on L5.
			
			The goal is to ensure holes 3, 4, and 5 falls on node 5.

			The following relation helps achieve this goal:
			
			L5 >= two distances from top and bottom + distance between holes
			3 & 5 + 3 hole diameters
			
			which defines a minimum length for L5.'''
		h3_h5_dist = spec["h5"] - spec["h3"]
		new_min = 2*spec["hmarg"] + spec["holed"] + h3_h5_dist
		L5 = csp.get_domain("L5")
		if new_min > L5["max"]:
			return CONTRADICTION
		csp.update_domain("L5", {"min": new_min, "max": L5["max"]})