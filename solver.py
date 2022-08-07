from ney_spec import specs
from csp import CSP
from assignment import ASSIGNMENT
from mac import MAC
from catalog import CATALOG
from _select import SELECT
from constants import *
import copy
from log import LOG
from conflict import CONFLICT
from backjump import BACKJUMP

class SOLVER():

	def statkeys(self):
		keys = {"assigns", "jumpovers", "direct_contradictions",
			   "backtracks", "nodes", "backjumps", 
			   "indirect_contradictions"}
		return keys

	def __init__(self, csvfile, kook, spec):
		self.__catalog = CATALOG(csvfile)
		self.__spec = spec
		self.__csp = CSP(self.catalog, self.spec)	
		self.__asmnt = ASSIGNMENT(self.csp)
		self.__conflict = CONFLICT(self.asmnt, self.csp)
		self.__backjump = BACKJUMP(asmnt, self.conflict)
		self.__select = SELECT(self.csp, self.asmnt)		
		self.__mac = MAC(self.csp, self.asmnt)
		self.__kook = kook
		self.__stats = {statkey: 0 for statkey in self.statkeys()}
		self.__l = LOG(self.csp, self.asmnt)

	def __value(self, curvar, domain, offset):
		'''Returns the next value in the domain curvar W.R.T. offset.
		
		This is a utility function.
		'''		
		if curvar[0] == "L":
			if offset > domain["max"] - domain["min"]:
				value = DOMAIN_EXHAUSTED
			else:
				value = domain["min"] + offset
		else:
			value = DOMAIN_EXHAUSTED if len(domain) == 0 else domain.pop()
		offset += 2 if curvar == "L2" else 1
		return (value, offset)
		
	def find(self):
		'''Runs MAC for all variables first and then calls DFS.
		
		If MAC figures out any contradiction before search begins, no
		solution could ever be found.
		'''
		res = self.mac.indirect()
		if res[0] == CONTRADICTION:
			return CONTRADICTION
		return self.dfs()
	
	def __assign(self, curvar, value):
		'''Tries assigning curvar: value.
		
		If the assignment would cause coontradiction, a conflict set is
		returned.
		
		Note: If the contradiction occurs due to indirect consistency
		maintenance, no conflict set is returned. In fact, only curvar
		is responsible for this inconsistency.'''
		dir_res = self.mac.direct(curvar, value)
		self.asmnt.assign(curvar, value)
		self.stats["assigns"] += 1
		if dir_res[0] == CONTRADICTION:
			self.stats["direct_contradictions"] += 1
			self.l.contradiction("direct", dir_res, curvar, value)
			return (INCONSISTENT_ASSIGNMENT, dir_res[1])
		if dir_res[0] == DOMAINS_REDUCED:
			indir_res = self.mac.indirect(dir_res[1])
			if indir_res[0] == CONTRADICTION:
				self.stats["indirect_contradictions"] += 1
				self.l.contradiction("indirect", indir_res, curvar, value)
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
		self.stats["nodes"] += 1
		if len(self.asmnt.unassigned) == 0: # solution
			self.l.solution(self.stats, self.kook, self.spec)
			return (SOLUTION, None)
		curvar = self.select.next()
		domain = copy.deepcopy(self.csp.D[curvar])
		offset = 0
		while True:
			(value, offset) = self.value(curvar, domain, offset)				
			if value == DOMAIN_EXHAUSTED:
				return self.backjump.retreat(curvar)
			dback = copy.deepcopy(self.csp.D)
			assign_res = self.assign(curvar, value)
			if assign_res[0] == INCONSISTENT_ASSIGNMENT:
				self.conflict.accumulate(curvar, assign_res[1])
				self.asmnt.unassign(curvar)
				self.csp.D = copy.deepcopy(dback)
				continue
			dfs_res = self.dfs()
			self.asmnt.unassign(curvar)
			self.csp.D = copy.deepcopy(dback)
			if dfs_res[0] in {SOLUTION, SEARCH_SPACE_EXHAUSTED}:
				return dfs_res[0]
			if dfs_res[0] == BACKTRACK:
				self.stats["backtracks"] += 1
				continue
			if dfs_res[0] == BACKJUMP:
				if dfs_res[2] != curvar:
					self.stats["jumpovers"] += 1
					return dfs_res
				else:
					self.conflict.absorb(curvar, dfs_res[1])
					self.stats["backjumps"] += 1
					continue

for kook, spec in specs.items():
	solver = SOLVER("measures_of_drained_pieces.csv", kook, spec)
	res = solver.find()
	if res == SOLUTION:
		print(solver.stats)
		print(solver.asmnt.assignment)
	else:
		print("No solution", res)
