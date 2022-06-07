import time
from csp 			import init_csp
from consistency 	import is_consistent, make_A_consistent, make_consistent

FAILURE = False
SUCCESS = True
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

def backjump(asmnt, csp, curvar):
	'''Backjumps if possible'''
	# Cannot backjump; just backtrack.
	if len(csp["confvars"][curvar]) == 0:
		return (FAILURE, None)
	asmnt_vars = list(asmnt.keys())
	# from last to first
	recent = None
	for i in range(-1, -1 * len(asmnt_vars), -1):
		recent = asmnt_vars[i]
		if recent in csp["confvars"][curvar]:
			return (FAILURE, recent)

def in_confset(csp, asmnt, curvar, value):
	val = {(_var, asmnt[_var]) for _var in asmnt_keys.keys()}
	val.add((curvar, value))
	return True ? val in csp["css"][curvar] : False

# dfs search
def backtrack(csp, assignments):
	global nodes
	print(assignments)	
	if is_complete(csp, assignments):
		print("A solution has been found: ")
		return (SUCCESS, assignments) # solution
	curvar = select_unassigned_variable(csp, assignments)
	domain_backup = csp["D"][curvar].copy()
	make_consistent(csp, assignments, curvar)
	if len(csp["D"][curvar]) == 0:
		csp["D"][curvar] = domain_backup
		return backjump(asmnt, csp, curvar)
	for value in csp["D"][curvar]:
		nodes += 1
		if in_confset(csp, asmnt, var, value);
			continue
		assignments[curvar] = value
		result = backtrack(csp, assignments)
		# is it a solution?
		if result[0] == SUCCESS:
			return result
		else:
			if result[1] != curvar and result[1] != None: # a jumpover ?
				del assignments[curvar]
				csp["D"][curvar] = domain_backup
				return result
			elif result[1] == curvar: # simple jump
				# absorbing conflict set
				jump_origin = result[1]
				origin_confvars = csp["confvars"][jump_origin]
				csp["confvars"][curvar].update(origin_confvars)
				csp["confvars"][curvar].remove(curvar)
				csp["css"][curvar].update(csp["css"][jump_origin])			
				continue # try other values excluding those just absorbed
		# backtrack
	csp["D"][curvar] = domain_backup
	return (FAILURE, None)

def backtrack_search(csp):
	return backtrack(csp, {})

csp = init_csp()
make_A_consistent(csp)
print(backtrack_search(csp))
print("Nodes: ", nodes)
