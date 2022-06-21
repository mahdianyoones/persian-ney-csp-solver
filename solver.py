from ney_spec import spec
from csp import CSP
from assignment import ASSIGNMENT
from mac import MAC
from catalog import CATALOG

FAILURE = False
SUCCESS = True
DOMAIN_EXHAUSTED = None

class Solver():
	
	def __init__(self, csvfile, spec):
		'''Instantiates from CSP, MAC, CATALOG, and ASSIGNMENT classes.'''
		self.catalog = CATALOG(csvfile)
		self.spec = spec
		self.csp = CSP(self.catalog, self.spec)
		self.asmnt = ASSIGNMENT(self.csp)		
		self.mac = MAC(self.csp, self.asmnt, self.confset)
		self.confset = {}
		self.learned_cs = set([]) # learned constraints		
		for var in self.csp.X:
			self.confset[var] = [] # order matters

	def getSolution(self):
		return self.asmnt.assignment
			
	def accum_confset(curvar, confset):
		'''Accumulates the conflict set for curvar.
		
		Conflict set must be sorted based on the time of assignment.
		The core notion of a conflict set is to create a time machine where
		order of variables in the set must follow the order of variables in 
		the assignment.
		
		Example:
		
		D1 -> R1 -> TH1 -> L1 (failes due to TH1 and D1)
		
		confset[L1] = [D1, TH1] so that jump happens to TH1 not D1
		
		Jumping must happen to the near past not distant past.
		Why would we repeat a long history? Why not jump to yesterday and
		make a tiny different decision and quicky proceed to today? If we jumped
		to the last year instead, we would have to to live a fully year again to see if
		that solves the issue or not!
		'''
		assigned = self.asmnt.assigned # time sorted
		for cfv in [var in assigned if var in confset and var != curvar]:
			if not cfv in self.confset[curvar]: # prevent duplicates
				self.confset[curvar].append(cfv)

	def absorb_confset(self, curvar, confset):
		'''Absorbs conflict set from jump origin.
		
		Current variable gets the conflict set of the 
		variable that has failed in the future.
		
		This failure in the future happens due to legal assignments at
		some time in the past. Conflict set provides a time machine
		to travel back to the time when people made good moves, but
		future proves it wrong! People may not be able to see the
		effect of their actions far enough because it takes too much time
		to consider every scenario.
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
		if not constraint in self.C:
			self.C[constraint] = confvars
			self.R[constraint] = set([])
		asmnt = self.asmnt.assignment
		no_good = [(var, asmnt[var]) for var in assigned if var in confvars]
		no_good = set(no_good)
		self.R[constraint].add(no_good)
		self.learned_cs.add(tuple(confvars))

	def next_val(self, curvar, D, offset):
		'''Returns the next value in domain of given curvar W.R.T. offset.
		
		This is a utility function.
		'''
		if curvar[1] == "L":
			if offset > D["max"] - D["min"]:
				return DOMAIN_EXHAUSTED
			else:
				return D["min"] + offset
		else:
			if offset > len(D):
				return DOMAIN_EXHAUSTED
			else:
				return D[offset]
		
	def backtrack_search(self):
		'''Runs MAC for all variables first and then calls DFS.
		
		If MAC figures out any contradiction before search begins, no
		solution could ever be found.
		'''
		for var in self.csp.X:
			cresult = self.mac.maintain(var, None)
			if cresult[0] == CONTRADICTION:
				print("Search cannot start. No consistent solution exists")
				return (FAILURE)
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
		if self.asmnt.is_complete():
			return (SUCCESS, None)
		curvar = self.select_var()
		D = self.csp.D[curvar] # Domain of curvar is never empty here
		value = None
		offset = 0
		while True:
			offset += 1
			value = self.next_val(curvar, D, offset)
			# TODO: check if this value violates a learned constraint
			if value == DOMAIN_EXHAUSTED:
				break
			cresult = self.mac.maintain(curvar, value)
			if cresult[0] == FAILURE:				# Future would fail if tried.
				confset = cresult[1]
				self.accum_confset(curvar, confset)
				self.learn_c(curvar, confset)
				continue
			self.asmnt.assign(curvar, value)
			result = self.dfs()						# Go to the future.
			if result[0] == SUCCESS:					# Future was bright.
				return result						
			self.asmnt.unassign(curvar)				# Future failed.
			if result[1] == None:
				continue							# backtracked
			if result[2] == curvar:
				confset = result[1]
				self.absorb_confset(curvar, confset)	# backjumped
				continue							# Try next value
			else:
				return result						# Jumped over curvar
		# domain exhausted
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
		unassigned = self.asmnt.unassign
		for var in [dsv for dsv in degree if dsv in unassigned]:
			if var[1] == "L":
				d_size = self.D[var]["max"] - self.D[var]["min"]
			else:
				d_size = len(self.D[var])
			if d_size < mrv:
				mrv_var = var
				mrv = d_size
		return mrv_var

solver = Solver("measures_of_drained_pieces.csv", spec)
result = solver.backtrack_search()
if result[0] == SUCCESS:
	print("Found a solution: ", solver.asmnt.assignment)
else:
	print("Failed. No solution has been found!")
