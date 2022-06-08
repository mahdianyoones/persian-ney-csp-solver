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

def select_var(csp, asmnt):
	# Degree sorted
	degree_sorted = ["A", "B1", "C1", "D1", "E1", "F1", "G",
				"B2", "B3", "B4", "C2", "C3", "C4",
				"D2", "D3", "E2", "F2"
	]
	unassigned_vars = []
	for var in degree_sorted:
		if not var in asmnt:
			unassigned_vars.append(var)
	# MRV (minimum remaining values) heuristic
	mrv = float("inf")
	for var in unassigned_vars:
		if len(csp["D"][var]) < mrv:
			_var = var
			mrv = len(csp["D"][var])
	return _var

def is_complete(csp, asmnt):
	if
	for var in csp["X"]:
		if not var in asmnt:
			return False
	return True

def backjump(asmnt, csp, curvar):
	'''Backjumps if possible'''
	# Cannot backjump; just backtrack.
	if len(csp["confvars"][curvar]) == 0:
		return (FAILURE, None)
	asmnt_vars = list(asmnt.keys())
	# from last to first
	for i in range(-1, -1 * len(asmnt_vars), -1):
		recent = asmnt_vars[i]
		if recent in csp["confvars"][curvar]:
			return (FAILURE, recent)

def in_confset(csp, asmnt, curvar, value):
	val = {(_var, tuple(asmnt[_var].values())) for _var in asmnt.keys()}
	val.add((curvar, tuple(value.values())))
	return True if val in csp["confset"][curvar] else False

# dfs search
def backtrack(csp, asmnt):
	global nodes
	print(asmnt)
	if is_complete(csp, asmnt):
		print("A solution has been found: ")
		return (SUCCESS, asmnt) # solution
	curvar = select_var(csp, asmnt)
	domain_backup = csp["D"][curvar].copy()
	if len(asmnt.keys()) > 1:
		make_consistent(csp, asmnt, curvar)
	if len(csp["D"][curvar]) == 0:
		csp["D"][curvar] = domain_backup
		return backjump(asmnt, csp, curvar)
	for value in csp["D"][curvar]:
		nodes += 1
		if in_confset(csp, asmnt, curvar, value):
			continue
		asmnt[curvar] = value
		result = backtrack(csp, asmnt)
		# is it a solution?
		if result[0] == SUCCESS:
			return result
		else:
			if result[1] != curvar and result[1] != None: # a jumpover ?
				csp["D"][curvar] = domain_backup
				return result
			elif result[1] == curvar: # simple jump
				# absorbing conflict set
				jump_origin = result[1]
				origin_confvars = csp["confvars"][jump_origin]
				csp["confvars"][curvar].update(origin_confvars)
				csp["confset"][curvar].update(csp["confset"][jump_origin])			
				continue # try other values excluding those just absorbed
	csp["D"][curvar] = domain_backup
	return (FAILURE, None) # backtrack

def backtrack_search(csp):
	return backtrack(csp, {})

csp = init_csp(csp)
make_A_consistent(csp)
print(backtrack_search(csp))
print("Nodes: ", nodes)
