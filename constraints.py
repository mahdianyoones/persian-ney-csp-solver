from ney_spec import desired_ney

EMPTY_VALUE = {
	"NO": 	0, 
	"L": 	0,
	"TH": 	0,
	"R":		0,
	"D":		0 
}

def N1_length(asmnt):
	'''Takes assignments, returns length(node 1) + length(mouthpiece).'''
	return asmnt["A"]["L"] + desired_ney["mp_lenght"]

def N2_length(asmnt):
	'''Takes assignments, returns length(B1+B2+B3+B4).'''
	length = asmnt["B1"]["L"]
	if asmnt["B2"] != EMPTY_VALUE:
		length += asmnt["B2"]["L"]
	if asmnt["B3"] != EMPTY_VALUE:
		length += asmnt["B3"]["L"]
	if asmnt["B4"] != EMPTY_VALUE:
		length += asmnt["B4"]["L"]
	return length
	
def N3_length(asmnt):
	'''Takes assignments, returns length(C1+C2+C3+C4).'''
	length = asmnt["C1"]["L"]
	if asmnt["C2"] != EMPTY_VALUE:
		length += asmnt["C2"]["L"]
	if asmnt["C3"] != EMPTY_VALUE:
		length += asmnt["C3"]["L"]
	if asmnt["C4"] != EMPTY_VALUE:
		length += asmnt["C4"]["L"]
	return length

def N4_length(asmnt):
	'''Takes assignments, returns length(D1+D2+D3).'''
	length = asmnt["D1"]["L"]
	if asmnt["D2"] != EMPTY_VALUE:
		length += asmnt["D2"]["L"]
	if asmnt["D3"] != EMPTY_VALUE:
		length += asmnt["D3"]["L"]
	return length

def N5_length(asmnt):
	'''Takes assignments, returns length(E1+E2).'''
	length = asmnt["E1"]["L"]
	if asmnt["E2"] != EMPTY_VALUE:
		length += asmnt["E2"]["L"]
	return length
	
def N6_length(asmnt):
	'''Takes assignments, returns length(F1+F2).'''
	length = asmnt["F1"]["L"]
	if asmnt["F2"] != EMPTY_VALUE:
		length += asmnt["F2"]["L"]
	return length
	
# Unary constraints

def top_diameter(asmnt):
	'''Takes assignments and checks the diameter of node 1.'''
	if asmnt["A"]["D"] == desired_ney["n1_diameter"]:
		return True
	return False
	
def top_llower(asmnt):
	'''Takes assignments and checks the length lower bound of node 1.'''
	if N1_length(asmnt) < desired_ney["n1_llower"]:
		return False
	return True

def top_lupper(asmnt):
	'''Takes assignments and checks the length upper bound of node 1.'''
	if N1_length(asmnt) > desired_ney["n1_lupper"]:
		return False
	return True


# Binary constraints

def n5_llower(asmnt):
	'''Takes assignments and checks the length lower bound of node 5.
	
	Returns True if required variables are not all in the assignments, since
	length might change in the future.
	'''
	if not set(["E1", "E2"]).issubset(asmnt.keys()):
		return True
	if N5_length(asmnt) < desired_ney["n5_llower"]:
		return False
	return True


def n6_llower(asmnt):
	'''Takes assignments and checks the length lower bound of node 6.
	
	Returns True if required variables are not all in the assignments, since
	length might change in the future.
	'''
	if not set(["F1", "F2"]).issubset(asmnt.keys()):
		return True
	if N6_length(asmnt) < desired_ney["n6_llower"]:
		return False
	return True

def n6_chunks_sim(asmnt):
	'''Takes assignments and checks the similarity between the chunks of node 6.
	
	Roundness, thickness, and dimater of both chunks must be the same.
	'''
	if not set(["F1", "F2"]).issubset(asmnt.keys()):
		return True
	if asmnt["F1"]["D"] == asmnt["F2"]["D"]:
		if asmnt["F1"]["R"] == asmnt["F2"]["R"]:
			if asmnt["F1"]["TH"] == asmnt["F2"]["TH"]:
				return False
	return True

def n5_chunks_sim(E1, E2):
	'''Takes assignments and checks the similarity between the chunks of node 5.
	
	Roundness, thickness, and dimater of both chunks must be the same.
	'''
	if not set(["E1", "E2"]).issubset(asmnt.keys()):
		return True
	if asmnt["E1"]["D"] == asmnt["E2"]["D"]:
		if asmnt["E1"]["R"] == asmnt["E2"]["R"]:
			if asmnt["E1"]["TH"] == asmnt["E2"]["TH"]:
				return True
	return False

# Higher order constraints

