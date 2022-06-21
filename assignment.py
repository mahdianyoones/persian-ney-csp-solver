FEATURE_IS_NOT_SET = False
FEATURE_IS_SET = True
class assignment():
	def __init__(self, csp):
		self.X = csp.getVars()
		self.asmnt = {}
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
		
	def isComplete(self)
		if len(self.unassigned) == 0:
			return True
		return False
		
	def getAssignment(self):
		return self.asmnt
	
	def getAssigned(self):
		return self.assigned
	
	def getUnassigned(self):
		return self.unassigned
		
	def assign(self, var, val):
		self.asmnt[var] = val
		self.unassigned.remove(var)
		self.assigned.append(var) # order matters
		self.nodes[int(var[1])][var[0]] = True
		
	def unassign(self, var):
		del self.asmnt[var]
		self.unassigned.add(var)
		del self.assigned[self.assigned.index(var)]
		self.nodes[int(var[1])][var[0]] = False		
