from csp 			import init_csp
from consistency 	import is_consistent, make_A_consistent

FAILURE = False
nodes = 0
EMPTY_VALUE = {
	"NO": 	0, 
	"L": 	0,
	"TH": 	0,
	"R":		0,
	"D":		0 
}

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
	for index, value in enumerate(csp["D"][var]):
		if value == EMPTY_VALUE:
			# trying to discard optional variables for now
			csp["D"][var][index]["V"] = float("-inf")
			continue
		csp["D"][var][index]["V"] = 0
		for constraint in imc:
			if not is_consistent(csp, assignments, var, value):
				csp["D"][var][index]["V"] += 1
	csp["D"][var] = sorted(csp["D"][var], key=lambda value: value["V"], \
		reverse=True)

def is_complete(csp, assignments):
	for var in csp["X"]:
		if not var in assignments:
			return False
	return True

# forward checking
def inference(csp, var, assignments):
	uns = [] # unassigned neighbors
	for constraint in csp["X_C"][var]:
		for un in csp["X"]:
			if un != var and un in csp["C"][constraint] and \
				not un in assignments:
				uns.append(un)
	inferences = {}
	for un in uns:
		inferences[un] = []
		for index, value in enumerate(csp["D"][un]):
			if not is_consistent(csp, assignments, un, value):
				del csp["D"][un][index]
				inferences[un].append(value)
		if len(csp["D"][un]) == 0:
			csp["D"][un].extend(inferences[un]) # undoing domain reduction
			return FAILURE
		if len(inferences[un]) == 0:
			del inferences[un]
	return inferences

def remove_inferences(csp, inferences):
	for var in inferences.keys():
		csp["D"][var].extend(inferences[var])

# dfs search
def backtrack(csp, assignments):
	global nodes
	if is_complete(csp, assignments):
		print("A solution has been found: ")
		return assignments # solution
	var = select_unassigned_variable(csp, assignments)
	order_domain_values(csp, var, assignments)
	for value in csp["D"][var]:
		nodes += 1
		if is_consistent(csp, assignments, var, value):
			assignments[var] = value
			inferences = inference(csp, var, assignments)
			if inferences != FAILURE:
				# inferences are already added in the inference callback
				result = backtrack(csp, assignments)
				if result != FAILURE:
					return result
				remove_inferences(csp, inferences)
			del assignments[var]
	return FAILURE

def backtrack_search(csp):
	return backtrack(csp, {})

csp = init_csp()
make_A_consistent(csp)
print(backtrack_search(csp))
print("Nodes: ", nodes)
