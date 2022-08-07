class CONFLICT():

	def __init__(self, asmnt, csp):
		self.__asmnt = asmnt
		self.__confsets = {v: [] for v in csp.X} # order matters

	def has(self, var):
		pass
		
	def last(self, var):
		pass
		
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
