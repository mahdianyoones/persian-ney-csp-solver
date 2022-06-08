from ney_spec import desired_ney
from csp import EMPTY_VALUE, assigned_vars

# A value is a tuple of this format: (NO, L, TH, R, D).
# All functions return (success/failure indicator, inconsistent variables)
# True = success, False = failure
# inconsistent variables is a set of variables in conflict	

def no(value):
	return value[0]
def l(value):
	return value[1]
def th(value):
	return value[2]
def r(value):
	return value[3]
def d(value):
	return value[4]
	
def N1_length(asmnt):
	'''Takes assignments, returns length(node 1) + length(mouthpiece).'''
	return l(asmnt["A"]) + desired_ney["mp_lenght"]

def N2_length(asmnt):
	'''Takes assignments, returns length(B1+B2+B3+B4).'''
	length = l(asmnt["B1"])
	if asmnt["B2"] != EMPTY_VALUE:
		length += l(asmnt["B2"])
	if asmnt["B3"] != EMPTY_VALUE:
		length += l(asmnt["B3"])
	if asmnt["B4"] != EMPTY_VALUE:
		length += l(asmnt["B4"])
	return length
	
def N3_length(asmnt):
	'''Takes assignments, returns length(C1+C2+C3+C4).'''
	length = l(asmnt["C1"])
	if asmnt["C2"] != EMPTY_VALUE:
		length += l(asmnt["C2"])
	if asmnt["C3"] != EMPTY_VALUE:
		length += l(asmnt["C3"])
	if asmnt["C4"] != EMPTY_VALUE:
		length += l(asmnt["C4"])
	return length

def N4_length(asmnt):
	'''Takes assignments, returns length(D1+D2+D3).'''
	length = l(asmnt["D1"])
	if asmnt["D2"] != EMPTY_VALUE:
		length += l(asmnt["D2"])
	if asmnt["D3"] != EMPTY_VALUE:
		length += l(asmnt["D3"])
	return length

def N5_length(asmnt):
	'''Takes assignments, returns length(E1+E2).'''
	length = l(asmnt["E1"])
	if asmnt["E2"] != EMPTY_VALUE:
		length += l(asmnt["E2"])
	return length
	
def N6_length(asmnt):
	'''Takes assignments, returns length(F1+F2).'''
	length = l(asmnt["F1"])
	if asmnt["F2"] != EMPTY_VALUE:
		length += l(asmnt["F2"])
	return length
	
# Unary constraints

def top_diameter(asmnt):
	'''Takes assignments and checks the diameter of node 1.'''
	if d(asmnt["A"]) == desired_ney["n1_diameter"]:
		return (True, None)
	return (False, {"A"})
	
def top_llower(asmnt):
	'''Takes assignments and checks the length lower bound of node 1.'''
	if N1_length(asmnt) < desired_ney["n1_llower"]:
		return (False, {"A"})
	return (True, None)

def top_lupper(asmnt):
	'''Takes assignments and checks the length upper bound of node 1.'''
	if N1_length(asmnt) > desired_ney["n1_lupper"]:
		return (False, {"A"})
	return (True, None)


# Binary constraints

def n5_llower(asmnt):
	'''Takes assignments and checks the length lower bound of node 5.
	
	Returns True if required variables are not all in the assignments, since
	length might change in the future.
	'''
	if not set(["E1", "E2"]).issubset(set(asmnt.keys())):
		return (True, None)
	if N5_length(asmnt) < desired_ney["n5_llower"]:
		return (False, {"E1", "E2"})
	return (True, None)

def n6_llower(asmnt):
	'''Takes assignments and checks the length lower bound of node 6.
	
	Returns True if required variables are not all in the assignments, since
	length might change in the future.
	'''
	if not set(["F1", "F2"]).issubset(set(asmnt.keys())):
		return (True, None)
	if N6_length(asmnt) < desired_ney["n6_llower"]:
		return (False, {"F1", "F2"})
	return (True, None)

