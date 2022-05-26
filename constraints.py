TOP_NODE_MIN_LENGTH		36.5
THIRD_NODE_MIN_LENGTH	72
FOURTH_NODE_MIN_LENGTH	71
FIFTH_NODE_MIN_LENGTH	70
SIXTH_NODE_MIN_LENGTH	30
DIAMETER_DIFF_LOWER		0.5 # mm
DIAMETER_DIFF_UPPER		1.5 # mm

# Utility functions

def A_length(A, desired_ney):
	return A["length"] + desired_ney["mp_lenght"]

def N2_length(B1, B2, B3, B4):
	length = 0
	if B1 != None:
		length += B1["length"]
	if B2 != None:
		length += B2["length"]
	if B3 != None:
		length += B3["length"]
	if B4 != None:
		length += B4["length"]
	return length
	
def N3_length(C1, C2, C3, C4):
	length = 0
	if C1 != None:
		length += C1["length"]
	if C2 != None:
		length += C2["length"]
	if C3 != None:
		length += C3["length"]
	if C4 != None:
		length += C4["length"]
	return length

def N4_length(D1, D2, D3):
	length = 0
	if D1 != None:
		length += D1["length"]
	if D2 != None:
		length += D2["length"]
	if D3 != None:
		length += D3["length"]
	return length

def N5_length(E1, E2):
	length = 0
	if E1 != None:
		length += E1["length"]
	if E2 != None:
		length += E2["length"]
	return length
	
def N6_length(F1, F2):
	length = 0
	if F1 != None:
		length += F1["length"]
	if F2 != None:
		length += F2["length"]
	return length
	
# Unary constraints

# Top node diameter
def top_diameter(A, desired_ney):
	if A["diameter"] != desired_ney["min_top_diam"]:
		return False
	return True

# Top node length lower bound
def top_llower(A, desired_ney):
	if A_length(A, desired_ney) < TOP_NODE_MIN_LENGTH:
		return False
	return True

# Top node length upper bound
def top_lupper(A, desired_ney):
	if A_length(A, desired_ney) > desired_ney["h1"] - 263) / 3:
		return False
	return True


# Binary constraints


# Node 5 length lower bound
def n5_llower(E1, E2):
	n5_length = E1["length"]
	if E2 != None:
		n5_length += E2["length"]
		
	if n5_length < 70:
		return False
	return True
	
# Node 6 length lower bound
def n6_llower(F1, F2):
	n6_length = F1["length"]
	if F2 != None:
		n6_length += F2["length"]
		
	if n6_length < 30:
		return False
	return True

# Node 6 chunks similarity
def n6_chunks_sim(F1, F2):
	# F2 is an optional variable
	if F2 == None:
		return True
		
	if F1["diameter"] != F2["diameter"]
		return False
		
	if F1["roundness"] != F2["roundness"]
		return False

	if F1["thickness"] != F2["thickness"]
		return False
	return True

# Node 5 chunks similarity
def n5_chunks_sim(E1, E2):
	if E2 == None:
		return True
		
	if E1["diameter"] != E2["diameter"]
		return False
		
	if E1["roundness"] != E2["roundness"]
		return False

	if E1["thickness"] != E2["thickness"]
		return False
	return True

# Higher order constraints

# Node 1 is half of Node 2
def n1_half_n2(A, B1, B2, B3, B4, desired_ney):
	if A_length(A, desired_ney) == N2_length(B1, B2, B3, B4) * 2:
		return True
	return False

# Node 3 length lower bound and Node 4 length lower bound 
def n3n4_llower(C1, C2, C3, C4, D1, D2, D3):
	if N3_length(C1, C2, C3, C4) < THIRD_NODE_MIN_LENGTH:
		return False
	if N4_length(D1, D2, D3) < FOURTH_NODE_MIN_LENGTH:
		return False
	return True
	
