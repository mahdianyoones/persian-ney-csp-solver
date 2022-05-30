VAR_NOT_USED None

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
	# MRV (minimum remaining values) heuristic
	mrv = float("inf")
	for var in unassigned_vars:
		if len(csp["D"][var]) < mrv:
			_var = var
			mrv = len(csp["D"][var])
	return _var

def order_domain_values(csp, var, assignments):
	# value["V"] : the number of constraints violated due to this value
	# Impacting constraints: a set of constraints with unassigned neighbors
	imc = set([])
	for constraint in csp["X_C"][var]:
		for var in csp["X"]:
			if var in csp["C"][constraint] and not var in assignments:
				imc.add(constraint)
	for value in csp["D"][var]:
		if value == VAR_NOT_USED:
			# trying to discard optional variables for now
			csp["D"][var]["V"] = float("-inf")
			continue
		csp["D"][var]["V"] = 0
		for constraint in imc:
			if not is_consistent(assignment, var, value):
				csp["D"][var]["V"] += 1
	csp["D"][var] = sorted(csp["D"][var], key=lambda value: value["V"], \
		reverse=True)