def n1_half_n2(asmnt):
	'''Takes assignments and checks whether node 2 is double as long as node 1.
	
	Returns True if required variables are not all in the assignments, since
	length of each node might change in the future.
	'''
	if not set(["A", "B1", "B2", "B3", "B4"]).issubset(asmnt.keys()):
		return True
	if 2 * N1_length(asmnt) == N2_length(asmnt):
		return True
	return False

def n3n4_llower(asmnt):
	'''Takes assignments and checks the length lower bound of node 3 and 4.
	
	Returns True if required variables are not all in the assignments, since
	length of nodes might change in the future.
	
	This constraint could have been two separate constraints.
	'''
	if set(["C1", "C2", "C3", "C4"]).issubset(asmnt.keys):
		if n3_length(asmnt) < desired_ney["n3_llower"]:
			return False
	if set(["D1", "D2", "D3"]).issubset(asmnt.keys):
	 	if n4_length(asmnt) < desired_ney["n4_llower"]:
	 		return False
	return True

def h7_on_n4(asmnt):
	'''Takes assignments and checks whether hole 7 falls on node 4 or not.
	
	Returns True if required variables are not all in the assignments, since
	length of the nodes might change in the future.
	'''
	required_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4"]
	if not set(required_vars).issubset(asmnt.keys()):
		return True
	chunks_length = N1_length(asmnt) + N2_length(asmnt) + N3_length(asmnt)
	if chunks_length + desired_ney["min_hj_dist"] < desired_ney["h7"]:
		return True
	return False

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
			if asmnt[p]["TH"] != asmnt[var]["TH"] or \
			   	asmnt[p]["R"] != asmnt[var]["R"] or \
			   	asmnt[p]["D"] != asmnt[var]["D"]:
			   		return False
	return True

# TODO: we can define upper bound for all nodes as well

def h6_end_n4(asmnt):
	'''Takes assignments and checks if hole 6 falls on node 4 or not.
	
	Returns True if required variables are not all in the assignments, since
	length of the nodes might change in the future.
	'''
	req_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "D1", "D2", "D3"]
	if not set(req_vars).issubset(asmnt.keys()):
		return True
	chunks_length = N1_length(asmnt["A"]) + N2_length(asmnt)
	chunks_length += N3_length(asmnt) + N4_length(asmnt)
	if chunks_length == desired_ney["h6"] + desired_ney["min_hj_dist"]:
		return True
	return False

def h5_on_n5(asmnt):
	'''Takes assignments and checks if hole 5 falls on node 5 or not.
	
	Returns True if required variables are not all in the assignments, since
	length of the nodes might change in the future.
	'''
	req_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "D1", "D2", "D3"]
	if not set(req_vars).issubset(asmnt.keys()):
		return True
	chunks_length = N1_length(asmnt) + N2_length(asmnt)
	chunks_length += N3_length(asmnt) + N4_length(asmnt)
	if chunks_length + desired_ney["min_hj_dist"] <= desired_ney["h5"]:
		return True
	return False

def h4_on_n5(asmnt):
	'''Takes assignments and checks if hole 4 falls on node 5 or not.
	
	Returns True if required variables are not all in the assignments, since
	length of the nodes might change in the future.
	'''
	req_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "D1", "D2", "D3"]
	if not set(req_vars).issubset(asmnt.keys()):
		return True
	chunks_length = N1_length(asmnt["A"]) + N2_length(asmnt)
	chunks_length += N3_length(asmnt) + N4_length(asmnt)
	# hole 5 junction distance + hole 5 diameter + hole 5 hole 6 distance
	extra_space = desired_ney["min_hj_dist"] + desired_ney["h_diameter"]
	extra_space += desired_ney["min_hh_dist"]
	if chunks_length + extra_space <= desired_ney["h4"]:
		return True
	return False

# Hole 3 falls at the end of node 5
def h3_endof_n5(asmnt):
	'''Takes assignments and checks if hole 3 falls on the end of node 5.
	
	Returns True if required variables are not all in the assignments, since
	length of the nodes might change in the future.
	'''
	required_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", \
		"D1", "D2", "D3", "E1", "E2"]
	if not set(required_vars).issubset(asmnt.keys()):
		return True
	chunks_length = N1_length(asmnt) + N2_length(asmnt) + N3_length(asmnt)
	chunks_length += N4_length(asmnt) + N5_length(asmnt)
	if chunks_length + desired_ney["min_hj_dist"] == desired_ney["h3"]:
		return True
	return False

def h2_startof_n6(asmnt):
	'''Takes assignments and checks if hole 2 falls on the beginning of node 6.
	
	Returns True if required variables are not all in the assignments, since
	length of the nodes might change in the future.
	'''
	required_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", \
		"D1", "D2", "D3", "E1", "E2"]
	if not set(required_vars).issubset(asmnt.keys()):
		return True
	chunks_length = N1_length(asmnt) + N2_length(asmnt) + N3_length(asmnt)
	chunks_length += N4_length(asmnt) + N5_length(asmnt)
	if chunks_length + desired_ney["min_hj_dist"] <= desired_ney["h2"]:
		return True
	return False

