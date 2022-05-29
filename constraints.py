from ney_spec 		import desired_ney
from utils		import *

# Unary constraints

def top_diameter(value):
	if value["D"] != desired_ney["n1_diameter"]:
		return False
	return True

def top_llower(value):
	if A_length(value) < desired_ney["n1_llower"]:
		return False
	return True

def top_lupper(value):
	if A_length(value) > desired_ney["n1_lupper"]:
		return False
	return True


# Binary constraints

def n5_llower(assignments):
	if "E1" not in assignments or "E2" not in assignments:
		return True
	n5_length = assignments["E1"]["L"] + assignments["E2"]["L"]
	if n5_length < desied_ney["n5_llower"]:
		return False
	return True

def n6_llower(assignments):
	if "F1" not in assignments or "F2" not in assignments:
		return True
	n5_length = assignments["F1"]["L"] + assignments["F2"]["L"]
	if n5_length < desied_ney["n6_llower"]:
		return False
	return True

def n6_chunks_sim(assignments):
	if "F1" not in assignments or "F2" not in assignments:
		return True	
	if assignments["F1"]["D"] != assignments["F2"]["D"] or \
		assignments["F1"]["R"] != assignments["F2"["R"] or \
		assignments["F1"]["TH"] != assignments["F2"]["TH"]:
			return False
	return True

def n5_chunks_sim(E1, E2):
	if "E1" not in assignments or "E2" not in assignments:
		return True	
	if assignments["E1"]["D"] != assignments["E2"]["D"] or \
		assignments["E1"]["R"] != assignments["E2"["R"] or \
		assignments["E1"]["TH"] != assignments["E2"]["TH"]:
			return False
	return True

# Higher order constraints

def n1_half_n2(assignments):
	if "A" not in assignments or \
		"B1" not in assignments or \
		"B2" not in assignments or \
		"B3" not in assignments or \
		"B4" not in assignments:
		return True	
	n2_length = N2_length(assignments["B1"], assignments["B2"], \
		assignments["B3"], assignments["B4"])
	if A_length(assignments["A"]) == n2_length * 2:
		return True
	return False

def n3n4_llower(assignments):
	if not ("C1" in assignmnts and "C2" in assignment \
			"C3" in assignment and "C4" in assignment) and \
	 	not ("D1" in assignmnts and "D2" in assignment \
			"D3" in assignment):
			return True
	n3_length = N3_length(assignments["C1"], assignments["C2"], \
				assignments["C3"], assignments["C4"])
	n4_length = N4_length(assignments["D1"], assignments["D2"], \
				assignments["D3"])
	if n3_length < desired_ney["n3_llower"]:
		return False
	if n4_length < desired_ney["n4_llower"]:
		return False
	return True

def h7_on_n4(assignments):
	if "A" not in assignments or \
		"B1" not in assignments or \
		"B2" not in assignments or \
		"B3" not in assignments or \
		"B4" not in assignments or \
		"C1" not in assignments or \
		"C2" not in assignments or \
		"C3" not in assignments or \
		"C4" not in assignments:
		return True	

	chunks_length = A_length(assignments["A"])
	chunks_length += N2_length(assignments["B1"], assignments["B2"], \
		assignments["B3"], assignments["B4"])
	chunks_length += N3_length(assignments["C1"], assignments["C2"], \
				assignments["C3"], assignments["C4"])
	if chunks_length + desired_ney["min_hj_dist"] < desired_ney["h7"]:
		return True
	return False

def chunks_similar(assignments):
	#n2
	if "B1" in assignments and "B2" in assignments:
		if assignments["B1"]["TH"] != assignments["B2"]["TH"] or \
		   assignments["B1"]["R"] != assignments["B2"]["R"] or \
		   assignments["B1"]["D"] != assignments["B2"]["D"]:
		   	return False
	if "B2" in assignments and "B3" in assignments:
		if assignments["B2"]["TH"] != assignments["B3"]["TH"] or \
		   assignments["B2"]["R"] != assignments["B3"]["R"] or \
		   assignments["B2"]["D"] != assignments["B3"]["D"]:
		   	return False
	if "B3" in assignments and "B4" in assignments:
		if assignments["B3"]["TH"] != assignments["B4"]["TH"] or \
		   assignments["B3"]["R"] != assignments["B4"]["R"] or \
		   assignments["B3"]["D"] != assignments["B4"]["D"]:
		   	return False
	#n3
	if "C1" in assignments and "C2" in assignment:
		if assignments["C1"]["TH"] != assignments["C2"]["TH"] or \
		   assignments["C1"]["R"] != assignments["C2"]["R"] or \
		   assignments["C1"]["D"] != assignments["C2"]["D"]:
		   	return False
	if "C2" in assignments and "C3" in assignment:
		if assignments["C2"]["TH"] != assignments["C3"]["TH"] or \
		   assignments["C2"]["R"] != assignments["C3"]["R"] or \
		   assignments["C2"]["D"] != assignments["C3"]["D"]:
		   	return False
	if "C3" in assignments and "C4" in assignments:
		if assignments["C3"]["TH"] != assignments["C4"]["TH"] or \
		   assignments["C3"]["R"] != assignments["C4"]["R"] or \
		   assignments["C3"]["D"] != assignments["C4"]["D"]:
		   	return False
	#n4
	if "D1" in assignments and "D2" in assignment:
		if assignments["D1"]["TH"] != assignments["D2"]["TH"] or \
		   assignments["D1"]["R"] != assignments["D2"]["R"] or \
		   assignments["D1"]["D"] != assignments["D2"]["D"]:
		   	return False
	if "D2" in assignments and "D3" in assignment:
		if assignments["D2"]["TH"] != assignments["D3"]["TH"] or \
		   assignments["D2"]["R"] != assignments["D3"]["R"] or \
		   assignments["D2"]["D"] != assignments["D3"]["D"]:
		   	return False
		   	
	return True

# TODO: we can define upper bound for all nodes

def h6_end_n4(assignments):
	if "A" not in assignments or \
		"B1" not in assignments or \
		"B2" not in assignments or \
		"B3" not in assignments or \
		"B4" not in assignments or \
		"C1" not in assignments or \
		"C2" not in assignments or \
		"C3" not in assignments or \
		"C4" not in assignments or ]
		"D1" not in assignments or \
		"D2" not in assignments or \
		"D3" not in assignments :
		return True	

	chunks_length = A_length(assignments["A"])
	chunks_length += N2_length(assignments["B1"], assignments["B2"], \
		assignments["B3"], assignments["B4"])
	chunks_length += N3_length(assignments["C1"], assignments["C2"], \
				assignments["C3"], assignments["C4"])
	chunks_length += N4_length(assignments["D1"], assignments["D2"], \
				assignments["D3"])
	if chunks_length == desired_ney["h6"] + desired_ney["min_hj_dist"]:
		return True
	return False

def h5_on_n5(assignments):
	if "A" not in assignments or \
		"B1" not in assignments or \
		"B2" not in assignments or \
		"B3" not in assignments or \
		"B4" not in assignments or \
		"C1" not in assignments or \
		"C2" not in assignments or \
		"C3" not in assignments or \
		"C4" not in assignments or ]
		"D1" not in assignments or \
		"D2" not in assignments or \
		"D3" not in assignments :
		return True	

	chunks_length = A_length(assignments["A"])
	chunks_length += N2_length(assignments["B1"], assignments["B2"], \
		assignments["B3"], assignments["B4"])
	chunks_length += N3_length(assignments["C1"], assignments["C2"], \
				assignments["C3"], assignments["C4"])
	chunks_length += N4_length(assignments["D1"], assignments["D2"], \
				assignments["D3"])
	if chunks_length + desired_ney["min_hj_dist"] <= desired_ney["h5"]:
		return True
	return False

