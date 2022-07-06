from ney_spec import spec
from csp import CSP
from assignment import ASSIGNMENT
from mac import MAC
from catalog import CATALOG
from constants import *
import copy
from log import logger

class SOLVER():

	def __init__(self, csvfile, spec):
		self.nodes = 0
		self.catalog = CATALOG(csvfile)
		self.spec = spec
		self.csp = CSP(self.catalog, self.spec)
		self.asmnt = ASSIGNMENT(self.csp)		
		self.confset = {}
		self.mac = MAC(self.csp)
		self.learned_cs = {} # learned constraints	
		self.R = {}	
		for var in self.csp.X:
			self.confset[var] = [] # order matters
			
	def accum_confset(self, curvar, confset):
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
		assigned = self.asmnt.assigned # time sorted
		if len(assigned) == 0:
			raise Exception("Confset & empty assignment.", curvar, confset)
		for cfv in [v for v in assigned if v in confset and v != curvar]:
			if not cfv in self.confset[curvar]: # prevent duplicates
				self.confset[curvar].append(cfv)

	def absorb_confset(self, curvar, confset):
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
		for confvar in [v for v in confset if v !=curvar]:
			if not confvar in self.confset[curvar]:
				self.confset[curvar].append(confvar) # order matters

	def learn_c(self, curvar, confset):
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
		assigned = self.asmnt.assigned # order matters
		confvars = [var for var in assigned if var in confset and var != curvar]
		constraint = ""
		for confvar in confvars:
			constraint += confvar
		if not constraint in self.learned_cs:
			self.learned_cs[constraint] = confvars
			self.R[constraint] = set([])
		assignment = self.asmnt.assignment
		no_good = [(var, assignment[var]) for var in assigned if var in confvars]
		self.R[constraint].add(tuple(no_good))

	def next_val(self, curvar, domain, offset):
		'''Returns the next value in the domain curvar W.R.T. offset.
		
		This is a utility function.
		'''
		if curvar[0] == "L":
			if offset > domain["max"] - domain["min"]:
				return DOMAIN_EXHAUSTED
			else:
				return domain["min"] + offset
		else:
			if len(domain) == 0:
				return DOMAIN_EXHAUSTED
			else:
				return domain.pop()
			
	def backtrack_search(self):
		'''Runs MAC for all variables first and then calls DFS.
		
		If MAC figures out any contradiction before search begins, no
		solution could ever be found.
		'''
		dback = copy.deepcopy(self.csp.D)		
		bresult = self.mac.b_update(self.asmnt)
		logger.log3(dback, self.csp.D, self.csp.X, bresult)
		if bresult == CONTRADICTION:
			return (ibresult, set([]))
		return self.dfs()

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
		self.nodes += 1
		if self.nodes > 10000:
			exit()
		if self.asmnt.is_complete():
			return (SUCCESS, None)
		curvar = self.select_var()
		domain = copy.deepcopy(self.csp.D[curvar]) # Domain of curvar is never empty here
		value = None
		offset = 0
		while True:
			value = self.next_val(curvar, domain, offset)
			if curvar == "L2":
				offset += 2
			else:
				offset += 1
			# TODO: check if this value violates a learned constraint
			if value == DOMAIN_EXHAUSTED:
				break
			dback = copy.deepcopy(self.csp.D)
			indir_res = (DOMAINS_INTACT, None)
			dir_res = self.mac.establish(self.asmnt, curvar, value)
			logger.log1(dback, self.csp.D, curvar, value, dir_res)
			confset = dir_res[1]
			self.asmnt.assign(curvar, value)
			if dir_res[0] == DOMAINS_REDUCED:
				dbefore = copy.deepcopy(self.csp.D)		
				indir_res = self.mac.b_update(self.asmnt, dir_res[1])
				logger.log3(dbefore, self.csp.D, dir_res[1], indir_res)				
				confset = indir_res[1]
			if dir_res[0] == CONTRADICTION or indir_res[0] == CONTRADICTION:
				self.accum_confset(curvar, confset)
				self.learn_c(curvar, confset)
				self.csp.D = copy.deepcopy(dback)
				self.asmnt.unassign(curvar)
				continue
			logger.log2(curvar, value, self.asmnt)
			result = self.dfs()						# Try future
			if result[0] == SUCCESS:					# Future would be bright
				return result						
			self.asmnt.unassign(curvar)				# Future failed!
			self.csp.D = copy.deepcopy(dback)
			if result[1] == None:
				continue							# backtracked
			if result[2] == curvar:
				confset = result[1]
				self.absorb_confset(curvar, confset)	# backjumped
				logger.log5(curvar)
				continue							# Try next value
			else:
				logger.log4(curvar, result[2])
				return result						# Jumped over curvar
		# domain exhausted
		logger.log6(curvar)
		confset = self.asmnt.assigned
		self.learn_c(confset, curvar)
		if len(self.confset[curvar]) > 0:
			confset = self.confset[curvar]
			jump_target = self.confset[curvar][-1]
			return (FAILURE, confset, jump_target) 		# do jumpback
		return (FAILURE, None) 						# do backtrack
	
	def select_var(self):
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
result = solver.backtrack_search()
if result[0] == SUCCESS:
	print("Found a solution: ", solver.asmnt.assignment)
	print("Nodes: ", solver.nodes)
else:
	print("No solution has been found!")
	print("Nodes: ", solver.nodes)
