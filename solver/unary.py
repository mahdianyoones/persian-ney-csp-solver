import copy
from constants import *
import csv

class UNARY():
	'''Implements unary constraints.
	
	The algorithms in this class are fairly simple and testing them
	is deemed unnecessary.'''

	def unarify(csp, spec):
		'''Executes all unary consistency methods.'''
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

	def init_domains(csp, data_set_path):
		'''Defines initial values for domains of all variables..
		
		Contradiction cannot occur at this stage unless the dataset contains
		no pieces.'''	
		X = csp.get_variables()
		pieces = set([])
		with open(data_set_path) as f:
			reader = csv.reader(f)
			for p in reader:
				L = float(p[1]) * 10 # cm -> mm
				T = float(p[2])
				R = float(p[3])
				D = float(p[4])
				no = p[0]
				pieces.add((no, L, T, R, D))
		if len(pieces) == 0:
			return CONTRADICTION
		for var in X:
			if var[0] == "P":
				csp.update_domain(var, copy.copy(pieces))
			else:
				arbitrary = 100000
				csp.update_domain(var, {"min": 1, "max": arbitrary})

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
		if not "L6" in X:
			return
		L6 = csp.get_domain("L6")
		new_d = copy.copy(L6)
		new_d["min"] = spec["hmarg"] * 2 + spec["holed"] * 1
		if new_d["min"] > L6["max"]:
			return CONTRADICTION
		csp.update_domain("L6", new_d)
				
	def __first_node_diameter(csp, spec):
		'''Node 1 cannot have a diameter below a certain value (e.g. 18mm).'''
		P1 = csp.get_domain("P1")
		max_diam = spec["topd"]["max"]
		min_diam = spec["topd"]["min"]
		legal_pieces = set([])
		for piece in P1:
			if piece[4] >= min_diam and piece[4] <= max_diam:
				legal_pieces.add(piece)
		if len(legal_pieces) == 0:
			return CONTRADICTION
		csp.update_domain("P1", legal_pieces)

	def __fourth_node_two_holes(csp, spec):
		'''Implements a length constraint on L4.
			
			The goal is to ensure holes 1 and 2 fall on node 4.

			The following relation helps achieve this goal:
			
			L4 >= 2*hole_margin + 2*hole_diameter + h2 - h1 - hole_diameter
			
			which defines a minimum length for L4.'''
		X = csp.get_variables()
		if not "L4" in X:
			return
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
		X = csp.get_variables()
		if not "L5" in X:
			return
		h3_h5_dist = spec["h5"] - spec["h3"]
		new_min = 2*spec["hmarg"] + spec["holed"] + h3_h5_dist
		L5 = csp.get_domain("L5")
		if new_min > L5["max"]:
			return CONTRADICTION
		csp.update_domain("L5", {"min": new_min, "max": L5["max"]})