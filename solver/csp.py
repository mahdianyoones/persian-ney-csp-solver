import copy, random

class CSP():
    '''Encodes a CSP problem, encapculating operations on varialbes,
    domains, values, and constraints.'''

    def __init__(self, S=1, X=None, C=None):
        '''Initiates an intial CSP problem.
        
        S is the number of solutions required.
        X and C are possible to pass for test.'''
        if X == None and C == None:
            self.__init_main_csp(S)
        else:
            self.__X = X
            self.__C = C
        self.__D = {}
        self.__domains_backups = [] # order matters
        self.__assignment = {}
        self.__unassigned = copy.copy(self.__X)
        self.__assigned = [] # order matters

    def __init_main_csp(self, S):
        '''Creates variables and constraints on them.
        
        S is the number of solutions required.
        e.g. if S = 2, two sets of variables are created (2*14 = 28 vars).'''
        self.__X = set([])
        self.__C = {}
        for i in range(0, S):
            self.__X.update({"L"+str(i*7+j) for j in range(1, 8)})
            self.__X.update({"P"+str(i*7+j) for j in range(1, 8)})
            self.__C["samethick_"+str(i)] = {"P"+str(i*7+j) for j in range(1, 8)}
            self.__C["sameround_"+str(i)] = {"P"+str(i*7+j) for j in range(1, 8)}
            self.__C["len_"+str(i)] = {"L"+str(i*7+j) for j in range(1, 8)}
            self.__C["hole6_"+str(i)] = {"L"+str(i*7+j) for j in range(1, 6)}
            self.__C["hole3_"+str(i)] = {"L"+str(i*7+j) for j in range(1, 5)}
            self.__C["hole1_"+str(i)] = {"L"+str(i*7+j) for j in range(1, 4)}
            self.__C["half_"+str(i)] = {"L"+str(i*7+1), "L"+str(i*7+2)}
            self.__C["diamdec1-2_"+str(i)] = {"P"+str(i*7+1), "P"+str(i*7+2)}
            self.__C["diamdec2-3_"+str(i)] = {"P"+str(i*7+2), "P"+str(i*7+3)}
            self.__C["diamdec3-4_"+str(i)] = {"P"+str(i*7+3), "P"+str(i*7+4)}
            self.__C["diamdec4-5_"+str(i)] = {"P"+str(i*7+4), "P"+str(i*7+5)}
            self.__C["diamdec5-6_"+str(i)] = {"P"+str(i*7+5), "P"+str(i*7+6)}
            self.__C["diamdec6-7_"+str(i)] = {"P"+str(i*7+7), "P"+str(i*7+7)}
            self.__C["lendec2-3_"+str(i)] = {"L"+str(i*7+2), "L"+str(i*7+3)}
            self.__C["lendec3-4_"+str(i)] = {"L"+str(i*7+3), "L"+str(i*7+4)}
            self.__C["lendec4-5_"+str(i)] = {"L"+str(i*7+4), "L"+str(i*7+5)}
            self.__C["lendec5-6_"+str(i)] = {"L"+str(i*7+5), "L"+str(i*7+6)}
            self.__C["lendec6-7_"+str(i)] = {"L"+str(i*7+6), "L"+str(i*7+7)}
            self.__C["lendeclower2-3_"+str(i)] = {"L"+str(i*7+2), "L"+str(i*7+3)}
            self.__C["lendeclower3-4_"+str(i)] = {"L"+str(i*7+3), "L"+str(i*7+4)}
            self.__C["lendeclower4-5_"+str(i)] = {"L"+str(i*7+4), "L"+str(i*7+5)}
            self.__C["lendeclower5-6_"+str(i)] = {"L"+str(i*7+5), "L"+str(i*7+6)}
            self.__C["piecemin1_"+str(i)] = {"P"+str(i*7+1), "L"+str(i*7+1)}
            self.__C["piecemin2_"+str(i)] = {"P"+str(i*7+2), "L"+str(i*7+2)}
            self.__C["piecemin3_"+str(i)] = {"P"+str(i*7+3), "L"+str(i*7+3)}
            self.__C["piecemin4_"+str(i)] = {"P"+str(i*7+4), "L"+str(i*7+4)}
            self.__C["piecemin5_"+str(i)] = {"P"+str(i*7+5), "L"+str(i*7+5)}
            self.__C["piecemin6_"+str(i)] = {"P"+str(i*7+6), "L"+str(i*7+6)}
            self.__C["piecemin7_"+str(i)] = {"P"+str(i*7+7), "L"+str(i*7+7)}
            self.__C["nodemax1_"+str(i)] = {"P"+str(i*7+1), "L"+str(i*7+1)}
            self.__C["nodemax2_"+str(i)] = {"P"+str(i*7+2), "L"+str(i*7+2)}
            self.__C["nodemax3_"+str(i)] = {"P"+str(i*7+3), "L"+str(i*7+3)}
            self.__C["nodemax4_"+str(i)] = {"P"+str(i*7+4), "L"+str(i*7+4)}
            self.__C["nodemax5_"+str(i)] = {"P"+str(i*7+5), "L"+str(i*7+5)}
            self.__C["nodemax6_"+str(i)] = {"P"+str(i*7+6), "L"+str(i*7+6)}
            self.__C["nodemax7_"+str(i)] = {"P"+str(i*7+7), "L"+str(i*7+7)}

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
            if int(var[1:]) % 7 == 2: # i.e. L2, L9, L16, & so on
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