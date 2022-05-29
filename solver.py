from domain 		import init_domain
from csp 			import csp
from consistency 	import make_A_consistent

# Returns constraints between var and variables in the assignment
def neighborhoods(csp, assignment, var):
	neighborhoods = set([])
	for constraint in csp["X_C"][var]:
		for assigned_var in assignment.keys():
			if assigned_var in csp["C"][constraint]:
				neighborhoods.add(constraint)
	return neighborhoods
	
def is_consistent(assignment, var, value):
	_assignment = assignment
	_assignment[var] = value
	for constraint in neighborhoods:
		

# Returns True if all variables are assigned
def is_complete(csp, assignment):
	for var in csp["X"]:
		if not var in assignment:
			return False
	return True

# implements dfs search
def backtrack(csp, assignment):
	if is_complete(csp, assignment):
		return assignment # solution
	var = select_unassigned_var(csp, assignment)
	for value in order_domain_values(csp, var, assignment):
		if is_consistent(var, value, assignment):
			assignment[var] = value
			inferences = inference(csp, var, assignment)
			if inferences != False:
				csp["inferences"].append(inferences)
				result = backtrack(csp, assignment)
				if result != False:
					return result
				# TODO: remove inferences here
			del assignment["var"]
	return False

def backtrack_search(csp):
	return backtrack(csp, {})
	
init_domain(csp)

make_A_consistent(csp)

print(backtrack_search(csp))

#print (dfs_search(CSP, desired_ney))
