from spec import specs
from csp import CSP
from mac import MAC
from catalog import CATALOG
from pickup import SELECT
from constants import *
from unary import UNARY
import copy

class SOLVER():

	def __init__(self, csp, select, mac):
		self.__csp = csp
		self.__select = select
		self.__mac = mac
		X = self.__csp.get_variables()
		self.__confsets = {v: [] for v in X} # order matters
		
	def __confvars(self, A, inconsistents, confset, curvar):
		'''Decides which variables can be added to the conflict set.
		
		This is a mathematical function.'''
		confvars = []
		for var in A:
			if not var in confvars:
				continue
			if var == curvar:
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
		
		D1 -> R1 -> TH1 -> L1 (if failes due to TH1 and D1)
		
		confset[L1] = [D1, TH1] so that jump happens to TH1 not D1
		
		Jumping must happen to the near past not distant past.
		
		Why would we repeat a long history? Why not jump to yesterday and
		make a tiny difference and quicky proceed to today?
		
		If we jumped to the last year instead, we would have to to live a
		full year again to see if that solves the issue or not!
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
				
	def __retreat(self, curvar, confsets, ac):
		'''Decides to backjump or backtrack in case an assignment fails.
		
		This is a mathematical function.'''
		if self.__csp.assigned_count() == 0:
			return (SEARCH_SPACE_EXHAUSTED, None)
		if curvar in self.__confsets:
			jump_target = self.__confsets[curvar][-1]
			confset = self.__confsets[curvar]
			return (BACKJUMP, confset, jump_target)
		return (BACKTRACK, None)
							
	def __assign(self, curvar, value):
		'''Tries assigning curvar: value.
		
		If the assignment would cause coontradiction, a conflict set is
		returned.
		
		Note: If the contradiction occurs due to indirect consistency
		maintenance, no conflict set is returned. In fact, only curvar
		is responsible for this inconsistency.'''
		dir_res = self.mac.direct(curvar, value)
		self.asmnt.assign(curvar, value)
		if dir_res[0] == CONTRADICTION:
			return (INCONSISTENT_ASSIGNMENT, dir_res[1])
		if dir_res[0] == DOMAINS_REDUCED:
			indir_res = self.mac.indirect(dir_res[1])
			if indir_res[0] == CONTRADICTION:
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
		if self.__csp.unassigned_count() == 0: # solution
			return (SOLUTION, None)
		curvar = self.__select.nextvar()
		domain = copy.deepcopy(self.__csp.get_domain(curvar))
		offset = 0
		while True:
			(val, offset) = self.__select.nextval(curvar, domain, offset)				
			if val == DOMAIN_EXHAUSTED:
				ac = self.__csp.assigned_count()
				return self.__retreat(curvar, self.__confsets, ac)
			self.__csp.backup_domains()
			assign_res = self.__assign(curvar, val)
			if assign_res[0] == INCONSISTENT_ASSIGNMENT:
				self.__accumulate(curvar, assign_res[1])
				self.__csp.unassign(curvar)
				self.__csp.revert_domains()
				continue
			dfs_res = self.dfs()
			self.__csp.unassign(curvar)
			self.__csp.revert_domains()
			if dfs_res[0] in {SOLUTION, SEARCH_SPACE_EXHAUSTED}:
				return dfs_res[0]
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
		unary = UNARY()
		unary.unarify(self.__csp, catalog, spec)
		res = self.__mac.indirect()
		if res[0] == CONTRADICTION:
			return CONTRADICTION
		return self.__dfs()

def main():
	catalog = CATALOG("measures_of_drained_pieces.csv")
	csp = CSP()
	select = SELECT(csp)
	mac = MAC(csp, catalog)
	solver = SOLVER(csp, select, mac)
	res = solver.find(catalog, specs["C"])
	if res == SOLUTION:
		print(solver.stats)
	else:
		print("No solution", res)
			
if __name__ == "__main__":	
	main()
