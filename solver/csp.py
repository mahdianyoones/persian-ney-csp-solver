import copy

class CSP():

	def __init__(self):
		self.__X = {	"L1", "L2", "L3", "L4", "L5", "L6", "L7",
					"D1", "D2", "D3", "D4", "D5", "D6", "D7",
					"R1", "R2", "R3", "R4", "R5", "R6", "R7",
					"T1", "T2", "T3", "T4", "T5", "T6", "T7"}
		self.__C = {
			"same_t":	 {"T1", "T2", "T3", "T4", "T5", "T6", "T7"},
			"same_r":  {"R1", "R2", "R3", "R4", "R5", "R6", "R7"},
			"d_dec":	 {"D1", "D2", "D3", "D4", "D5", "D6", "D7"},
			"stock1":  {"T1", "R1", "D1"},
			"stock2":  {"T2", "R2", "D2"},
			"stock3":  {"T3", "R3", "D3"},
			"stock4":  {"T4", "R4", "D4"},
			"stock5":  {"T5", "R5", "D5"},
			"stock6":  {"T6", "R6", "D6"},
			"stock7":  {"T7", "R7", "D7"},
			"half":	 {"L1", "L2"},
			"l_dec":   {"L2", "L3", "L4", "L5", "L6", "L7"},
			"h1":	 {"L1", "L2", "L3"},
			"h2":	 {"L1", "L2", "L3"},
			"h3":	 {"L1", "L2", "L3", "L4"},
			"h4":	 {"L1", "L2", "L3", "L4"},
			"h5":	 {"L1", "L2", "L3", "L4"},
			"h6":	 {"L1", "L2", "L3", "L4", "L5"},
			"len":	 {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}
		}
		self.__D = {}
		self.__domains_backup = [] # order matters
		self.__assignment = {}
		self.__unassigned = copy.deepcopy(self.__X)
		self.__assigned = [] # order matters		
	
	def update_domain(self, var, new_domain):
		self.__D[var] = new_domain
	
	def backup_domains(self):
		self.__domains_backups.append(copy.deepcopy(self.__D))
	
	def revert_domains(self):
		self.__D = copy.deepcopy(self.__domains_backups.pop())
	
	def get_assignment(self):
		return self.__assignment
	
	def assigned_count(self):
		return len(self.__assigned)
	
	def unassigned_count(self):
		return len(self.__unassigned)
		
	def assign(self, var, val):
		self.__assignment[var] = val
		self.__unassigned.remove(var)
		self.__assigned.append(var) # order matters
	
	def unassign_all(self):
		self.assignment = {}
		self.unassigned = copy.deepcopy(self.__X)
		self.assigned = [] # order matters
	
	def get_variables(self):
		return self.__X
	
	def get_constraints(self):
		return self.__C
	
	def get_domains(self):
		return self.__D
	
	def get_domain(self, var):
		return self.__D[var]
	
	def get_neighbors(self, constraint):
		return self.__C[constraint]
	
	def unassign(self, var):
		del self.assignment[var]
		self.unassigned.add(var)
		del self.assigned[self.assigned.index(var)]
