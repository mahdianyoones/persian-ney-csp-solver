import time
from csp 			import remove_var, assigned_vars, init_csp, EMPTY_VALUE
from consistency 	import is_consistent, make_A_consistent, make_consistent

FAILURE = False
SUCCESS = True

nodes = 0


def select_var(csp, asmnt):
	# Degree sorted
	degree = ["A", "B1", "C1", "D1", "E1", "F1", "G",
				"B2", "B3", "B4", "C2", "C3", "C4", "D2", "D3", "E2", "F2"]
	asmnt_vars = assigned_vars(asmnt)
	unassigned_vars = [dsv for dsv in degree if not dsv in asmnt_vars]
	# MRV (minimum remaining values) heuristic
	mrv = float("inf")
	mrv_var = None
	for var in unassigned_vars:
		if len(csp["D"][var]) < mrv:
			mrv_var = var
			mrv = len(csp["D"][var])
	return mrv_var

def backjump(asmnt, csp, curvar):
	'''Backjumps to a conflict variable, if any.'''
	if len(csp["confvars"][curvar]) == 0:
		return (FAILURE, None) 	# Cannot backjump; just backtrack.
	asmnt_vars = assigned_vars(asmnt)
	jump_origin = curvar
	# from last to first
	for i in range(-1, -1 * len(asmnt_vars), -1):
		jump_target = asmnt_vars[i]
		if jump_target in csp["confvars"][curvar]:
			return (FAILURE, jump_target, jump_origin)
	return (FAILURE, None)

def in_confset(csp, asmnt, curvar, value):
	confasmnt = asmnt.copy()
	confasmnt.append((curvar, value))
	if tuple(confasmnt) in csp["confset"][curvar]:
		return True
	return False

def absorbconfs(csp, curvar, result):
	'''Absorbing conflict set and conflict vars from jump origin.'''
	jump_origin = result[2]
	o_confvars = csp["confvars"][jump_origin]
	o_confvars.remove(curvar)
	csp["confvars"][curvar].update(o_confvars)
	o_confset = csp["confset"][jump_origin]
	csp["confset"][curvar].update(o_confset)			

def backtrack(csp, asmnt):
	'''Implements Depth-first search (DFS) to solve the given CSP problem.'''
	global nodes
	asmnt_vars = assigned_vars(asmnt)
	if csp["X"] == set(asmnt_vars): # a complete assignment ?
		print("A solution has been found: ")
		return (SUCCESS, asmnt) # solution
	curvar = select_var(csp, asmnt)
	domain_backup = csp["D"][curvar].copy()
	if len(asmnt_vars) >= 1:
		make_consistent(csp, asmnt, curvar)
	varsleft = len(csp["X"]) - len(asmnt_vars)
	print("Trying ", curvar," - domain size : ", \
		len(csp["D"][curvar]), "confvars:",  csp["confvars"][curvar], \
		"confset size: ", len(csp["confset"][curvar]),
		"- vars left: ", varsleft)
	if len(csp["D"][curvar]) == 0:
		csp["D"][curvar] = domain_backup
		return backjump(asmnt, csp, curvar)
	for value in csp["D"][curvar]:
		nodes += 1
		if in_confset(csp, asmnt, curvar, value):
			print("Omitting conflict value for ", curvar)
			continue
		asmnt.append(tuple([curvar, value]))
		result = backtrack(csp, asmnt)
		# is it a solution?
		if result[0] == SUCCESS:
			return result
		else:
			jump_target = result[1]
			# a jumpover ?
			remove_var(curvar, asmnt)
			if jump_target != curvar and jump_target != None:
				print("Jumping over", curvar)
				csp["D"][curvar] = domain_backup
				return result
			elif jump_target == curvar: # simple jump
				absorbconfs(csp, curvar, result)
				print("Jumped back to ", jump_target," - domain size : ", \
					len(csp["D"][jump_target]), "confvars:", \
					csp["confvars"][jump_target], \
					"confset size: ", \
					len(csp["confset"][jump_target]))	
				#print(csp["confset"][jump_target])			
				# try other values excluding those just absorbed
				continue			
	csp["D"][curvar] = domain_backup
	remove_var(curvar, asmnt)
	# backtrack
	return (FAILURE, None)

def backtrack_search(csp):
	return backtrack(csp, [])

csp = init_csp()

make_A_consistent(csp)
print(backtrack_search(csp))
print("Nodes: ", nodes)
