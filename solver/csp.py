import copy

class CSP():

	def __init__(self, X=None, C=None):
		if X == None and C == None:
			self.__init_main_csp()
		else:
			self.__X = X
			self.__C = C
		self.__D = {}
		self.__domains_backups = [] # order matters
		self.__assignment = {}
		self.__unassigned = copy.deepcopy(self.__X)
		self.__assigned = [] # order matters

	def __init_main_csp(self):
		self.__X = {"L1", "L2", "L3", "L4", "L5", "L6", "L7",
					"P1", "P2", "P3", "P4", "P5", "P6", "P7",
					"D1", "D2", "D3", "D4", "D5", "D6", "D7",
					"R1", "R2", "R3", "R4", "R5", "R6", "R7",
					"T1", "T2", "T3", "T4", "T5", "T6", "T7"}
		self.__C = {
			"samethick":	{"T1", "T2", "T3", "T4", "T5", "T6", "T7"},
			"sameround":	{"R1", "R2", "R3", "R4", "R5", "R6", "R7"},
			"len":	 		{"L1", "L2", "L3", "L4", "L5", "L6", "L7"},
			"hole6":		{"L1", "L2", "L3", "L4", "L5"},
			"hole3":		{"L1", "L2", "L3", "L4"},
			"hole1":		{"L1", "L2", "L3",},
			"half":			{"L1", "L2"}
		}
		for i in range(1, 8):
			participants = {"T"+str(i), "R"+str(i), "D"+str(i), "P"+str(i)}
			self.__C["pstock"+str(i)] = participants
			participants = {"T"+str(i), "R"+str(i), "D"+str(i)}
			self.__C["rstock"+str(i)] = participants
			self.__C["dstock"+str(i)] = participants
			self.__C["tstock"+str(i)] = participants
			participants = {"P"+str(i), "L"+str(i)}
			self.__C["piecemin"+str(i)] = participants
			self.__C["nodemax"+str(i)] = participants
			if i < 7:
				participants = {"D"+str(i), "D"+str(i+1)}
				self.__C["diamdec"+str(i)] = participants
			if i >= 2 and i < 7:
				participants = {"L"+str(i), "L"+str(i+1)}
				self.__C["lendec"+str(i)] = participants
				participants = {"L"+str(i), "L"+str(i+1)}
				self.__C["lendeclower"+str(i)] = participants

	def update_domain(self, var, new_domain):
		self.__D[var] = new_domain
	
	def backup_domains(self):
		self.__domains_backups.append(copy.deepcopy(self.__D))
	
	def revert_domains(self):
		last_D = self.__domains_backups.pop()
		self.__D = copy.deepcopy(last_D)
	
	def get_assignment(self):
		return self.__assignment
	
	def get_assigned_vars(self):
		return self.__assigned

	def get_unassigned_vars(self):
		return self.__unassigned
		
	def assigned_count(self):
		return len(self.__assigned)
	
	def unassigned_count(self):
		return len(self.__unassigned)
		
	def assign(self, var, val):
		self.__assignment[var] = val
		self.__unassigned.remove(var)
		self.__assigned.append(var) # order matters
	
	def unassign_all(self):
		self.__assignment = {}
		self.__unassigned = copy.deepcopy(self.__X)
		self.__assigned = [] # order matters
	
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
		del self.__assignment[var]
		self.__unassigned.add(var)
		del self.__assigned[self.__assigned.index(var)]