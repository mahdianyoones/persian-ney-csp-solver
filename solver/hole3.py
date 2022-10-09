from constants import *
import copy

class HOLE3():
    '''Implements hole3 constraint.
    
    The goal is to ensure that hole 3 falls on node 5.

    The following relation must exist between variables.

    L1 + L2 + L3 + L4 + hole_margin < h3.

    From which we can define the upper bounds for L1, L2, L3, and L4 as such:
    
    1) L1_max < h3 - L2_min - L3_min - L4_min - hole_margin
    2) L2_max < h3 - L1_min - L3_min - L4_min - hole_margin
    3) L3_max < h3 - L1_min - L2_min - L4_min - hole_margin
    4) L4_max < h3 - L1_min - L2_min - L3_min - hole_margin

    Also, we can detect contradiction from their lower bounds. That is:
    
    L1_min + L2_min + L3_min + L4_min + hole_margin >= h3.
    
    In this case, consistency is impossible, since the lower bounds cannot
    be reduced.'''

    def __init__(self, spec):
        self.__h = spec["h3"]
        self.__space = spec["hmarg"]
        self.__impact_map = {
            "L1": {"L2", "L3", "L4"},
            "L2": {"L1", "L3", "L4"},
            "L3": {"L1", "L2", "L4"},
            "L4": {"L1", "L2", "L3"}		
        }

    def establish(self, csp, curvar, value):
        '''Establishes consistency after the assignment curvar: value.'''
        A = csp.get_assignment()
        ims = self.__impactables(A, curvar, self.__impact_map)
        if len(ims) == 0:
            return (DOMAINS_INTACT, set([]))
        D = csp.get_domains()
        lowers = self.__lowers(A, D, curvar, value)
        h = self.__h
        s = self.__space
        new_domains = self.__new_domains(D, lowers, ims, h, s)		
        return self.__update(csp, new_domains, ims)

    def propagate(self, csp, reduced_vars):
        '''Establishes consistency after reduction of some variables.'''
        A = csp.get_assignment()
        ims = set([])
        for reduced_var in reduced_vars:
            _ims = self.__impactables(A, reduced_var, self.__impact_map)
            ims.update(_ims)
        if len(ims) == 0:
            return (DOMAINS_INTACT, set([]))
        D = csp.get_domains()
        lowers = self.__lowers(A, D)
        h = self.__h
        s = self.__space
        if self.__contradiction(lowers, h, s):
            return (CONTRADICTION, ims, set([]))
        new_domains = self.__new_domains(D, lowers, ims, h, s)
        return self.__update(csp, new_domains, ims)
    
    def __contradiction(self, lows, h, s):
        '''Detects contradiction'''
        if lows["L1"] + lows["L2"] + lows["L3"] + lows["L4"] + s >= h:
            return True
        return False
            
    def __lowers(self, A, D, curvar=None, value=None):
        '''Defines what variables could reduce due to assignment to curvar.'''
        lowers = {}
        for var in {"L1", "L2", "L3", "L4"}:
            if var in A:
                lowers[var] = A[var]
            else:
                lowers[var] = D[var]["min"]
        if curvar != None:
            lowers[curvar] = value
        return lowers
        
    def __impactables(self, A, curvar, imap):
        '''A mathematical function.'''
        ims = set([])
        for var in imap[curvar]:
            if not var in A:
                ims.add(var)
        return ims
    
    def __inbounds(self, val, bounds):
         return val >= bounds["min"] and val <= bounds["max"]
     
    def __new_domains(self, D, lows, ims, h, s):
        '''Calculates new consistent bounds.'''
        ups = {}
        if "L1" in ims:
            ups["L1"] = h - lows["L2"] - lows["L3"] - lows["L4"] - s - 1
        if "L2" in ims:
            ups["L2"] = h - lows["L1"] - lows["L3"] - lows["L4"] - s - 1
        if "L3" in ims:
            ups["L3"] = h - lows["L1"] - lows["L2"] - lows["L4"] - s - 1
        if "L4" in ims:
            ups["L4"] = h - lows["L1"] - lows["L2"] - lows["L3"] - s - 1
        new_domains = {}			
        for var, new_upper in ups.items():
            if not self.__inbounds(new_upper, D[var]):
                return CONTRADICTION
            if new_upper < D[var]["max"]:
                new_domain = {"min": D[var]["min"], "max": new_upper}
                new_domains[var] = new_domain
        return new_domains
            
    def __confset(self, csp):
        '''Returns the conflict set.'''
        confset = set([])
        A = csp.get_assignment()
        for v in {"L1", "L2", "L3", "L4"}:
            if v in A:
                confset.add(v)
        return confset

    def __update(self, csp, new_domains, ims):
        '''Carries out the final domain updates.'''
        if new_domains == CONTRADICTION:
            confset = self.__confset(csp)
            return (CONTRADICTION, ims, confset)
        elif len(new_domains) > 0:
            for var, new_domain in new_domains.items():
                csp.update_domain(var, new_domain)
            return (DOMAINS_REDUCED, ims, set(new_domains.keys()))
        else:
            return (DOMAINS_INTACT, ims)