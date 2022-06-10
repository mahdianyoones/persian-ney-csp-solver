import time
import os
from csp import remove_var, assigned_vars, init_csp, EMPTY_VALUE
from consistency import learn_constraint, is_consistent, make_A_consistent, consistent_values
from conflict import absorb_confset

FAILURE = False
SUCCESS = True

def select_var(csp, asmnt):
	'''Selects a variable using MRV‌ and degree heurisitcs.'''
	degree = ["A", "B1", "C1", "D1", "E1", "F1", "G",
				"B2", "B3", "B4", "C2", "C3", "C4", "D2", "D3", "E2", "F2"]
	# TODO: MRV looks redundant without forward checking
	mrv = float("inf")
	mrv_var = None
	# looks into unassigned variables
	asmnt_vars = assigned_vars(asmnt)
	for var in [dsv for dsv in degree if not dsv in asmnt_vars]:
		if len(csp["D"][var]) < mrv:
			mrv_var = var
			mrv = len(csp["D"][var])
	return mrv_var
	
def backtrack(csp, asmnt):
	'''Implements Depth-first search (DFS) to solve the given CSP problem.

	Returns a tuple of either of these formats:
	
	(failure indicator, None)		=> backtrack or end
	(success indicator, solution)		=> end
	(failure indicator, conflict set) => backjump
	'''
	if csp["X"] == set(assigned_vars(asmnt)): # complete? solution.
		return (SUCCESS, asmnt)
	curvar = select_var(csp, asmnt)
	legal_values = consistent_values(csp, asmnt, curvar)
	for value in legal_values:
		asmnt.append(tuple([curvar, value]))
		result = backtrack(csp, asmnt)
		if result[0] == SUCCESS: # a solution?
			return result
		remove_var(curvar, asmnt)
		if result[1] == None: # backtrack ?
			continue
		if result[1] == curvar: # jump ?
			absorb_confset(csp, curvar, result[2])
			continue
		else: # a jumpover
			return result
	if len(legal_values) > 0:
		learn_constraint(csp, asmnt, assigned_vars(asmnt), curvar)
	if len(csp["confset"][curvar]) == 0:
		return (FAILURE, None)
	# jump target: a variable in the last conflict set
	confset = list(csp["confset"][curvar][-1])
	return (FAILURE, confset[-1], csp["confset"][curvar])
	
def backtrack_search(csp):
	return backtrack(csp, [])

csp = init_csp()

make_A_consistent(csp)
print(backtrack_search(csp))
#print("Nodes: ", nodes)
