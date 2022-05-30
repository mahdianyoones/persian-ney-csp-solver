from ney_spec import desired_ney

EMPTY_VALUE = {
	"NO": 	0, 
	"L": 	0,
	"TH": 	0,
	"R":		0,
	"D":		0 
}

def A_length(asmnt):
	return asmnt["A"]["L"] + desired_ney["mp_lenght"]

def N2_length(asmnt):
	length = asmnt["B1"]["L"]
	if asmnt["B2"] != EMPTY_VALUE:
		length += asmnt["B2"]["L"]
	if asmnt["B3"] != EMPTY_VALUE:
		length += asmnt["B3"]["L"]
	if asmnt["B4"] != EMPTY_VALUE:
		length += asmnt["B4"]["L"]
	return length
	
def N3_length(asmnt):
	length = asmnt["C1"]["L"]
	if asmnt["C2"] != EMPTY_VALUE:
		length += asmnt["C2"]["L"]
	if asmnt["C3"] != EMPTY_VALUE:
		length += asmnt["C3"]["L"]
	if asmnt["C4"] != EMPTY_VALUE:
		length += asmnt["C4"]["L"]
	return length

def N4_length(asmnt):
	length = asmnt["D1"]["L"]
	if asmnt["D2"] != EMPTY_VALUE:
		length += asmnt["D2"]["L"]
	if asmnt["D3"] != EMPTY_VALUE:
		length += asmnt["D3"]["L"]
	return length

def N5_length(E1, E2):
	length = asmnt["E1"]["L"]
	if asmnt["E2"] != EMPTY_VALUE:
		length += asmnt["E2"]["L"]
	if asmnt["E3"] != EMPTY_VALUE:
		length += asmnt["E3"]["L"]
	return length
	
def N6_length(F1, F2):
	length = asmnt["F1"]["L"]
	if asmnt["F2"] != EMPTY_VALUE:
		length += asmnt["F2"]["L"]
	if asmnt["F3"] != EMPTY_VALUE:
		length += asmnt["F3"]["L"]
	return length
	
# Unary constraints

def top_diameter(asmnt):
	if asmnt["A"]["D"] == desired_ney["n1_diameter"]:
		return True
	return False
	
def top_llower(value):
	if A_length(value) < desired_ney["n1_llower"]:
		return False
	return True

def top_lupper(value):
	if A_length(value) > desired_ney["n1_lupper"]:
		return False
	return True


# Binary constraints

def n5_llower(asmnt):
	if "E1" not in asmnt or "E2" not in asmnt:
		return True
	n5_length = asmnt["E1"]["L"] + asmnt["E2"]["L"]
	if n5_length < desired_ney["n5_llower"]:
		return False
	return True

def n6_llower(asmnt):
	if "F1" not in asmnt or "F2" not in asmnt:
		return True
	n5_length = asmnt["F1"]["L"] + asmnt["F2"]["L"]
	if n5_length < desired_ney["n6_llower"]:
		return False
	return True

def n6_chunks_sim(asmnt):
	if "F1" not in asmnt or "F2" not in asmnt:
		return True	
	if asmnt["F1"]["D"] != asmnt["F2"]["D"] or \
		asmnt["F1"]["R"] != asmnt["F2"]["R"] or \
		asmnt["F1"]["TH"] != asmnt["F2"]["TH"]:
			return False
	return True

def n5_chunks_sim(E1, E2):
	if "E1" not in asmnt or "E2" not in asmnt:
		return True	
	if asmnt["E1"]["D"] != asmnt["E2"]["D"] or \
		asmnt["E1"]["R"] != asmnt["E2"]["R"] or \
		asmnt["E1"]["TH"] != asmnt["E2"]["TH"]:
			return False
	return True

# Higher order constraints

def n1_half_n2(asmnt):
	
	if "A" not in asmnt or \
		"B1" not in asmnt or \
		"B2" not in asmnt or \
		"B3" not in asmnt or \
		"B4" not in asmnt:
		return True	
	n2_length = N2_length(asmnt["B1"], asmnt["B2"], \
		asmnt["B3"], asmnt["B4"])
	if A_length(asmnt["A"]) == n2_length * 2:
		return True
	return False

def n3n4_llower(asmnt):
	if "C1" in asmnt and "C2" in asmnt and \
			"C3" in asmnt and "C4" in asmnt:
			n3_length = N3_length(asmnt["C1"], asmnt["C2"], \
						asmnt["C3"], asmnt["C4"])
			if n3_length < desired_ney["n3_llower"]:
				return False
	if "D1" in asmnt and "D2" in asmnt and "D3" in asmnt:
	 	n4_length = N4_length(asmnt["D1"], asmnt["D2"], asmnt["D3"])
	 	if n4_length < desired_ney["n4_llower"]:
	 		return False
	return True

