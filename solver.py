import time
import os
from csp import remove_var, assigned_vars, init_csp, EMPTY_VALUE
from consistency import is_consistent, make_A_consistent, make_consistent
from conflict import in_confset

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
	if len(asmnt) == 0:
		return (FAILURE, None) # No solution has been found
	confvars = csp["confvars"][curvar]
	if len(confvars) == 0:
		return (FAILURE, None) # Backtracking
	jump_origin = curvar
	# from last to first
	jump_target = confvars[-1]
	return (FAILURE, jump_target, jump_origin)

def absorbconfs(csp, curvar, jump_origin):
	'''Absorbing conflict set and conflict vars from jump origin.'''
	for confvar in csp["confvars"][jump_origin]:
		if confvar != curvar and not confvar in csp["confvars"][curvar]:
			csp["confvars"][curvar].append(confvar)
	
def backtrack(csp, asmnt):
	'''Implements Depth-first search (DFS) to solve the given CSP problem.'''
	global nodes
	asmnt_vars = assigned_vars(asmnt)
	if csp["X"] == set(asmnt_vars): # a complete assignment ?
		return (SUCCESS, asmnt) # solution
	curvar = select_var(csp, asmnt)
	domain_backup = csp["D"][curvar].copy()
	if len(asmnt_vars) >= 1:
		make_consistent(csp, asmnt, curvar)
	legal_values = csp["D"][curvar].copy()
	csp["D"][curvar] = domain_backup # reverting the domain 
	for value in legal_values:
		if in_confset(csp, asmnt, curvar, value):
			remove_var(curvar, asmnt)
			continue
		nodes += 1
		print("Nodes: ", nodes)
		asmnt.append(tuple([curvar, value]))
		result = backtrack(csp, asmnt)
		if result[0] == SUCCESS: # a solution?
			return result
		remove_var(curvar, asmnt)
		jump_target = result[1]
		if jump_target != curvar and jump_target != None: # a jumpover ?
			return result
		elif jump_target == curvar: # a jump?
			absorbconfs(csp, curvar, result[2])
			continue	
	# Backjump / backtrack
	return backjump(asmnt, csp, curvar)
	
def backtrack_search(csp):
	return backtrack(csp, [])

csp = init_csp()

make_A_consistent(csp)
print(backtrack_search(csp))
print("Nodes: ", nodes)