def n6_chunks_sim(asmnt):
	'''Takes assignments and checks the similarity between the chunks of node 6.
	
	Roundness, thickness, and dimater of both chunks must be the same.
	'''
	if not set(["F1", "F2"]).issubset(set(asmnt.keys())):
		return (True, None)
	if d(asmnt["F1"]) == d(asmnt["F2"]):
		if r(asmnt["F1"]) == r(asmnt["F2"]):
			if th(asmnt["F1"]) == th(asmnt["F2"]):
				return (True, None)
	return (False, {"F1", "F2"})

def n5_chunks_sim(E1, E2):
	'''Takes assignments and checks the similarity between the chunks of node 5.
	
	Roundness, thickness, and dimater of both chunks must be the same.
	'''
	if not set(["E1", "E2"]).issubset(set(asmnt.keys())):
		return (True, None)
	if d(asmnt["E1"]) == d(asmnt["E2"]):
		if r(asmnt["E1"]) == r(asmnt["E2"]):
			if th(asmnt["E1"]) == th(asmnt["E2"]):
				return (True, None)
	return (False, {"E1", "E2"})

# Higher order constraints

def n1_half_n2(asmnt):
	'''Takes assignments and checks whether node 2 is double as long as node 1.
	
	Returns True if required variables are not all in the assignments, since
	length of each node might change in the future.
	'''
	if not set(["A", "B1", "B2", "B3", "B4"]).issubset(set(asmnt.keys())):
		return (True, None)
	if 2 * N1_length(asmnt) == N2_length(asmnt):
		return (True, None)
	return (False, {"A", "B1", "B2", "B3", "B4"})

def n3n4_llower(asmnt):
	'''Takes assignments and checks the length lower bound of node 3 and 4.
	
	Returns True if required variables are not all in the assignments, since
	length of nodes might change in the future.
	
	This constraint could have been two separate constraints.
	'''
	if set(["C1", "C2", "C3", "C4"]).issubset(set(asmnt.keys())):
		if n3_length(asmnt) < desired_ney["n3_llower"]:
			return (False, {"C1", "C2", "C3", "C4"})
	if set(["D1", "D2", "D3"]).issubset(set(asmnt.keys())):
	 	if n4_length(asmnt) < desired_ney["n4_llower"]:
	 		return (False, {"D1", "D2", "D3"})
	return (True, None)

def h7_on_n4(asmnt):
	'''Takes assignments and checks whether hole 7 falls on node 4 or not.
	
	Returns True if required variables are not all in the assignments, since
	length of the nodes might change in the future.
	'''
	req_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4"]
	if not set(req_vars).issubset(set(asmnt.keys())):
		return (True, None)
	chunks_length = N1_length(asmnt) + N2_length(asmnt) + N3_length(asmnt)
	if chunks_length + desired_ney["min_hj_dist"] < desired_ney["h7"]:
		return (True, None)
	return (False, set(req_vars))

def chunks_similar(asmnt):
	'''Takes assignments and checks the similarity between chunks of nodes 2, 3 & 4.
	
	Roundness, thickness, and dimater of all chunks must be the same.
	This constraint could have been three separate constraints.
	'''
	_vars = {
		"B1": ["B2", "B3", "B4"],
		"C1": ["C2", "C3", "c4"],
		"D1": ["D2", "D3"]
	}
	for p, q in _vars.items():	
		if p not in asmnt:
			continue
		for var in q:
			if var not in asmnt or var == EMPTY_VALUE:
				continue
			if th(asmnt[p]) != th(asmnt[var]) or \
			   	d(asmnt[p]) != d(asmnt[var]) or \
			   	r(asmnt[p]) != r(asmnt[var]):
			   		return (False, {p, var})
	return (True, None)

# TODO: we can define upper bound for all nodes as well

def h6_end_n4(asmnt):
	'''Takes assignments and checks if hole 6 falls on node 4 or not.
	
	Returns True if required variables are not all in the assignments, since
	length of the nodes might change in the future.
	'''
	req_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "D1", "D2", "D3"]
	if not set(req_vars).issubset(set(asmnt.keys())):
		return (True, None)
	chunks_length = N1_length(asmnt["A"]) + N2_length(asmnt)
	chunks_length += N3_length(asmnt) + N4_length(asmnt)
	if chunks_length == desired_ney["h6"] + desired_ney["min_hj_dist"]:
		return (True, None)
	return (False, set(req_vars))

