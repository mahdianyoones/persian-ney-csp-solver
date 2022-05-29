from ney_spec import desired_ney

VAR_NOT_USED None

def A_length(A):
	return A["L"] + desired_ney["mp_lenght"]

def N2_length(B1, B2, B3, B4):
	length = B1["L"]
	if B2 != VAR_NOT_USED:
		length += B2["L"]
	if B3 != VAR_NOT_USED:
		length += B3["L"]
	if B4 != VAR_NOT_USED:
		length += B4["L"]
	return length
	
def N3_length(C1, C2, C3, C4):
	length += C1["L"]
	if C2 != VAR_NOT_USED:
		length += C2["L"]
	if C3 != VAR_NOT_USED:
		length += C3["L"]
	if C4 != VAR_NOT_USED:
		length += C4["L"]
	return length

def N4_length(D1, D2, D3):
	length = D1["L"]
	if D2 != VAR_NOT_USED:
		length += D2["L"]
	if D3 != VAR_NOT_USED:
		length += D3["L"]
	return length

def N5_length(E1, E2):
	length = E1["L"]
	if E2 != VAR_NOT_USED:
		length += E2["L"]
	return length
	
def N6_length(F1, F2):
	length = F1["L"]
	if F2 != VAR_NOT_USED:
		length += F2["L"]
	return lengths
