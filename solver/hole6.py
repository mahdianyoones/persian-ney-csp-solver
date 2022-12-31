from constants import *
import copy

class HOLE6():
    '''Implements hole6 constraint.
    
    The goal is to ensure that hole 6 falls on node 6.

    The following relation must exist:

    mouthpiece_len + L1 + L2 + L3 + L4 + L5 + hole_margin < h6.
    
    From which we can define the upper bounds for L1, L2, L3, L4, and L5
    as such:

    1) L1_max < h6 - L2_min - L3_min - L4_min - L5_min - hole_margin - mouthpiece_len
    2) L2_max < h6 - L1_min - L3_min - L4_min - L5_min - hole_margin - mouthpiece_len
    3) L3_max < h6 - L1_min - L2_min - L4_min - L5_min - hole_margin - mouthpiece_len
    4) L4_max < h6 - L1_min - L2_min - L3_min - L5_min - hole_margin - mouthpiece_len
    5) L5_max < h6 - L1_min - L2_min - L3_min - L4_min - hole_margin - mouthpiece_len
    
    Also, we can detect contradiction from their lower bounds. That is:
    
    mouthpiece_len + L1_min + L2_min + L3_min + L4_min + L5_min + hole_margin >= h6.'''

    def __init__(self, h6, hmarg, mouthpiece_len):
        self.__h = h6
        self.__space = hmarg
        self.__impact_map = {
            "L1": {"L2", "L3", "L4", "L5"},
            "L2": {"L1", "L3", "L4", "L5"},
            "L3": {"L1", "L2", "L4", "L5"},
            "L4": {"L1", "L2", "L3", "L5"},
            "L5": {"L1", "L2", "L3", "L4"},
        }
        self.__mp = mouthpiece_len        

    def establish(self, csp, curvar, value, participants):
        '''Establishes consistency after the assignment curvar: value.'''
        A = csp.get_assignment()
        ims = self.__impactables(A, curvar, self.__impact_map)
        if len(ims) == 0:
            return REVISED_NONE
        D = csp.get_domains()
        lowers = self.__lowers(A, D, curvar, value)
        h = self.__h
        s = self.__space
        new_domains = self.__new_domains(D, lowers, ims, h, s, self.__mp)		
        if new_domains == CONTRADICTION:
            return (CONTRADICTION, self.__failed_set(csp))
        return self.__update(csp, new_domains, ims)

    def propagate(self, csp, reduced_vars, participants):
        '''Establishes consistency after reduction of some variables.'''
        A = csp.get_assignment()
        ims = set([])
        for reduced_var in reduced_vars:
            _ims = self.__impactables(A, reduced_var, self.__impact_map)
            ims.update(_ims)
        if len(ims) == 0:
            return REVISED_NONE
        D = csp.get_domains()
        lowers = self.__lowers(A, D)
        h = self.__h
        s = self.__space
        if self.__contradiction(lowers, h, s, self.__mp):
            return (CONTRADICTION, self.__failed_set(csp))
        new_domains = self.__new_domains(D, lowers, ims, h, s, self.__mp)
        if new_domains == CONTRADICTION:
            return (CONTRADICTION, self.__failed_set(csp))
        return self.__update(csp, new_domains, ims)
    
    def __contradiction(self, lows, h, s, mp):
        '''Detects contradiction'''
        if mp + lows["L1"]+lows["L2"]+lows["L3"]+lows["L4"]+lows["L5"] + s >= h:
            return True
        return False
            
    def __lowers(self, A, D, curvar=None, value=None):
        '''Returns lower bounds of domains.
        
        If a variable is asssigned, its assigned values is returned instead.'''
        lowers = {}
        for var in {"L1", "L2", "L3", "L4", "L5"}:
            if var in A:
                lowers[var] = A[var]
            else:
                lowers[var] = D[var]["min"]
        if curvar != None:
            lowers[curvar] = value
        return lowers
        
    def __failed_set(self, csp):
        '''Returns the failed set.'''
        members = {"L1", "L2", "L3", "L4", "L5"}
        unassigned = csp.get_unassigned_vars()
        return members.intersection(unassigned)

    def __impactables(self, A, curvar, imap):
        '''Defines what variables could reduce due to assignment to curvar.'''
        ims = set([])
        for var in imap[curvar]:
            if not var in A:
                ims.add(var)
        return ims
         
    def __new_domains(self, D, lows, ims, h, s, mp):
        '''Calculates new consistent bounds.'''
        ups = {}
        if "L1" in ims:
            ups["L1"] = h-mp-lows["L2"]-lows["L3"]-lows["L4"]-lows["L5"]-s-1
        if "L2" in ims:
            ups["L2"] = h-mp-lows["L1"]-lows["L3"]-lows["L4"]-lows["L5"]-s-1
        if "L3" in ims:
            ups["L3"] = h-mp-lows["L1"]-lows["L2"]-lows["L4"]-lows["L5"]-s-1
        if "L4" in ims:
            ups["L4"] = h-mp-lows["L1"]-lows["L2"]-lows["L3"]-lows["L5"]-s-1
        if "L5" in ims:
            ups["L5"] = h-mp-lows["L1"]-lows["L2"]-lows["L3"]-lows["L4"]-s-1
        new_domains = {}			
        for var, new_upper in ups.items():
            if new_upper < D[var]["min"]:
                return CONTRADICTION
            if new_upper < D[var]["max"]:
                new_domain = {"min": D[var]["min"], "max": new_upper}
                new_domains[var] = new_domain
        return new_domains

    def __update(self, csp, new_domains, ims):
        '''Carries out the final domain updates.'''
        if len(new_domains) > 0:
            for var, new_domain in new_domains.items():
                csp.update_domain(var, new_domain)
            return (MADE_CONSISTENT, set(new_domains.keys()))
        return ALREADY_CONSISTENT