FEATURE_IS_NOT_SET = False
FEATURE_IS_SET = True
class ASSIGNMENT():
	def __init__(self, csp):
		self.X = csp.getVars()
		self.assignment = {}
		self.unassigned = self.X.copy()
		self.assigned = [] # order matters
		self.nodes = {}
		for i in [1, 2, 3, 4, 5, 6, 7]:			
			self.nodes[i] = {
				"D": 	FEATURE_IS_NOT_SET, 
				"R": 	FEATURE_IS_NOT_SET, 
				"TH": 	FEATURE_IS_NOT_SET, 
				"L": 	FEATURE_IS_NOT_SET
			}
	
	def is_complete(self)
		if len(self.unassigned) == 0:
			return True
		return False
			
	def assign(self, var, val):
		self.assignment[var] = val
		self.unassigned.remove(var)
		self.assigned.append(var) # order matters
		self.nodes[int(var[1])][var[0]] = True
		
	def unassign(self, var):
		del self.assignment[var]
		self.unassigned.add(var)
		del self.assigned[self.assigned.index(var)]
		self.nodes[int(var[1])][var[0]] = False		
