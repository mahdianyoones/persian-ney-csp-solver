from constants import *

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

    def __init__(self):
        self.__impact_map = {}

    def __configure_impact_maps(self, csp):
        X = csp.get_variables()
        if self.__impact_map != {} and \
            len(self.__impact_map) >= (len(X) // 7 * 5):
            return
        for i in range(0, 10000000): # arbitrary large number
            L1 = "L"+str(i*7+1)
            if not L1 in X:
                break
            L2 = "L"+str(i*7+2)
            L3 = "L"+str(i*7+3)
            L4 = "L"+str(i*7+4)
            L5 = "L"+str(i*7+5)
            self.__impact_map[L1] = {L2, L3, L4, L5}
            self.__impact_map[L2] = {L1, L3, L4, L5}
            self.__impact_map[L3] = {L1, L2, L4, L5}
            self.__impact_map[L4] = {L1, L2, L3, L5}
            self.__impact_map[L5] = {L1, L2, L3, L4}

    def establish(self, csp, curvar, value, participants, spec):
        '''Establishes consistency after the assignment curvar: value.'''
        A = csp.get_assignment()
        self.__configure_impact_maps(csp)
        ims = self.__impactables(A, curvar, self.__impact_map)
        if len(ims) == 0:
            return REVISED_NONE
        D = csp.get_domains()
        lowers = self.__lowers(A, D, participants, curvar, value)
        h = spec["h6"]
        s = spec["hmarg"]
        mp = spec["mp"]
        new_domains = self.__new_domains(D, lowers, ims, h, s, mp, participants)
        if new_domains == CONTRADICTION:
            return (CONTRADICTION, self.__failed_set(csp, participants))
        return self.__update(csp, new_domains, ims)

    def propagate(self, csp, reduced_vars, participants, spec):
        '''Establishes consistency after reduction of some variables.'''
        A = csp.get_assignment()
        self.__configure_impact_maps(csp)
        ims = set([])
        for reduced_var in reduced_vars:
            _ims = self.__impactables(A, reduced_var, self.__impact_map)
            ims.update(_ims)
        if len(ims) == 0:
            return REVISED_NONE
        D = csp.get_domains()
        lowers = self.__lowers(A, D, participants)
        h = spec["h6"]
        s = spec["hmarg"]
        mp = spec["mp"]
        if self.__contradiction(lowers, h, s, mp, participants):
            return (CONTRADICTION, self.__failed_set(csp, participants))
        new_domains = self.__new_domains(D, lowers, ims, h, s, mp, participants)
        if new_domains == CONTRADICTION:
            return (CONTRADICTION, self.__failed_set(csp, participants))
        return self.__update(csp, new_domains, ims)
    
    def __contradiction(self, lows, h, s, mp, participants):
        '''Detects contradiction'''
        if mp + sum([lows[p] for p in participants]) + s >= h:
            return True
        return False
            
    def __lowers(self, A, D, participants, curvar=None, value=None):
        '''Returns lower bounds of domains.
        
        If a variable is asssigned, its assigned values is returned instead.'''
        lowers = {}
        for var in participants:
            if var in A:
                lowers[var] = A[var]
            else:
                lowers[var] = D[var]["min"]
        if curvar != None:
            lowers[curvar] = value
        return lowers
        
    def __failed_set(self, csp, participants):
        '''Returns the failed set.'''
        unassigned = csp.get_unassigned_vars()
        return participants.intersection(unassigned)

    def __impactables(self, A, curvar, imap):
        '''Defines what variables could reduce due to assignment to curvar.'''
        ims = set([])
        for var in imap[curvar]:
            if not var in A:
                ims.add(var)
        return ims
         
    def __new_domains(self, D, lows, ims, h, s, mp, participants):
        '''Calculates new consistent bounds.'''
        ups = {}
        for p in participants:
            anyofthem = p
            break
        i = (int(anyofthem[1:]) // 7) * 7 + 1
        L1 = "L"+str(i)
        L2 = "L"+str(i+1)
        L3 = "L"+str(i+2)
        L4 = "L"+str(i+3)
        L5 = "L"+str(i+4)
        if L1 in ims:
            ups[L1] = h-mp-lows[L2]-lows[L3]-lows[L4]-lows[L5]-s-1
        if L2 in ims:
            ups[L2] = h-mp-lows[L1]-lows[L3]-lows[L4]-lows[L5]-s-1
        if L3 in ims:
            ups[L3] = h-mp-lows[L1]-lows[L2]-lows[L4]-lows[L5]-s-1
        if L4 in ims:
            ups[L4] = h-mp-lows[L1]-lows[L2]-lows[L3]-lows[L5]-s-1
        if L5 in ims:
            ups[L5] = h-mp-lows[L1]-lows[L2]-lows[L3]-lows[L4]-s-1
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