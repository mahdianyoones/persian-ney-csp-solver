import time
from csp 			import init_csp
from consistency 	import is_consistent, make_A_consistent, make_consistent

FAILURE = False
nodes = 0
EMPTY_VALUE = {
	"NO": 	0, 
	"L": 	0,
	"TH": 	0,
	"R":		0,
	"D":		0 
}

def select_unassigned_variable(csp, assignments):
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

def is_complete(csp, assignments):
	for var in csp["X"]:
		if not var in assignments:
			return False
	return True

# dfs search
def backtrack(csp, assignments):
	global nodes
	print(assignments)	
	if is_complete(csp, assignments):
		print("A solution has been found: ")
		return assignments # solution
	var = select_unassigned_variable(csp, assignments)
	domain_backup = csp["D"][var].copy()
	make_consistent(csp, assignments, var)
	for value in csp["D"][var]:
		nodes += 1
		assignments[var] = value
		result = backtrack(csp, assignments)
		if result != FAILURE:
			return result
		del assignments[var]
	csp["D"][var] = domain_backup
	return FAILURE

def backtrack_search(csp):
	return backtrack(csp, {})

csp = init_csp()
make_A_consistent(csp)
print(backtrack_search(csp))
print("Nodes: ", nodes)