def h4_on_n5(assignments):
	if "A" not in assignments or \
		"B1" not in assignments or \
		"B2" not in assignments or \
		"B3" not in assignments or \
		"B4" not in assignments or \
		"C1" not in assignments or \
		"C2" not in assignments or \
		"C3" not in assignments or \
		"C4" not in assignments or ]
		"D1" not in assignments or \
		"D2" not in assignments or \
		"D3" not in assignments :
		return True	

	chunks_length = A_length(assignments["A"])
	chunks_length += N2_length(assignments["B1"], assignments["B2"], \
		assignments["B3"], assignments["B4"])
	chunks_length += N3_length(assignments["C1"], assignments["C2"], \
				assignments["C3"], assignments["C4"])
	chunks_length += N4_length(assignments["D1"], assignments["D2"], \
				assignments["D3"])
	# hole 5 junction distance + hole 5 diameter + hole 5 hole 6 distance
	if chunks_length + desired_ney["min_hj_dist"] + desired_ney["h_diameter"] \
	 	+ desired_ney["min_hh_dist"] <= desired_ney["h4"]:
		return True
	return False

# Hole 3 falls at the end of node 5
def h3_endof_n5(assignments):
	if "A" not in assignments or \
		"B1" not in assignments or \
		"B2" not in assignments or \
		"B3" not in assignments or \
		"B4" not in assignments or \
		"C1" not in assignments or \
		"C2" not in assignments or \
		"C3" not in assignments or \
		"C4" not in assignments or ]
		"D1" not in assignments or \
		"D2" not in assignments or \
		"D3" not in assignments or \
		"E1" not in assignments or \
		"E2" not in assignments:
		return True	

	chunks_length = A_length(assignments["A"])
	chunks_length += N2_length(assignments["B1"], assignments["B2"], \
		assignments["B3"], assignments["B4"])
	chunks_length += N3_length(assignments["C1"], assignments["C2"], \
				assignments["C3"], assignments["C4"])
	chunks_length += N4_length(assignments["D1"], assignments["D2"], \
				assignments["D3"])
	chunks_length += N5_length(assignments["E1"], assignments["E2"])
	if chunks_length + desired_ney["min_hj_dist"] == desired_ney["h3"]:
		return True
	return False