def h7_on_n4(asmnt):
	_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4"]
	for var in _vars:
		if not var in asmnt:
			return True
	chunks_length = A_length(asmnt) + N2_length(asmnt) + N3_length(asmnt)
	if chunks_length + desired_ney["min_hj_dist"] < desired_ney["h7"]:
		return True
	return False

def chunks_similar(asmnt):
	#n2
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
			if asmnt[p]["TH"] != asmnt[q]["TH"] or \
			   	asmnt[p]["R"] != asmnt[q]["R"] or \
			   	asmnt[p]["D"] != asmnt[q]["D"]:
			   		return False	
	return True

# TODO: we can define upper bound for all nodes

def h6_end_n4(asmnt):
	_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "D1", "D2", "D3"]
	for var in _vars:
		if not var in asmnt:
			return True
	chunks_length = A_length(asmnt["A"]) + N2_length(asmnt) + \
				N3_length(asmnt) + N4_length(asmnt)
	if chunks_length == desired_ney["h6"] + desired_ney["min_hj_dist"]:
		return True
	return False

def h5_on_n5(asmnt):
	_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "D1", "D2", "D3"]
	for var in _vars:
		if not var in asmnt:
			return True
	chunks_length = A_length(asmnt["A"]) + N2_length(asmnt) + \
			N3_length(asmnt) + N4_length(asmnt)
	if chunks_length + desired_ney["min_hj_dist"] <= desired_ney["h5"]:
		return True
	return False

def h4_on_n5(asmnt):
	_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "D1", "D2", "D3"]
	for var in _vars:
		if not var in asmnt:
			return True
	chunks_length = A_length(asmnt["A"]) + N2_length(asmnt) + \
			N3_length(asmnt) + N4_length(asmnt)
	# hole 5 junction distance + hole 5 diameter + hole 5 hole 6 distance
	if chunks_length + desired_ney["min_hj_dist"] + desired_ney["h_diameter"] \
	 	+ desired_ney["min_hh_dist"] <= desired_ney["h4"]:
		return True
	return False

# Hole 3 falls at the end of node 5
def h3_endof_n5(asmnt):
	_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", \
		"D1", "D2", "D3", "E1", "E2"]
	for var in _vars:
		if not var in asmnt:
			return True
	chunks_length = A_length(asmnt["A"]) + N2_length(asmnt) + \
			N3_length(asmnt) + N4_length(asmnt) + N5_length(asmnt)
	if chunks_length + desired_ney["min_hj_dist"] == desired_ney["h3"]:
		return True
	return False

def h2_startof_n6(asmnt):
	_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", \
		"D1", "D2", "D3", "E1", "E2"]
	for var in _vars:
		if not var in asmnt:
			return True
	chunks_length = A_length(asmnt["A"]) + N2_length(asmnt) + \
			N3_length(asmnt) + N4_length(asmnt) + N5_length(asmnt)
	if chunks_length + desired_ney["min_hj_dist"] <= desired_ney["h2"]:
		return True
	return False

def len_decrement(asmnt):
	# asserting n2 > n3
	if "B1" in asmnt and "B2" in asmnt and \
		"B3" in asmnt and "B4" in asmnt and \
		"C1" in asmnt and "C2" in asmnt and \
		"C3" in asmnt and "C4" in asmnt:
			n2_length = N2_length(asmnt["B1"], asmnt["B2"], \
						asmnt["B3"], asmnt["B4"])
			n3_length = N3_length(asmnt["C1"], asmnt["C2"], \
						asmnt["C3"], asmnt["C4"])				
			if n2_length <= n3_length:
				return False
	# asserting n3 > n4
	if "C1" in asmnt and "C2" in asmnt and \
		"C3" in asmnt and "C4" in asmnt and \
		"D1" in asmnt and "D2" in asmnt and \
		"D3" in asmnt:
			n3_length = N3_length(asmnt["C1"], asmnt["C2"], \
						asmnt["C3"], asmnt["C4"])				
			n4_length = N4_length(asmnt["D1"], asmnt["D2"], \
				asmnt["D3"])
			if n3_length <= n4_length:
				return False
	# asserting n4 > n5		
	if "D1" in asmnt and "D2" in asmnt and \
		"D3" in asmnt and "E1" in asmnt and \
		"E2" in asmnt:
			n4_length = N4_length(asmnt["D1"], asmnt["D2"], \
				asmnt["D3"])
			n5_length = N5_length(asmnt["E1"], asmnt["E2"])
			if n4_length <= n5_length:
				return False
	# asserting n5 > n6
	if "E1" in asmnt and "E2" in asmnt and \
		"F1" in asmnt and "F2" in asmnt:
			n5_length = N5_length(asmnt["E1"], asmnt["E2"])
			n6_length = N6_length(asmnt["F1"], asmnt["F2"])
			if n5_length <= n6_length:
				return False
	return True

