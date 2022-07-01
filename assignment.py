from constants import *
from base import BASE

class ASSIGNMENT(BASE):

	def __init__(self, csp):
		self.assignment = {}
		self.unassigned = csp.X.copy()
		self.assigned = [] # order matters
		self.nodes = {}
		for i in [1, 2, 3, 4, 5, 6, 7]:			
			self.nodes[str(i)] = {
				"D": 	FEATURE_IS_NOT_SET, 
				"R": 	FEATURE_IS_NOT_SET, 
				"TH": 	FEATURE_IS_NOT_SET,
				"L": 	FEATURE_IS_NOT_SET
			}
	
	def is_complete(self):
		if len(self.unassigned) == 0:
			return True
		return False
			
	def assign(self, var, val):
		self.assignment[var] = val
		if not var in self.unassigned:
			raise Exception(var, "is not in the unassigned variables.")
		self.unassigned.remove(var)
		self.assigned.append(var) # order matters
		var_i = self.var_i(var)
		var_name = self.var_name(var)
		self.nodes[str(var_i)][var_name] = FEATURE_IS_SET
		
	def unassign(self, var):
		del self.assignment[var]
		self.unassigned.add(var)
		del self.assigned[self.assigned.index(var)]
		var_i = self.var_i(var)
		var_name = self.var_name(var)
		self.nodes[str(var_i)][var_name] = FEATURE_IS_NOT_SET