def h2_startof_n6(assignments):
	if "A" not in assignments or \
		"B1" not in assignments or \
		"B2" not in assignments or \
		"B3" not in assignments or \
		"B4" not in assignments or \
		"C1" not in assignments or \
		"C2" not in assignments or \
		"C3" not in assignments or \
		"C4" not in assignments or ]
		"D1" not in assignments or \
		"D2" not in assignments or \
		"D3" not in assignments or \
		"E1" not in assignments or \
		"E2" not in assignments:
		return True	

	chunks_length = A_length(assignments["A"])
	chunks_length += N2_length(assignments["B1"], assignments["B2"], \
		assignments["B3"], assignments["B4"])
	chunks_length += N3_length(assignments["C1"], assignments["C2"], \
				assignments["C3"], assignments["C4"])
	chunks_length += N4_length(assignments["D1"], assignments["D2"], \
				assignments["D3"])
	chunks_length += N5_length(assignments["E1"], assignments["E2"])
	if chunks_length + desired_ney["min_hj_dist"] <= desired_ney["h2"]:
		return True
	return False

def len_decrement(assignments):
	# asserting n2 > n3
	if "B1" in assignments and "B2" in assignments and \
		"B3" in assignments and "B4" in assignments and \
		"C1" in assignments and "C2" in assignments and \
		"C3" in assignments and "C4" in assignments:
			n2_length = N2_length(assignments["B1"], assignments["B2"], \
						assignments["B3"], assignments["B4"])
			n3_length = N3_length(assignments["C1"], assignments["C2"], \
						assignments["C3"], assignments["C4"])				
			if n2_length <= n3_length:
				return False
	# asserting n3 > n4
	if "C1" in assignments and "C2" in assignments and \
		"C3" in assignments and "C4" in assignments and \
		"D1" in assignments and "D2" in assignments and \
		"D3" in assignments:
			n3_length = N3_length(assignments["C1"], assignments["C2"], \
						assignments["C3"], assignments["C4"])				
			n4_length = N4_length(assignments["D1"], assignments["D2"], \
				assignments["D3"])
			if n3_length <= n4_length:
				return False
	# asserting n4 > n5		
	if "D1" in assignments and "D2" in assignments and \
		"D3" in assignments and "E1" in assignments) and \
		"E2" in assignments:
			n4_length = N4_length(assignments["D1"], assignments["D2"], \
				assignments["D3"])
			n5_length = N5_length(assignments["E1"], assignments["E2"])
			if n4_length <= n5_length:
				return False
	# asserting n5 > n6
	if "E1" in assignments and "E2" in assignments and \
		"F1" in assignments and "F2" in assignments:
			n5_length = N5_length(assignments["E1"], assignments["E2"])
			n6_length = N6_length(assignments["F1"], assignments["F2"])
			if n5_length <= n6_length:
				return False
	return True

def ddiff_similar(assignments):
	A_B_diff = B_C_diff = C_D_diff = D_E_diff = E_F_diff = F_G_diff = 0
	if "A" in assignments and "B1" in assignments:
		A_B_diff = assignments["A"]["D"] - assignments["B1"]["D"]
	if "B1" in assignments and "C1" in assignments:
		B_C_diff = assignments["B1"]["D"] - assignments["C1"]["D"]
	if "C1" in assignments and "D1" in assignments:
		C_D_diff = assignments["C1"]["D"] - assignments["D1"]["D"]
	if "D1" in assignments and "E1" in assignments:
		D_E_diff = assignments["D1"]["D"] - assignments["E1"]["D"]
	if "E1" in assignments and "F1" in assignments:
		E_F_diff = assignments["E1"]["D"] - assignments["F1"]["D"]
	if "F1" in assignments and "g" in assignments:
		F_G_diff = assignments["F1"]["D"] - assignments["G"]["D"]
	if A_B_diff == B_C_diff == C_D_diff == D_E_diff == E_F_diff == F_G_diff:
		return True
	return False