# Hole 7 falls on Node 4
def h7_on_n4(A, B1, B2, B3, B4, C1, C2, C3, C4, desired_ney):
	chunks_length = A_length(A, desired_ney)
	chunks_length += N2_length(B1, B2, B3, B4)
	chunks_length += N3_length(C1, C2, C3, C4)
	if chunks_length + desired_ney["min_hj_dist"] < desired_ney["h7"]:
		return True
	return False

# Similarity between chunks of Node 2, Node 3, and Node 4
def chunks_similar(B1, B2, B3, B4, C1, C2, C3, C4, D1, D2, D3):
	if B1 != None and B2 != None:
		if B1["thickness"] != B2["thickness"] or \
		   B1["roundness"] != B2["roundness"] or \
		   B1["diameter"] != B2["diameter"]:
		   	return False
	if B2 != None and B3 != None:
		if B2["thickness"] != B3["thickness"] or \
		   B2["roundness"] != B3["roundness"] or \
		   B2["diameter"] != B3["diameter"]:
		   	return False
	if B3 != None and B4 != None:
		if B3["thickness"] != B4["thickness"] or \
		   B3["roundness"] != B4["roundness"] or \
		   B3["diameter"] != B4["diameter"]:
		   	return False
	
	if C1 != None and C2 != None:
		if C1["thickness"] != C2["thickness"] or \
		   C1["roundness"] != C2["roundness"] or \
		   C1["diameter"] != C2["diameter"]:
		   	return False
	if C2 != None and C3 != None:
		if C2["thickness"] != C3["thickness"] or \
		   C2["roundness"] != C3["roundness"] or \
		   C2["diameter"] != C3["diameter"]:
		   	return False
	if C3 != None and C4 != None:
		if C3["thickness"] != C4["thickness"] or \
		   C3["roundness"] != C4["roundness"] or \
		   C3["diameter"] != C4["diameter"]:
		   	return False

	if D1 != None and D2 != None:
		if D1["thickness"] != D2["thickness"] or \
		   D1["roundness"] != D2["roundness"] or \
		   D1["diameter"] != D2["diameter"]:
		   	return False
	if D2 != None and D3 != None:
		if D2["thickness"] != D3["thickness"] or \
		   D2["roundness"] != D3["roundness"] or \
		   D2["diameter"] != D3["diameter"]:
		   	return False

	return True

# Hole 6 falls at the end Node 4
def h6_end_n4(A, B1, B2, B3, B4, C1, C2, C3, C4, D1, D2, D3, desired_ney):
	chunks_length = A_length(A, desired_ney)
	chunks_length += N2_length(B1, B2, B3, B4)
	chunks_length += N3_length(C1, C2, C3, C4)
	chunks_length += N4_length(D1, D2, D3)
	if chunks_length == desired_ney["h6"] + desired_ney["min_hj_dist"]:
		return True

# Hole 5 falls on node 5
def h5_on_n5(A, B1, B2, B3, B4, C1, C2, C3, C4, D1, D2, D3, desired_ney):
	chunks_length = A_length(A, desired_ney)
	chunks_length += N2_length(B1, B2, B3, B4)
	chunks_length += N3_length(C1, C2, C3, C4)
	chunks_length += N4_length(D1, D2, D3)
	if chunks_length + desired_ney["min_hj_dist"] <= desired_ney["h5"]:
		return True
	return False

# Hole 4 falls on node 5 (below hole 5)
def h4_on_n5(A, B1, B2, B3, B4, C1, C2, C3, C4, D1, D2, D3, desired_ney):
	chunks_length = A_length(A, desired_ney)
	chunks_length += N2_length(B1, B2, B3, B4)
	chunks_length += N3_length(C1, C2, C3, C4)
	chunks_length += N4_length(D1, D2, D3)
	# hole 5 junction distance + hole 5 diameter + hole 5 hole 6 distance
	if chunks_length + desired_ney["min_hj_dist"] + desired_ney["h_diameter"] \
	 	+ desired_ney["min_hh_dist"] <= desired_ney["h4"]:
		return True
	return False

