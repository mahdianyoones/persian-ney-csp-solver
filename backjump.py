from constants import *

class BACKJUMP():
	'''Is concerned with backtracking and backjumping.
	
	It helps the solver class to make decision on what to do next if
	the domain of current variable is exhausted or a contradiction has
	occured.'''

	def __init__(self, asmnt, conflict):
		self.asmnt = asmnt
		self.conflict = conflict
		
	def retreat(self, curvar):
		'''Decides to backjump or backtrack in case an assignment fails.'''
		if len(self.asmnt.assigned) == 0:
			return (SEARCH_SPACE_EXHAUSTED, None)
		if len(self.conflict.confset[curvar]) > 0:
			jump_target = self.conflict.confset[curvar][-1]
			confset = self.conflict.confset[curvar]
			return (BACKJUMP, confset, jump_target)
		return (BACKTRACK, None)
