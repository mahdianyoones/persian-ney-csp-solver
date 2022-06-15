import time
import os
from csp import remove_var, assigned_vars, init_csp, EMPTY_VALUE
from consistency import learn_constraint, is_consistent, make_A_consistent, consistent_values
from conflict import absorb_confset

FAILURE = False
SUCCESS = True

backjumps_counter = 0
backtrack_counter = 0
legal_values_counter = {}
nodes = 0

def report(asmnt, curvar, legal_values):
	global backjumps_counter, backtrack_counter, nodes
	os.system("clear")
	print("Nodes: ", nodes)
	print("Trying: ", asmnt)
	print("Backtracks: ", backtrack_counter)
	print("Backjumps: ", backjumps_counter)
	print("Curvar: ", curvar)
	sp = 1
	for v, c in legal_values_counter.items():
		sp *= c if c > 0 else 1
		print(v, " ---- Legal values :", c, " ---- Conflict set: ", csp["confset"][v])
	print("Search space: ", sp)
	print("Learned constraints: ")
	for r, tuples in csp["R"].items():
		print(r, ": ", len(tuples))

def select_var(csp, asmnt):
	'''Selects a variable using MRV‌ and degree heurisitcs.'''
	global nodes
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
	(failure indicator, jump target) => backjump
	'''
	global backjumps_counter, backtrack_counter, jumpover_counter, nodes
	nodes += 1
	if csp["X"] == set(assigned_vars(asmnt)): # complete? solution.
		return (SUCCESS, asmnt)
	curvar = select_var(csp, asmnt)
	legal_values = consistent_values(csp, asmnt, curvar)
	legal_values_counter[curvar] = len(legal_values)
	for value in legal_values:
		asmnt.append(tuple([curvar, value]))
		report(asmnt, curvar, legal_values)
		#forward_check(csp, asmnt, curvar)
		result = backtrack(csp, asmnt)
		if result[0] == SUCCESS: # a solution?
			return result
		remove_var(curvar, asmnt)
		if result[1] == None: # backtrack ?
			backtrack_counter += 1
			continue
		if result[1] == curvar: # jump ?
			backjumps_counter += 1
			absorb_confset(csp, curvar, result[2])
			continue
		else: # a jumpover
			return result
	if len(legal_values) > 0:
		learn_constraint(csp, asmnt, assigned_vars(asmnt), curvar)
	if len(csp["confset"][curvar]) == 0:
		backtrack_counter += 1
		return (FAILURE, None) # do backtrack
	else:
		backjumps_counter += 1
		return (FAILURE, csp["confset"][curvar][-1], curvar) # do jumpback
	
def backtrack_search(csp):
	return backtrack(csp, [])

csp = init_csp()

make_A_consistent(csp)
print(backtrack_search(csp))
#print("Nodes: ", nodes)
