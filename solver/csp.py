import copy

class CSP():

	def __init__(self):
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
			"piece_stock1":	{"T1", "R1", "D1", "P1"},
			"piece_stock2":	{"T2", "R2", "D2", "P2"},
			"piece_stock3":	{"T3", "R3", "D3", "P3"},
			"piece_stock4":	{"T4", "R4", "D4", "P4"},
			"piece_stock5":	{"T5", "R5", "D5", "P5"},
			"piece_stock6":	{"T6", "R6", "D6", "P6"},
			"piece_stock7":	{"T7", "R7", "D7", "P7"},
			"hole1":		{"L1", "L2", "L3",},
			"thick_stock1":	{"T1", "R1", "D1"},
			"thick_stock2":	{"T2", "R2", "D2"},
			"thick_stock3":	{"T3", "R3", "D3"},
			"thick_stock4":	{"T4", "R4", "D4"},
			"thick_stock5":	{"T5", "R5", "D5"},
			"thick_stock6":	{"T6", "R6", "D6"},
			"thick_stock7":	{"T7", "R7", "D7"},
			"diam_stock1":	{"T1", "R1", "D1"},
			"diam_stock2":	{"T2", "R2", "D2"},
			"diam_stock3":	{"T3", "R3", "D3"},
			"diam_stock4":	{"T4", "R4", "D4"},
			"diam_stock5":	{"T5", "R5", "D5"},
			"diam_stock6":	{"T6", "R6", "D6"},
			"diam_stock7":	{"T7", "R7", "D7"},
			"round_stock1":	{"T1", "R1", "D1"},
			"round_stock2":	{"T2", "R2", "D2"},
			"round_stock3":	{"T3", "R3", "D3"},
			"round_stock4":	{"T4", "R4", "D4"},
			"round_stock5":	{"T5", "R5", "D5"},
			"round_stock6":	{"T6", "R6", "D6"},
			"round_stock7":	{"T7", "R7", "D7"},
			"piece_min1":	{"P1", "L1"},
			"piece_min2":	{"P2", "L2"},
			"piece_min3":	{"P3", "L3"},
			"piece_min4":	{"P4", "L4"},
			"piece_min5":	{"P5", "L5"},
			"piece_min6":	{"P6", "L6"},
			"piece_min7":	{"P7", "L7"},
			"node_max1":	{"P1", "L1"},
			"node_max2":	{"P2", "L2"},
			"node_max3":	{"P3", "L3"},
			"node_max4":	{"P4", "L4"},
			"node_max5":	{"P5", "L5"},
			"node_max6":	{"P6", "L6"},
			"node_max7":	{"P7", "L7"},
			"diamdec1":		{"D1", "D2"},
			"diamdec2":		{"D2", "D3"},
			"diamdec3":		{"D3", "D4"},
			"diamdec4":		{"D4", "D5"},
			"diamdec5":		{"D5", "D6"},
			"diamdec6":		{"D6", "D7"},
			"lendec1":		{"L2", "L3"},
			"lendec2":		{"L3", "L4"},
			"lendec3":		{"L4", "L5"},
			"lendec4":		{"L5", "L6"},
			"lendec5":		{"L6", "L7"},
			"lendeclower1":	{"L2", "L3"},
			"lendeclower2":	{"L3", "L4"},
			"lendeclower3":	{"L4", "L5"},
			"lendeclower4":	{"L5", "L6"},
			"lendeclower5":	{"L6", "L7"},
			"half":			{"L1", "L2"},
			"double":		{"L1", "L2"},
		}
		self.__D = {}
		self.__domains_backups = [] # order matters
		self.__assignment = {}
		self.__unassigned = copy.deepcopy(self.__X)
		self.__assigned = [] # order matters		
	
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