# Hole 3 falls at the end of node 5
def h3_endof_n5(A, B1, B2, B3, B4, C1, C2, C3, C4, D1, D2, D3, E1, E2, desired_ney):
	chunks_length = A_length(A, desired_ney)
	chunks_length += N2_length(B1, B2, B3, B4)
	chunks_length += N3_length(C1, C2, C3, C4)
	chunks_length += N4_length(D1, D2, D3)
	chunks_length += N5_length(E1, E2)
	if chunks_length + desired_ney["min_hj_dist"] == desired_ney["h3"]:
		return True
	return False

# Hole 2 falls at the beginning of node 6
def h2_startof_n6(A, B1, B2, B3, B4, C1, C2, C3, C4, D1, D2, D3, E1, E2, desired_ney):
	chunks_length = A_length(A, desired_ney)
	chunks_length += N2_length(B1, B2, B3, B4)
	chunks_length += N3_length(C1, C2, C3, C4)
	chunks_length += N4_length(D1, D2, D3)
	chunks_length += N5_length(E1, E2)
	if chunks_length + desired_ney["min_hj_dist"] <= desired_ney["h2"]:
		return True
	return False

# Length of nodes decrease from Node 2 to Node 6
def len_decrement(B1, B2, B3, B4, C1, C2, C3, C4, D1, D2, D3, E1, E2, F1, F2):
	if N2_length(B1, B2, B3, B4) <= N3_length(C1, C2, C3, C4):
		return False
	if N3_length(C1, C2, C3, C4 <= N4_length(D1, D2, D3)
		return False
	if N4_length(D1, D2, D3) <= N5_length(E1, E2):
		return False	
	if N5_length(E1, E2) <= N6_length(F1, F2):
		return False
	return True

# The diameter difference between adjacent nodes are similar
def ddiff_similar(A, B1, C1, D1, E1, F1, G):
	A_B_diff = A["diameter"] - B1["diameter"]
	B_C_diff = B1["diameter"] - C1["diameter"]
	C_D_diff = C1["diameter"] - D1["diameter"]
	D_E_diff = D1["diameter"] - E1["diameter"]
	E_F_diff = E1["diameter"] - F1["diameter"]
	F_G_diff = F1["diameter"] - G["diameter"]
	if A_B_diff == B_C_diff == C_D_diff == D_E_diff == E_F_diff == F_G_diff:
			return True
	return False

# The diameter difference between two adjacent nodes must be within a range
def diam_diff(A, B1, C1, D1, E1, F1, G):
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
		
	E_F_diff = E1["diameter"] - F1["diameter"]
	if DIAMETER_DIFF_LOWER > E_F_diff or DIAMETER_DIFF_UPPER < E_F_diff:
		return False	
		
	F_G_diff = F1["diameter"] - G["diameter"]
	if DIAMETER_DIFF_LOWER > F_G_diff or DIAMETER_DIFF_UPPER < F_G_diff:
		return False
	
	return True

# Similarity between nodes
def nodes_similar(A, B1, C1, D1, E1, F1, G):
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
	if E1 != None and F1 != None:
		if E1["thickness"] != F1["thickness"] or \
		   E1["roundness"] != F1["roundness"] or \
		   E1["diameter"] != F1["diameter"]:
		   	return False
	if F1 != None and G != None:
		if F1["thickness"] != G["thickness"] or \
		   F1["roundness"] != G["roundness"] or \
		   F1["diameter"] != G["diameter"]:
		   	return False
	return True

# Hole 1 must be equal to the length of all chunks	
def h1_length(A, B1, B2, B3, B4, C1, C2, C3, C4, D1, D2, D3, E1, E2, \
			F1, F2, G, desired_ney):
	chunks_length = A_length(A, desired_ney)
	chunks_length += N2_length(B1, B2, B3, B4)
	chunks_length += N3_length(C1, C2, C3, C4)
	chunks_length += N4_length(D1, D2, D3)
	chunks_length += N5_length(E1, E2)
	chunks_length += N6_length(F1, F2)
	chunks_length += G["length"]
	return chunks_length == desired_ney["h1"] ? True : False