def diam_diff(assignments):
	A_B_diff = B_C_diff = C_D_diff = D_E_diff = \
	E_F_diff = F_G_diff = desired_ney["diam_diff_upper"] + \
		desired_ney["diam_diff_lower"]) / 2
	if "A" in assignments and "B1" in assignments:
		A_B_diff = assignments["A"]["D"] - assignments["B1"]["D"]
	if "B1" in assignments and "C1" in assignments:
		B_C_diff = assignments["B1"]["D"] - assignments["C1"]["D"]
	if "C1" in assignments and "D1" in assignments:
		C_D_diff = assignments["C1"]["D"] - assignments["D1"]["D"]
	if "D1" in assignments and "E1" in assignments:
		D_E_diff = assignments["D1"]["D"] - assignments["E1"]["D"]
	if "E1" in assignments and "F1" in assignments:
		E_F_diff = assignments["E1"]["D"] - assignments["F1"]["D"]
	if "F1" in assignments and "G" in assignments:
		F_G_diff = assignments["F1"]["D"] - assignments["G"]["D"]
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

def nodes_similar(assignments):
	if "A" in assignments and "B1" in assignments:
		if assignments["A"]["TH"] != assignments["B1"]["TH"] or \
		   assignments["A"]["R"] != assignments["B1"]["R"] or \
		   assignments["A"]["D"] != assignments["B1"]["D"]:
		   	return False
	if "B1" in assignments and "C1" in assignments:
		if assignments["B1"]["TH"] != assignments["C1"]["TH"] or \
		   assignments["B1"]["R"] != assignments["C1"]["R"] or \
		   assignments["B1"]["D"] != assignments["C1"]["D"]:
		   	return False
		B_C_diff = assignments["B1"]["D"] - assignments["C1"]["D"]
	if "C1" in assignments and "D1" in assignments:
		if assignments["C1"]["TH"] != assignments["D1"]["TH"] or \
		   assignments["C1"]["R"] != assignments["D1"]["R"] or \
		   assignments["C1"]["D"] != assignments["D1"]["D"]:
		   	return False
	if "D1" in assignments and "E1" in assignments:
		if assignments["D1"]["TH"] != assignments["E1"]["TH"] or \
		   assignments["D1"]["R"] != assignments["E1"]["R"] or \
		   assignments["D1"]["D"] != assignments["E1"]["D"]:
		   	return False
	if "E1" in assignments and "F1" in assignments:
		if assignments["E1"]["TH"] != assignments["F1"]["TH"] or \
		   assignments["E1"]["R"] != assignments["F1"]["R"] or \
		   assignments["E1"]["D"] != assignments["F1"]["D"]:
		   	return False
	if "F1" in assignments and "G" in assignments:
		if assignments["F1"]["TH"] != assignments["G"]["TH"] or \
		   assignments["F1"]["R"] != assignments["G"]["R"] or \
		   assignments["F1"]["D"] != assignments["G"]["D"]:
		   	return False
	return True

def h1_length(assignments):
	if "A" not in assignments or \
		"B1" not in assignments or \
		"B2" not in assignments or \
		"B3" not in assignments or \
		"B4" not in assignments or \
		"C1" not in assignments or \
		"C2" not in assignments or \
		"C3" not in assignments or \
		"C4" not in assignments or ]
		"D1" not in assignments or \
		"D2" not in assignments or \
		"D3" not in assignments or \
		"E1" not in assignments or \
		"E2" not in assignments or \
		"F1" not in assignments or \
		"F2" not in assignments or \
		"G" not in assignments:
			return True	
	chunks_length = A_length(assignments["A"])
	chunks_length += N2_length(assignments["B1"], assignments["B2"], \
		assignments["B3"], assignments["B4"])
	chunks_length += N3_length(assignments["C1"], assignments["C2"], \
				assignments["C3"], assignments["C4"])
	chunks_length += N4_length(assignments["D1"], assignments["D2"], \
				assignments["D3"])
	chunks_length += N5_length(assignments["E1"], assignments["E2"])
	chunks_length += N6_length(assignments["F1"], assignments["F2"])
	chunks_length += assignments["G"]["L"]
	return True if chunks_length == desired_ney["h1"] else False

def no_overlap(assignments):
	if len(assignments) < 2:
		return True
	piece_number = 0
	for var, value in assignments.items():
		if piece_number == value["NO"]:
			return False
		piece_number = value["NO"]
	return True