def len_decrement(asmnt):
	'''Takes assignments and checks if nodes decrease in length.
	
	Returns True if required variables are not all in the assignments, since
	length of the nodes might change in the future.
	'''
	# Asserting n2 > n3	
	req_vars = ["B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4"]
	if set(req_vars).issubset(asmnt.keys()):
		if N2_length(asmnt) <= N3_length(asmnt):
			return False
	# Asserting n3 > n4
	req_vars = ["C1", "C2", "C3", "C4", "D1", "D2", "D3"]
	if set(req_vars).issubset(asmnt.keys()):
		if N3_length(asmnt) <= N4_length(asmnt):
			return False
	# Asserting n4 > n5		
	req_vars = ["D1", "D2", "D3", "E1", "E2"]
	if set(req_vars).issubset(asmnt.keys()):
		if N4_length(asmnt) <= N5_length(asmnt):
			return False
	# Asserting n5 > n6
	req_vars = ["E1", "E2", "F1", "F2"]
	if set(req_vars).issubset(asmnt.keys()):
		if N5_length(asmnt) <= N6_length(asmnt):
			return False
	return True

def ddiff_similar(asmnt):
	'''Takes assignments and checks if nodes diameter decrease consistency.
	
	Asserts diam("A") - diam("B1") == diam("B1") - diam("C1") == ... til F1 - G
	'''
	_vars = ["A", "B1", "C1", "D1", "E1", "F1", "G"]
	asmnt_keys = asmnt.keys()
	if len(asmnt_keys) < 3:
		return True
	last_diff = 1000 # an arbitrary large number
	for index, var in enumerate(_vars):
		if index + 1 == len(_vars):
			break
		if set([_vars[index], _vars[index + 1]]).issubset(asmnt_keys):
			left_diam = asmnt[var]["D"]
			right_diam = asmnt[_vars[index + 1]]["D"]
			if last_diff == 1000:
				last_diff = left_diam - right_diam
				continue
			if last_diff != left_diam - right_diam:
				return False
	return True

def diam_diff(asmnt):
	'''Takes assignments and checks the bounds of diameter differeces.
	
	Adjacent nodes must differ in diameter within a given range.
	'''
	lower = desired_ney["diam_diff_lower"]
	upper = desired_ney["diam_diff_upper"]
	_vars = ["A", "B1", "C1", "D1", "E1", "F1", "G"]
	asmnt_keys = asmnt.keys()
	if len(asmnt_keys) < 2:
		return True
	for index, var in enumerate(_vars):
		if index + 1 == len(_vars):
			break
		if set([var, _vars[index + 1]]).issubset(set(asmnt_keys)):
			left_diam = asmnt[var]["D"]
			right_diam = asmnt[_vars[index + 1]]["D"]
			diff = left_diam - right_diam
			if diff < lower or diff > upper:
				return False
	return True

def nodes_similar(asmnt):
	'''Takes assignments and checks whether all nodes are similar or not.'''
	asmnt_keys = asmnt.keys()
	present_vars = set(asmnt_keys).intersection(["A", "B1", "C1", "D1", "E1", "F1", "G"])
	# At least two of the above vars must exist
	if len(present_vars) < 2:
		return True
	last_THR = (0, 0) # (thickness, roundness)
	for var in present_vars:
		value = asmnt[var]
		if last_THR == (0, 0):
			last_THR = (value["TH"], value["R"])
		elif last_THR != (value["TH"], value["R"]):
			return False
	return True

def h1_length(asmnt):
	'''Takes assignments and checks the length of the whole Ney.
	
	Returns True if required variables are not all in the assignments, since
	length of the nodes might change in the future.
	'''
	req_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3",
			"D1", "D2", "D3", "E1", "E2", "F1", "F2", "E1", "E2"]
	if not set(req_vars).issubset(asmnt.keys()):
		return True
	chunks_length = N1_length(asmnt) + N2_length(asmnt)
	chunks_length += N3_length(asmnt) + N4_length(asmnt)
	chunks_length += N5_length(asmnt) + N6_length(asmnt)
	chunks_length += asmnt["G"]["L"]
	return True if chunks_length == desired_ney["h1"] else False

def no_overlap(asmnt):
	'''Takes assignments and checks whether chunks overlap or not.
	
	Overlap means two different chunks are to be 
	cut from the same piece and share some area with eachother.
	'''
	if len(asmnt) < 2:
		return True
	piece_number = 0
	for var, value in asmnt.items():
		if piece_number == value["NO"]:
			return False
		piece_number = value["NO"]
	return True
