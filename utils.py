from ney_spec import desired_ney

def A_length(A):
	return A[1] + desired_ney["mp_lenght"]

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
	
