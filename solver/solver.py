from spec import specs
from csp import CSP
from mac import MAC
from catalog import CATALOG
from pickup import SELECT
from constants import *
from unary import UNARY
import copy
import os

current = os.path.dirname(os.path.realpath(__file__))

class SOLVER():

	def __init__(self, csp, select, mac):
		self.__csp = csp
		self.__select = select
		self.__mac = mac
		X = self.__csp.get_variables()
		self.__confsets = {v: [] for v in X}
		
	def __confvars(self, A, inconsistents, confset, curvar):
		'''Decides which variables can be added to the conflict set.
		
		Returns conflicting variables in the order of assignment.'''
		confvars = []
		for var in A:
			if not var in inconsistents:
				continue
			if var == curvar: # would be redundant
				continue
			if var in confset: # prevent duplicates
				continue
			confvars.append(var)
		return confvars
		
	def __accumulate(self, curvar, inconsistents):
		'''Accumulates the conflict set for curvar.
		
		Conflict set must be sorted based on the time of assignment.
		The core notion of a conflict set is to create a time machine where
		order of variables in the set must follow the order of variables in 
		the assignment.
		
		Example:
		
		D1 -> R1 -> T1 -> L1 (if failes due to T1 and D1)
		
		confset[L1] = [D1, T1] so that jump happens first to T1 not D1
		
		Jumping must happen to the near past not distant past.
		
		Why would we repeat a long history? Why not jump to yesterday and
		make a tiny change and quicky get back to today?
		
		If we jumped to the last year instead, we would have to repeat a
		full year again to see if that solves the issue of today!
		'''
		if len(inconsistents) == 0:
			return
		A = self.__csp.get_assignment() # time sorted
		confset = self.__confsets[curvar]	
		confvars = self.__confvars(A, inconsistents, confset, curvar)
		if len(confvars) > 0:
			self.__confsets[curvar].extend(confvars)

	def __absorb(self, curvar, inconsistents):
		'''Absorbs conflict set from jump origin.
		
		Current variable incorporates in itself the conflict set of the
		variable that has failed in the future.
		
		This failure in the future happens due to legal assignments at
		some time in the past. Conflict set provides a time machine
		to travel back to the time when people made good moves, but
		future proves it wrong!
		
		People may not be able to see the effect of their actions far enough
		because it takes too much time to consider every scenario.
		'''
		if len(inconsistents) == 0:
			return
		A = self.__csp.get_assignment() # time sorted
		confset = self.__confsets[curvar]		
		confvars = self.__confvars(A, inconsistents, confset, curvar)
		if len(confvars) > 0:
			self.__confsets[curvar].extend(confvars)
							
	def __assign(self, curvar, value):
		'''Tries assigning curvar: value.
		
		If the assignment would cause coontradiction, a conflict set is
		returned.
		
		Note: If the contradiction occurs due to propagation, no conflict set
		is returned. In fact, only curvar is responsible for this.'''
		csp = self.__csp
		csp.assign(curvar, value)
		res = self.__mac.establish(curvar, value)
		if res[0] == CONTRADICTION:
			return (INCONSISTENT_ASSIGNMENT, res[2])
		if res[0] == DOMAINS_REDUCED:
			propagate_res = self.__mac.propagate(res[2])
			if propagate_res[0] == CONTRADICTION:
				return (INCONSISTENT_ASSIGNMENT, set([]))
		return (CONSISTENT_ASSIGNMENT, set([]))
		
	def __dfs(self):
		'''Recursively assigns values to variables to find a solution.
		
		When the domain of a variable is exhausted without any solution
		being found, the algorithm marks this as a new constraint and do
		not backjump to the last variable (yesterday), since backtracking
		occurs anyway.
		
		This case does not occur more than once before termination. However,
		adding this contradiction to a new constraint may help optimization 
		in the next phase of the project.
		'''
		csp = self.__csp
		if csp.unassigned_count() == 0: # solution
			return (SOLUTION, csp.get_assignment())
		curvar = self.__select.nextvar(csp)
		domain = copy.deepcopy(csp.get_domain(curvar))
		while True:
			val = self.__select.nextval(curvar, domain)				
			if val == DOMAIN_EXHAUSTED:
				if csp.assigned_count() == 0:
					return (SEARCH_SPACE_EXHAUSTED, None)
				if curvar in self.__confsets and len(self.__confsets[curvar]) > 0:
					jump_target = self.__confsets[curvar][-1]
					confset = self.__confsets[curvar]
					return (BACKJUMP, confset, jump_target)
				return (BACKTRACK, None)
			csp.backup_domains()
			assign_res = self.__assign(curvar, val)
			if assign_res[0] == INCONSISTENT_ASSIGNMENT:
				self.__accumulate(curvar, assign_res[1])
				csp.unassign(curvar)
				csp.revert_domains() # undo establish and propagation effects
				continue # try the next value
			dfs_res = self.__dfs()
			if dfs_res[0] in {SOLUTION, SEARCH_SPACE_EXHAUSTED}:
				return dfs_res
			csp.unassign(curvar)
			csp.revert_domains()
			if dfs_res[0] == BACKTRACK:
				continue
			if dfs_res[0] == BACKJUMP:
				if dfs_res[2] != curvar:
					return dfs_res
				else:
					self.__absorb(curvar, dfs_res[1])
					continue
	
	def find(self, catalog, spec):
		'''Runs MAC for all variables first and then calls DFS.
		
		If MAC figures out any contradiction before search begins, no
		solution could ever be found.'''
		UNARY.unarify(self.__csp, catalog, spec)
		X = copy.deepcopy(self.__csp.get_variables())
		res = self.__mac.propagate(X)
		if res[0] == CONTRADICTION:
			return CONTRADICTION
		return self.__dfs()

def human_readable(solution):
	'''Prints a prettified view of the given solution.'''
	for v in ["L1", "L2", "L3", "L4", "L5", "L6", "L7"]:
		print(v, ": ", solution[v])
	for v in ["D1", "D2", "D3", "D4", "D5", "D6", "D7"]:
		print(v, ": ", solution[v])
	print("T: ", solution["T1"])
	print("R: ", solution["R1"])

def main():
	catalog = CATALOG(current+"/pieces.csv")
	csp = CSP()
	select = SELECT(csp)
	mac = MAC(csp, catalog, specs["C"])
	solver = SOLVER(csp, select, mac)
	res = solver.find(catalog, specs["C"])
	if res[0] == SOLUTION:
		human_readable(res[1])
	else:
		print("No solution was found!")
			
if __name__ == "__main__":	
	main()