def h5_on_n5(asmnt):
	'''Takes assignments and checks if hole 5 falls on node 5 or not.
	
	Returns True if required variables are not all in the assignments, since
	length of the nodes might change in the future.
	'''
	req_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "D1", "D2", "D3"]
	if not set(req_vars).issubset(set(asmnt.keys())):
		return (True, None)
	chunks_length = N1_length(asmnt) + N2_length(asmnt)
	chunks_length += N3_length(asmnt) + N4_length(asmnt)
	if chunks_length + desired_ney["min_hj_dist"] <= desired_ney["h5"]:
		return (True, None)
	return (False, set(req_vars))

def h4_on_n5(asmnt):
	'''Takes assignments and checks if hole 4 falls on node 5 or not.
	
	Returns True if required variables are not all in the assignments, since
	length of the nodes might change in the future.
	'''
	req_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "D1", "D2", "D3"]
	if not set(req_vars).issubset(set(asmnt.keys())):
		return (True, None)
	chunks_length = N1_length(asmnt["A"]) + N2_length(asmnt)
	chunks_length += N3_length(asmnt) + N4_length(asmnt)
	# hole 5 junction distance + hole 5 diameter + hole 5 hole 6 distance
	extra_space = desired_ney["min_hj_dist"] + desired_ney["h_diameter"]
	extra_space += desired_ney["min_hh_dist"]
	if chunks_length + extra_space <= desired_ney["h4"]:
		return (True, None)
	return (False, set(req_vars))

# Hole 3 falls at the end of node 5
def h3_endof_n5(asmnt):
	'''Takes assignments and checks if hole 3 falls on the end of node 5.
	
	Returns True if required variables are not all in the assignments, since
	length of the nodes might change in the future.
	'''
	req_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", \
		"D1", "D2", "D3", "E1", "E2"]
	if not set(req_vars).issubset(set(asmnt.keys())):
		return (True, None)
	chunks_length = N1_length(asmnt) + N2_length(asmnt) + N3_length(asmnt)
	chunks_length += N4_length(asmnt) + N5_length(asmnt)
	if chunks_length + desired_ney["min_hj_dist"] == desired_ney["h3"]:
		return (True, None)
	return (False, set(req_vars))

def h2_startof_n6(asmnt):
	'''Takes assignments and checks if hole 2 falls on the beginning of node 6.
	
	Returns True if required variables are not all in the assignments, since
	length of the nodes might change in the future.
	'''
	req_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", \
		"D1", "D2", "D3", "E1", "E2"]
	if not set(req_vars).issubset(set(asmnt.keys())):
		return (True, None)
	chunks_length = N1_length(asmnt) + N2_length(asmnt) + N3_length(asmnt)
	chunks_length += N4_length(asmnt) + N5_length(asmnt)
	if chunks_length + desired_ney["min_hj_dist"] <= desired_ney["h2"]:
		return (True, None)
	return (False, set(req_vars))

def len_decrement(asmnt):
	'''Takes assignments and checks if nodes decrease in length.
	
	Returns True if required variables are not all in the assignments, since
	length of the nodes might change in the future.
	'''
	# Asserting n2 > n3	
	req_vars = ["B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4"]
	if set(req_vars).issubset(set(asmnt.keys())):
		if N2_length(asmnt) <= N3_length(asmnt):
			return (False, set(req_vars))
	# Asserting n3 > n4
	req_vars = ["C1", "C2", "C3", "C4", "D1", "D2", "D3"]
	if set(req_vars).issubset(set(asmnt.keys())):
		if N3_length(asmnt) <= N4_length(asmnt):
			return (False, set(req_vars))
	# Asserting n4 > n5		
	req_vars = ["D1", "D2", "D3", "E1", "E2"]
	if set(req_vars).issubset(set(asmnt.keys())):
		if N4_length(asmnt) <= N5_length(asmnt):
			return (False, set(req_vars))
	# Asserting n5 > n6
	req_vars = ["E1", "E2", "F1", "F2"]
	if set(req_vars).issubset(set(asmnt.keys())):
		if N5_length(asmnt) <= N6_length(asmnt):
			return (False, set(req_vars))
	return (True, None)

