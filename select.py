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
	
# Selects next unassigned value applying MRV and Degree heuristics
def select_var(CSP, assignments):		
	left_vars = left_requried_vars(assignments)
	if left_req_vars == []:
		left_vars = left_optional_vars(assignments)
	mrv = float("inf")
	for left_var in left_vars:
		if CSP["D_count"][left_var] < mrv:
			mrv_var = left_var
			mrv = CSP["D_count"][left_var]
	return mrv_var
	
# Sorts the variable domain values applying least constraining value heuristic
def lcv_sort(CSP, var, values):
	# the value that rules out fewest options for its neighbors
	
	
	# D_A = {
		thickness: [1, 1.5, 2, 2.5, 3, 3.5],
		roundness: [0, 1, 1.5, 2, 2.5],
		diameter: [ 18, 19, 20, 21, 22, 23, 24, 25, 26],
		length: [20, 21, 22, 23, 24, ..., 200]
		length: {
			20: 120,
			21: 130,
			.
			.
			.
			60: 50,
			150: 1:
			"sum": 620
		},
		thickness: {
			1: 1000,
			1.5: 500,
			2: 200,
			2.5: 210,
			3: 40
		}
		
		diameter: {
			18: 20
		},
		possible_pieces
	# }
	# ...... 20 -> 40 = 20 ; 37 to 40 = 3
	# .. 20
	# ............ 20 -> 120 = 100 ; 37 to 120 = 83
	# ... 20 -> 30 = 10 x
	# ........ 37 to 50 -> 13
	# 30
	# ................. 20 - 150 = 130 ; 37 to 150 = 113
	