def ddiff_similar(asmnt):
	A_B_diff = B_C_diff = C_D_diff = D_E_diff = E_F_diff = F_G_diff = 0
	if "A" in asmnt and "B1" in asmnt:
		A_B_diff = asmnt["A"]["D"] - asmnt["B1"]["D"]
	if "B1" in asmnt and "C1" in asmnt:
		B_C_diff = asmnt["B1"]["D"] - asmnt["C1"]["D"]
	if "C1" in asmnt and "D1" in asmnt:
		C_D_diff = asmnt["C1"]["D"] - asmnt["D1"]["D"]
	if "D1" in asmnt and "E1" in asmnt:
		D_E_diff = asmnt["D1"]["D"] - asmnt["E1"]["D"]
	if "E1" in asmnt and "F1" in asmnt:
		E_F_diff = asmnt["E1"]["D"] - asmnt["F1"]["D"]
	if "F1" in asmnt and "g" in asmnt:
		F_G_diff = asmnt["F1"]["D"] - asmnt["G"]["D"]
	if A_B_diff == B_C_diff == C_D_diff == D_E_diff == E_F_diff == F_G_diff:
		return True
	return False

def diam_diff(asmnt):
	A_B_diff = B_C_diff = C_D_diff = D_E_diff = \
	E_F_diff = F_G_diff = (desired_ney["diam_diff_upper"] + \
		desired_ney["diam_diff_lower"]) / 2
	if "A" in asmnt and "B1" in asmnt:
		A_B_diff = asmnt["A"]["D"] - asmnt["B1"]["D"]
	if "B1" in asmnt and "C1" in asmnt:
		B_C_diff = asmnt["B1"]["D"] - asmnt["C1"]["D"]
	if "C1" in asmnt and "D1" in asmnt:
		C_D_diff = asmnt["C1"]["D"] - asmnt["D1"]["D"]
	if "D1" in asmnt and "E1" in asmnt:
		D_E_diff = asmnt["D1"]["D"] - asmnt["E1"]["D"]
	if "E1" in asmnt and "F1" in asmnt:
		E_F_diff = asmnt["E1"]["D"] - asmnt["F1"]["D"]
	if "F1" in asmnt and "G" in asmnt:
		F_G_diff = asmnt["F1"]["D"] - asmnt["G"]["D"]
	ddiflower = desired_ney["diam_diff_lower"]
	ddifupper = desired_ney["diam_diff_upper"]
	if ddiflower > A_B_diff or A_B_diff > ddifupper or \
		ddiflower > B_C_diff or B_C_diff > ddifupper or \
		ddiflower > C_D_diff or C_D_diff > ddifupper or \
		ddiflower > D_E_diff or D_E_diff > ddifupper or \
		ddiflower > E_F_diff or E_F_diff > ddifupper or \
		ddiflower > F_G_diff or F_G_diff > ddifupper:
			return False		
	return True

def nodes_similar(asmnt):
	THRD = (0, 0, 0)
	for var, value in asmnt.items():
		if THRD == (0, 0, 0):
			THRD = (value["TH"], value["R"], value["D"])
			continue
		if value != EMPTY_VALUE and THRD != (value["TH"], value["R"], value["D"]):
			return False
		THRD = (value["TH"], value["R"], value["D"])
	return True

def h1_length(asmnt):
	_vars = ["A", "B1", "B2", "B3", "B4", "C1", "C2", "C3", \
		"D1", "D2", "D3", "E1", "E2", "F1", "F2", "E1", "E2"]
	for var in _vars:
		if not var in asmnt:
			return True
	chunks_length = A_length(asmnt["A"]) + N2_length(asmnt) + \
			N3_length(asmnt) + N4_length(asmnt) + \
			N5_length(asmnt) + N6_length(asmnt) + asmnt["G"]["L"]
	return True if chunks_length == desired_ney["h1"] else False

def no_overlap(asmnt):
	if len(asmnt) < 2:
		return True
	piece_number = 0
	for var, value in asmnt.items():
		if piece_number == value["NO"]:
			return False
		piece_number = value["NO"]
	return True
