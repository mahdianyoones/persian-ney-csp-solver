# Returns a list of unassigned neighbors of var

def unassigned_neighbors(csp, var, assignments):
	

# Selects next unassigned value applying MRV and Degree heuristics
def select_unassigned_variable(CSP, assignments):
	# Degree sorted
	degree_sorted = ["A", "B1", "C1", "D1", "E1", "F1", "G",
				"B2", "B3", "B4", "C2", "C3", "C4",
				"D2", "D3", "E2", "F2"
	]
	unassigned_vars = []
	for var in degree_sorted:
		if not var in assignments:
			unassigned_vars.append(var)
	mrv = float("inf")
	_var = unassigned_vars[0]
	for var in unassigned_vars:
		if len(csp["D"][var]) < mrv:
			_var = var
			mrv = len(csp["D"][var])
	return _var

def order_domain_values(csp, var, assignments):
	for value in csp["D"][var]:
		_assignments = assignments.clone()
		_assignments[var] = value
		
