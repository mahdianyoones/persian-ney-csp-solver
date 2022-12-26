import copy, random

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
        self.__unassigned = copy.copy(self.__X)
        self.__assigned = [] # order matters

    def __init_main_csp(self):
        self.__X = {"L1", "L2", "L3", "L4", "L5", "L6", "L7",
                    "P1", "P2", "P3", "P4", "P5", "P6", "P7"}
        self.__C = {
            "samethick":	    {"P1", "P2", "P3", "P4", "P5", "P6", "P7"},
            "sameround":	    {"P1", "P2", "P3", "P4", "P5", "P6", "P7"},
            "len":	 		    {"L1", "L2", "L3", "L4", "L5", "L6", "L7"},
            "hole6":		    {"L1", "L2", "L3", "L4", "L5"},
            "hole3":		    {"L1", "L2", "L3", "L4"},
            "hole1":		    {"L1", "L2", "L3",},
            "half":			    {"L1", "L2"},
            "diamdec1-2":       {"P1", "P2"},
            "diamdec2-3":       {"P2", "P3"},
            "diamdec3-4":       {"P3", "P4"},
            "diamdec4-5":       {"P4", "P5"},
            "diamdec5-6":       {"P5", "P6"},
            "diamdec6-7":       {"P6", "P7"},
            "lendec2-3":        {"L2", "L3"},
            "lendec3-4":        {"L3", "L4"},
            "lendec4-5":        {"L4", "L5"},
            "lendec5-6":        {"L5", "L6"},
            "lendec6-7":        {"L6", "L7"},
            "lendeclower2-3":   {"L2", "L3"},
            "lendeclower3-4":   {"L3", "L4"},
            "lendeclower4-5":   {"L4", "L5"},
            "lendeclower5-6":   {"L5", "L6"},
            "piecemin1":        {"P1", "L1"},
            "piecemin2":        {"P2", "L2"},
            "piecemin3":        {"P3", "L3"},
            "piecemin4":        {"P4", "L4"},
            "piecemin5":        {"P5", "L5"},
            "piecemin6":        {"P6", "L6"},
            "piecemin7":        {"P7", "L7"},
            "nodemax1":         {"P1", "L1"},
            "nodemax2":         {"P2", "L2"},
            "nodemax3":         {"P3", "L3"},
            "nodemax4":         {"P4", "L4"},
            "nodemax5":         {"P5", "L5"},
            "nodemax6":         {"P6", "L6"},
            "nodemax7":         {"P7", "L7"},
        }

    def update_domain(self, var, new_domain):
        self.__D[var] = new_domain
    
    def copy_domain(self, domain):
        copied = {}
        for v, vals in domain.items():
            copied[v] = copy.copy(vals)
        return copied

    def backup_domains(self):
        self.__domains_backups.append(self.copy_domain(self.__D))
    
    def revert_domains(self):
        last_D = self.__domains_backups.pop()
        self.__D = last_D
    
    def get_assignment(self):
        return self.__assignment
    
    def get_assigned_vars(self):
        return self.__assigned

    def get_shuffled_values(self, var):
        if var[0] == "L":
            domain = self.get_domain(var)
            lower = int(domain["min"])
            upper = int(domain["max"])
            if var == "L2":
                vals = [v for v in range(lower, upper+2, 2)]
            else:
                vals = [v for v in range(lower, upper+1)]
            random.shuffle(vals)
            return set(vals)
        else:
            vals = copy.copy(self.get_domain(var))
            random.shuffle(list(vals))
            return vals

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