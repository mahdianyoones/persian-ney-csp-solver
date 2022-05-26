def left_requried_vars(assignments):
	left = []
	for var in ["A", "B1", "C1", "D1", "E1", "F1", "G"]: # Degree sorted
		if var not in assignments:
			left.append(var)
	return left

def left_optional_vars(assignments):
	left = []
	for var in ["B2", "B3", "B4", "C2", "C3", "C4", "D2", "D3", "E2", "F2"]: # Degree sorted
		if var not in assignments:
			left.append(var)
	return left
	
def select_var(CSP, assignments):
		
	left_req_vars = left_requried_vars(assignments)
	if left_req_vars != []:
		mrv_sorted = MRV_sort(CSP, left_req_vars)
		return mrv_sorted[0]
	
	left_optional_vars = left_optional_vars(assignments)
	mrv_sorted = mrv(CSP, left_optional_vars)
	return mrv_sorted[0]
	
