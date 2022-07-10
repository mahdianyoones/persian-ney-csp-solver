from ney_spec import spec
from csp import CSP
from assignment import ASSIGNMENT
from mac import MAC
from catalog import CATALOG
from constants import *
import copy
from log import LOG

class SOLVER():

	def statkeys(self):
		keys = {"assigns", "jumpovers", "direct_contradictions",
			   "backtracks", "nodes", "backjumps", 
			   "indirect_contradictions"}
		return keys

	def __init__(self, csvfile, spec):
		self.catalog = CATALOG(csvfile)
		self.spec = spec
		self.csp = CSP(self.catalog, self.spec)	
		self.asmnt = ASSIGNMENT(self.csp)			
		self.l = LOG(self.csp, self.asmnt)
		self.mac = MAC(self.csp)
		self.learned = {} 			             # learned constraints	
		self.R = {}				             # tuples for learned consts
		self.confset = {v: [] for v in self.csp.X} # order matters
		self.stats = {statkey: 0 for statkey in self.statkeys()}

	def accumulate(self, curvar, confset):
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
		if len(confset) == 0:
			return
		a = self.asmnt.assigned # time sorted
		for cfv in [v for v in a if v in confset and v != curvar]:
			if not cfv in self.confset[curvar]: # prevent duplicates
				self.confset[curvar].append(cfv)

	def absorb(self, curvar, confset):
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
		for cfv in [v for v in confset if v != curvar]:
			if not cfv in self.confset[curvar]:
				self.confset[curvar].append(cfv) # order matters

	def learn(self, curvar, value, confset):
		'''Adds new constraint or new values to a learned constraint.
		
		Confset contains all variables that participate in a violated
		constraint. The variables that participate in the new constraints
		include all the variables in the conflict set except curvar.
		
		For example, if the conflict set is {D1, TH1, R1}, and curvar = R1,
		we build a new constraint on D1 and TH1 only, since these new 
		learned constraints are to target LEGAL assignments that contradict
		all values of R1.
		
		i.e. an assignment to D1 and TH1 has caused contradiction for R1; 
		hence, we need to prevent this very valid assignment to D1 and TH1
		from ever happening again.
		
		This LEGAL-yet-must-prevented assignment forms a no-good set where
		members are tuples like (D1, value), (TH1, value), ... . No-goods are
		added to the relations (R) for the new constraint.
		'''
		return
		if len(confset) == 0:
			return
		confvars = [v for v in self.asmnt.assigned if v in confset]
		constraint = "".join(confvars)
		if not constraint in self.learned:
			self.stats["learned"] += 1
			self.learned[constraint] = confvars
			self.R[constraint] = set([])
		no_good = []
		for v in confvars:
			if v in self.asmnt.assigned:
				no_good.append((v, self.asmnt.assignment[v]))
			elif v == curvar:
				no_good.append((curvar, value))
		self.R[constraint].add(tuple(no_good))
		self.stats["learned_tuples"] += 1

	def value(self, curvar, domain, offset):
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
		bresult = self.mac.indirect(self.asmnt)
		if bresult[0] == CONTRADICTION:
			print("\n\nSearch stopped!")
			return
		return self.dfs()
	
	def assign(self, curvar, value):
		'''Tries assigning curvar: value.
		
		If the assignment would cause coontradiction, a conflict set is
		returned.'''
		dir_res = self.mac.direct(self.asmnt, curvar, value)
		self.asmnt.assign(curvar, value)
		self.stats["assigns"] += 1
		if dir_res[0] == CONTRADICTION:
			self.stats["direct_contradictions"] += 1
			return (INCONSISTENT_ASSIGNMENT, dir_res[1])
		if dir_res[0] == DOMAINS_REDUCED:
			indir_res = self.mac.indirect(self.asmnt, dir_res[1])
			if indir_res[0] == CONTRADICTION:
				self.stats["indirect_contradictions"] += 1
				return (INCONSISTENT_ASSIGNMENT, indir_res[1])
		return (CONSISTENT_ASSIGNMENT, set([]))
	
	def retreat(self, curvar):
		'''Decides to backjump or backtrack in case an assignment fails.'''
		if len(self.asmnt.assigned) == 0:
			return (SEARCH_SPACE_EXHAUSTED, None)
		if len(self.confset[curvar]) > 0:
			jump_target = self.confset[curvar][-1]
			confset = self.confset[curvar]
			return (BACKJUMP, confset, jump_target)
		return (BACKTRACK, None)				
	
	def dfs(self):
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
			self.l.solution(self.stats)
			return (SOLUTION, None)
		curvar = self.select()
		domain = copy.deepcopy(self.csp.D[curvar])
		offset = 0
		while True:
			(value, offset) = self.value(curvar, domain, offset)				
			if value == DOMAIN_EXHAUSTED:
				return self.retreat(curvar)
			dback = copy.deepcopy(self.csp.D)
			assign_res = self.assign(curvar, value)
			if assign_res[0] == INCONSISTENT_ASSIGNMENT:
				self.accumulate(curvar, assign_res[1])
				self.asmnt.unassign(curvar)
				self.csp.D = copy.deepcopy(dback)
				continue
			dfs_res = self.dfs()
			self.asmnt.unassign(curvar)
			self.csp.D = copy.deepcopy(dback)
			if dfs_res[0] == SOLUTION:
				continue
			if dfs_res[0] == SEARCH_SPACE_EXHAUSTED:
				return # termination
			if dfs_res[0] == BACKTRACK:
				self.stats["backtracks"] += 1
				continue
			if dfs_res[0] == BACKJUMP:
				if dfs_res[2] != curvar:
					self.stats["jumpovers"] += 1
					return dfs_res
				else:
					self.absorb(curvar, dfs_res[1])
					self.stats["backjumps"] += 1
					continue

	def select(self):
		'''Selects a variable using MRV‌ and degree heurisitcs.'''
		mrv = float("inf")
		mrv_var = None
		degree = ["L2", "L1", "L3", "L4", "L5", "L6", "L7", 
			"D1", "D2", "D3", "D4", "D5", "D6", "D7",
			"R1", "R2", "R3", "R4", "R5", "R6", "R7", 
			"TH1", "TH2", "TH3", "TH4", "TH5", "TH6", "TH7"]
		unassigned = self.asmnt.unassigned
		for var in [dsv for dsv in degree if dsv in unassigned]:
			if var[0] == "L":
				d_size = self.csp.D[var]["max"] - self.csp.D[var]["min"]
			else:
				d_size = len(self.csp.D[var])
			if d_size < mrv:
				mrv_var = var
				mrv = d_size
		return mrv_var

solver = SOLVER("measures_of_drained_pieces.csv", spec)
print(solver.find())
print(solver.stats)
print(solver.asmnt.assignment)
