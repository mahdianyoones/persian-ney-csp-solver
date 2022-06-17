from ney_spec import spec
from csp import CSP
from assignment import assignment

FAILURE = False
SUCCESS = True

class Solver():
	def __init__(self, csvfile, spec):
		self.catalog = catalog(csvfile)
		self.spec = spec
		self.csp = CSP(self.catalog, self.spec)
		self.confset = {}
		self.consistency = consistency(self.csp, self.assignment, self.confset)
		for var in self.csp.X:
			self.confset[var] = [] # order matters

	def getSolution(self):
		return self.assignment.getAssignment()
		
	def backtrack_search(self):
		self.assignment = assignment(self.csp)
		return self.backtrack
	
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
		assigned = self.assignment.getAssigned() # time sorted
		for cfv in [var in assigned if var in confset and var != curvar]:
			if not cfv in self.confset[curvar]: # prevent duplicates
				self.confset[curvar].append(cfv)

	def absorb_confset(self, curvar, futureVar):
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
		future_confset = self.confset[futureVar]
		for f_confset in [v for v in future_confset if v !=curvar]:
			if not f_confset in self.confset[curvar]:
				self.confset[curvar].append(f_confset) # order matters
	
	def learnC(self, assignment, confset, curvar):
		'''Adds new constraints or new values to learned constraints.'''
		assigned = assignment.getAssigned() # order matters
		confvars = [var for var in assigned if var in confset and var != curvar]
		constraint = ""
		for confvar in confvars:
			constraint += confvar
		if not constraint in self.C:
			self.C[constraint] = confvars
			self.R[constraint] = set([])
		asmnt = assignment.getAssignment()
		no_good = [(var, asmnt[var]) for var in assigned if var in confvars]
		no_good = tuple(no_good)
		self.R[constraint].add(no_good)
		self.learnC.add(tuple(confvars))
	
	def backtrack(self):
		if self.assignment.isComplete():
			return (SUCCESS, None)
		curvar = self.select_var()
		D = self.csp.varDomain(curvar) # D is never empty here
		value = None
		offset = 0
		while True:
			offset += 1
			if curvar[1] == "L":
				if offset > D["max"] - D["min"]:
					break # domain exhausted	
				else:
					value = D["min"] + offset
			else:
				if offset > len(D):
					break # domain exhausted
				else:
					value = D[offset]
			cresult = self.consistency.make(curvar, value)
			if cresult[0] == FAILURE:				# Future would fail if tried.
				self.accum_confset(curvar, cresult[1])
				self.csp.learnC(self.assignment, cresult[1], curvar)
				continue
			self.assignment.assign(curvar, value)
			result = self.backtrack()
			if result[0] == SUCCESS:					# Future succeeded
				return result						
			self.assignment.unassign(curvar)
			if result[1] == None:
				continue							# backtracked to curvar
			if result[1] == curvar:
				self.absorb_confset(curvar, result[2])	# backjumped to curvar
				continue
			else:
				return result						# backjumped over curvar
		# domain exhausted
		confset = self.assignment.getAssigned()
		self.csp.learnC(self.assignment, confset, curvar)
		if len(self.confset[curvar]) > 0:
			return (FAILURE, self.confset[curvar][-1], curvar) # do jumpback
		return (FAILURE, None) # do backtrack
					
	def select_var(self):
		'''Selects a variable using MRV‌ and degree heurisitcs.'''
		mrv = float("inf")
		mrv_var = None
		degree = ["L2", "L1", "L3", "L4", "L5", "L6", "L7", 
			"D1", "D2", "D3", "D4", "D5", "D6", "D7",
			"R1", "R2", "R3", "R4", "R5", "R6", "R7", 
			"TH1", "TH2", "TH3", "TH4", "TH5", "TH6", "TH7"]
		unassignedVars = self.asssignment.getUnassigned()
		for var in [dsv for dsv in degree if dsv in unassignedVars]:
			Dsize = csp.Dsize(var)
			if Dsize < mrv:
				mrv_var = var
				mrv = Dsize
		return mrv_var

solver = Solver("measures_of_drained_pieces.csv")
result = solver.backtrack_search()
if result[0] == SUCCESS:
	print("Found a solution: ", solver.getSolution())
else:
	print("Failed. No solution has been found!")
