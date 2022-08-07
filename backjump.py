from constants import *

class BACKJUMP():
	'''Is concerned with backtracking and backjumping.
	
	It helps the solver class to make decision on what to do next if
	the domain of current variable is exhausted or a contradiction has
	occured.'''

	def __init__(self, asmnt, conflict):
		self.__asmnt = asmnt
		self.__conflict = conflict
		
	def retreat(self, curvar):
		'''Decides to backjump or backtrack in case an assignment fails.'''
		if self.__asmnt.acount() == 0:
			return (SEARCH_SPACE_EXHAUSTED, None)
		if self.__conflict.has(curvar):
			jump_target = self.__conflict.last(curvar)
			#jump_target = self.conflict.confset[curvar][-1]
			confset = self.__conflict.getset(curvar)
			#confset = self.conflict.confset[curvar]
			return (BACKJUMP, confset, jump_target)
		return (BACKTRACK, None)
