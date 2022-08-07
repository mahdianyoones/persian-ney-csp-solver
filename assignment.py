from constants import *
from base import BASE
import copy

class ASSIGNMENT(BASE):

	def __init__(self, csp):
		self.__csp = csp
		self.__assignment = {}
		self.__unassigned = copy.deepcopy(self.csp.X)
		self.__assigned = [] # order matters
		self.__nodes = {}
		for i in [1, 2, 3, 4, 5, 6, 7]:			
			self.__nodes[str(i)] = {
				"D": 	FEATURE_IS_NOT_SET, 
				"R": 	FEATURE_IS_NOT_SET, 
				"TH": 	FEATURE_IS_NOT_SET,
				"L": 	FEATURE_IS_NOT_SET
			}
	
	def assign(self, var, val):
		if var in self.assigned or var in self.assignment:
			raise Exception(var, " is already assigned.")
		self.assignment[var] = val
		self.unassigned.remove(var)
		self.assigned.append(var) # order matters
		var_i = self.var_i(var)
		var_name = self.var_name(var)
		self.nodes[str(var_i)][var_name] = FEATURE_IS_SET
	
	def unall(self):
		self.assignment = {}
		self.unassigned = copy.deepcopy(self.csp.X)
		self.assigned = [] # order matters
		self.nodes = {}
		for i in [1, 2, 3, 4, 5, 6, 7]:			
			self.__nodes[str(i)] = {
				"D": 	FEATURE_IS_NOT_SET, 
				"R": 	FEATURE_IS_NOT_SET, 
				"TH": 	FEATURE_IS_NOT_SET,
				"L": 	FEATURE_IS_NOT_SET
			}
	
	def acount(self):
		pass
	
	def unassign(self, var):
		if var in self.unassigned:
			raise Exception(var, " is already unassigned.")
		del self.assignment[var]
		self.unassigned.add(var)
		del self.assigned[self.assigned.index(var)]
		var_i = self.var_i(var)
		var_name = self.var_name(var)
		self.nodes[str(var_i)][var_name] = FEATURE_IS_NOT_SET
