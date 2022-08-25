import copy
from utils import var_utils
from unary import UNARY

class CSP():

	def __init__(self, catalog, spec):
		self.__catalog = catalog
		self.__spec = spec
		self.__lvars = set([])
		self.__dvars = set([])
		self.__rvars = set([])
		self.__thvars = set([])
		self.__X = set([])
		self.__C = {}
		self.__D = {}
		self.__domains_backup = [] # order matters
		self.__unary()
		self.__assignment = {}
		self.__unassigned = copy.deepcopy(self.__X)
		self.__assigned = [] # order matters
	
	def define_csp(self):
		self.define_variables()
		self.define_constraints()
	
	def define_varialbes(self):
		self.__lvars = {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}
		self.__dvars = {"D1", "D2", "D3", "D4", "D5", "D6", "D7"}
		self.__rvars = {"R1", "R2", "R3", "R4", "R5", "R6", "R7"}
		self.__thvars = {"TH1", "TH2", "TH3", "TH4", "TH5", "TH6", "TH7"}
		self.__X = self.__lvars
		self.__X = self.__X.union(self.__dvars)
		self.__X = self.__X.union(self.__rvars)
		self.__X = self.__X.union(self.__thvars)
	
	def get_rvars(self):
		return self.__rvars
	
	def get_thvars(self):
		return self.__thvars
	
	def get_dvars(self):
		return self.__dvars	
	
	def define_constraints(self):
		self.C["same_th"] = {"TH1", "TH2", "TH3", "TH4", "TH5", "TH6", "TH7"}
		self.C["same_r"] = {"R1", "R2", "R3", "R4", "R5", "R6", "R7"}
		self.C["d_dec"] = {"D1", "D2", "D3", "D4", "D5", "D6", "D7"}
		self.C["in_stock"] = self.d_vars.union(self.th_vars, self.r_vars)
		self.C["l1_half_l2"] = {"L1", "L2"}
		self.C["l_dec"] = {"L2", "L3", "L4", "L5", "L6", "L7"}
		self.C["h1"] = {"L1", "L2", "L3"}
		self.C["h2"] = {"L1", "L2", "L3"}
		self.C["h3"] = {"L1", "L2", "L3", "L4"}
		self.C["h4"] = {"L1", "L2", "L3", "L4"}
		self.C["h5"] = {"L1", "L2", "L3", "L4"}
		self.C["h6"] = {"L1", "L2", "L3", "L4", "L5"}
		self.C["len"] = {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}
		
	def get_spec(self, key):
		return self.__spec[key]
	
	def get_node(self, i):
		return self.__nodes[i]
		
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
	
	def unall(self):
		self.assignment = {}
		self.unassigned = copy.deepcopy(self.csp.X)
		self.assigned = [] # order matters
	
	def get_variables(self):
		return self.__X
	
	def get_lvars(self):
		return self.__lvars
	
	def get_constraints(self):
		return self.__C
	
	def get_domains(self):
		return self.__D
	
	def get_domain(self, var):
		return self.__D[var]
	
	def get_participants(self, constraint):
		return self.__C[constraint]
	
	def unassign(self, var):
		del self.assignment[var]
		self.unassigned.add(var)
		del self.assigned[self.assigned.index(var)]
