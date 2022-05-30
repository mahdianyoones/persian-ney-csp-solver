from csp 			import init_csp
from consistency 	import is_consistent, make_A_consistent

FAILURE	False

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
			if not is_consistent(assignments, var, value):
				csp["D"][un].remove(index)
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
	if is_complete(csp, assignments):
		return assignments # solution
	var = select_unassigned_var(csp, assignments)
	order_domain_values(csp, var, assignments)
	for value in csp["D"][var]:
		if is_consistent(var, value, assignments):
			assignments[var] = value
			inferences = inference(csp, var, assignments)
			if inferences != FAILURE:
				# inferences are already added in the inference callback
				result = backtrack(csp, assignments)
				if result != FAILURE:
					return result
				remove_inferences(csp, inferences)
			del assignments["var"]
	return FAILURE

def backtrack_search(csp):
	return backtrack(csp, {})
	
csp = init_csp()
make_A_consistent(csp)
print(backtrack_search(csp))