def ddiff_similar(asmnt):
	'''Takes assignments and checks if nodes diameter decrease consistency.
	
	Asserts diam("A") - diam("B1") == diam("B1") - diam("C1") == ... til F1 - G
	'''
	_vars = ["A", "B1", "C1", "D1", "E1", "F1", "G"]
	asmnt_keys = set(asmnt.keys())
	if len(asmnt_keys) < 3:
		return (True, None)
	for index, var in enumerate(_vars):
		if index + 1 == len(_vars):
			break
		if set([var, _vars[index + 1]]).issubset(asmnt_keys):
			left_diam = d(asmnt[var])
			right_diam = d(asmnt[_vars[index + 1]])
			if index == 0:
				diff = left_diam - right_diam
				continue
			if diff != left_diam - right_diam:
				return (False, {_vars[index - 1], var, _vars[index + 1]})
	return (True, None)

def diam_diff(asmnt):
	'''Takes assignments and checks the bounds of diameter differeces.
	
	Adjacent nodes must differ in diameter within a given range.
	'''
	lower = desired_ney["diam_diff_lower"]
	upper = desired_ney["diam_diff_upper"]
	_vars = ["A", "B1", "C1", "D1", "E1", "F1", "G"]
	asmnt_keys = set(asmnt.keys())
	if len(asmnt_keys) < 2:
		return (True, None)
	for index, var in enumerate(_vars):
		if index + 1 == len(_vars):
			break
		if set([var, _vars[index + 1]]).issubset(set(asmnt_keys)):
			left_diam = d(asmnt[var])
			right_diam = d(asmnt[_vars[index + 1]])
			diff = left_diam - right_diam
			if diff < lower or diff > upper:
				return (False, {var, _vars[index + 1]})
	return (True, None)

def nodes_similar(asmnt):
	'''Takes assignments and checks whether all nodes are similar or not.'''
	asmnt_vars = asmnt.keys()
	present_vars = set(asmnt_vars).intersection(["A", "B1", "C1", 
		"D1", "E1", "F1", "G"])
	# At least two of the above vars should exist
	if len(present_vars) < 2:
		return (True, None)
	last_THR = (0, 0) # (thickness, roundness)
	last_var = None
	for var in present_vars:
		if last_THR == (0, 0):
			last_THR = (th(asmnt[var]), r(asmnt[var]))
			last_var = var
		elif last_THR != (th(asmnt[var]), r(asmnt[var])):
			return (False, {last_var, var})
	return (True, None)

def h1_length(asmnt):
	'''Takes assignments and checks the length of the whole Ney.
	
	Returns True if required variables are not all in the assignments, since
	length of the nodes might change in the future.
	'''
	req_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3",
			"D1", "D2", "D3", "E1", "E2", "F1", "F2", "E1", "E2"]
	if not set(req_vars).issubset(set(asmnt.keys())):
		return (True, None)
	chunks_length = N1_length(asmnt) + N2_length(asmnt)
	chunks_length += N3_length(asmnt) + N4_length(asmnt)
	chunks_length += N5_length(asmnt) + N6_length(asmnt)
	chunks_length += l(asmnt["G"])
	if chunks_length == desired_ney["h1"]:
		return (True, None)
	return (False, set(req_vars))

def no_overlap(asmnt):
	'''Takes assignments and checks whether chunks overlap or not.
	
	Overlap means two different chunks are to be 
	cut from the same piece and share some area with eachother.
	'''
	if len(asmnt) < 2:
		return (True, None)
	piece_number = 0
	last_var = 0
	for var, value in asmnt.items():
		if piece_number == no(value):
			return (False, {last_var, var})
		piece_number = no(value)
		last_var = var
	return (True, None)
