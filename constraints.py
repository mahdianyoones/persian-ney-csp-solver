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
	if 	not ("B1" in assignments and "B2" in assignments and \
			"B3" in assignments and "B4" in assignments and \
			"C1" in assignments) \
		and not ("C1" in assignments and "C2" in assignments and \
			"C3" in assignments and "C4" in assignments and \
			"D1" in assignments) \
		and not ("D1" in assignments and "D2" in assignments and \
			"D3" in assignments and "E1" in assignments) \
		and not ("E1" in assignments and "E2" in assignments and \
			"F1" in assignments):
			return True
	if	"B1" in assignments and "B2" in assignments and \
		"B3" in assignments and "B4" in assignments and \
		"C1" in assignments:
		# TODO: finishd this callback
	n2_length = N2_length(assignments["B1"], assignments["B2"], \
				assignments["B3"], assignments["B4"])
	n3_length = N3_length(assignments["C1"], assignments["C2"], \
				assignments["C3"], assignments["C4"])
	n4_length = N4_length(assignments["D1"], assignments["D2"], \
				assignments["D3"])
	n5_length = N5_length(assignments["E1"], assignments["E2"])
	n6_length = N6_length(assignments["F1"], assignments["F2"])
	
	if n2_length <= n3_length:
		return False
	if n3_length <= n4_length:
		return False
	if n4_length <= n5_length:
		return False	
	if n5_length <= n6_length:
		return False
	return True

# The diameter difference between adjacent nodes are similar
def ddiff_similar(A, B1, C1, D1, E1, assignments["F1"], G):
	A_B_diff = A["diameter"] - B1["diameter"]
	B_C_diff = B1["diameter"] - C1["diameter"]
	C_D_diff = C1["diameter"] - D1["diameter"]
	D_E_diff = D1["diameter"] - E1["diameter"]
	E_F_diff = E1["diameter"] - assignments["F1"]["diameter"]
	F_G_diff = assignments["F1"]["diameter"] - G["diameter"]
	if A_B_diff == B_C_diff == C_D_diff == D_E_diff == E_F_diff == F_G_diff:
			return True
	return False

# The diameter difference between two adjacent nodes must be within a range
def diam_diff(A, B1, C1, D1, E1, assignments["F1"], G):
	A_B_diff = A["diameter"] - B1["diameter"]	
	if DIAMETER_DIFF_LOWER > A_B_diff or DIAMETER_DIFF_UPPER < A_B_diff:
		return False
		
	B_C_diff = B1["diameter"] - C1["diameter"]
	if DIAMETER_DIFF_LOWER > B_C_diff or DIAMETER_DIFF_UPPER < B_C_diff:
		return False
		
	C_D_diff = C1["diameter"] - D1["diameter"]
	if DIAMETER_DIFF_LOWER > C_D_diff or DIAMETER_DIFF_UPPER < C_D_diff:
		return False	
		
	D_E_diff = D1["diameter"] - E1["diameter"]
	if DIAMETER_DIFF_LOWER > D_E_diff or DIAMETER_DIFF_UPPER < D_E_diff:
		return False	
		
	E_F_diff = E1["diameter"] - assignments["F1"]["diameter"]
	if DIAMETER_DIFF_LOWER > E_F_diff or DIAMETER_DIFF_UPPER < E_F_diff:
		return False	
		
	F_G_diff = assignments["F1"]["diameter"] - G["diameter"]
	if DIAMETER_DIFF_LOWER > F_G_diff or DIAMETER_DIFF_UPPER < F_G_diff:
		return False
	
	return True

# Similarity between nodes
def nodes_similar(A, B1, C1, D1, E1, assignments["F1"], G):
	if A != None and B1 != None:
		if A["thickness"] != B1["thickness"] or \
		   A["roundness"] != B1["roundness"] or \
		   A["diameter"] != B1["diameter"]:
		   	return False
	if B1 != None and C1 != None:
		if B1["thickness"] != C1["thickness"] or \
		   B1["roundness"] != C1["roundness"] or \
		   B1["diameter"] != C1["diameter"]:
		   	return False
	if C1 != None and D1 != None:
		if C1["thickness"] != D1["thickness"] or \
		   C1["roundness"] != D1["roundness"] or \
		   C1["diameter"] != D1["diameter"]:
		   	return False
	if D1 != None and E1 != None:
		if D1["thickness"] != E1["thickness"] or \
		   D1["roundness"] != E1["roundness"] or \
		   D1["diameter"] != E1["diameter"]:
		   	return False
	if E1 != None and assignments["F1"] != None:
		if E1["thickness"] != assignments["F1"]["thickness"] or \
		   E1["roundness"] != assignments["F1"]["roundness"] or \
		   E1["diameter"] != assignments["F1"]["diameter"]:
		   	return False
	if assignments["F1"] != None and G != None:
		if assignments["F1"]["thickness"] != G["thickness"] or \
		   assignments["F1"]["roundness"] != G["roundness"] or \
		   assignments["F1"]["diameter"] != G["diameter"]:
		   	return False
	return True

# Hole 1 must be equal to the length of all chunks	
def h1_length(A, B1, B2, B3, B4, C1, C2, C3, C4, D1, D2, D3, E1, E2, \
			assignments["F1"], F2, G, desired_ney):
	chunks_length = A_length(A, desired_ney)
	chunks_length += N2_length(B1, B2, B3, B4)
	chunks_length += N3_length(C1, C2, C3, C4)
	chunks_length += N4_length(D1, D2, D3)
	chunks_length += N5_length(E1, E2)
	chunks_length += N6_length(assignments["F1"], F2)
	chunks_length += G["length"]
	return True if chunks_length == desired_ney["h1"] else False
	
#def no_overlap(A, B1, B2, B3, B4, C1, C2, C3, C4, D1, D2, D3, E1, E2, \
#			assignments["F1"], F2, G):
#			
