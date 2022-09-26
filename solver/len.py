from constants import *
import copy

class LEN():
    '''Makes L variables consistent W.R.T. len constraint.
    
    This is probably the last constraint before a solution can
    be found. It enforces the overall length of the Ney.
    
    At any point, if the sum of lower bounds on L variables
    exceeds the value of "len", then a contradiction is occured.
    '''

    def __init__(self, spec):
        self.__len = spec["len"]
        self.__impact_map = {
            "L1": {"L2", "L3", "L4", "L5", "L6", "L7"},
            "L2": {"L1", "L3", "L4", "L5", "L6", "L7"},
            "L3": {"L1", "L2", "L4", "L5", "L6", "L7"},
            "L4": {"L1", "L2", "L3", "L5", "L6", "L7"},
            "L5": {"L1", "L2", "L3", "L4", "L6", "L7"},
            "L6": {"L1", "L2", "L3", "L4", "L5", "L7"},
            "L7": {"L1", "L2", "L3", "L4", "L5", "L6"}
        }
    
    def establish(self, csp, curvar, value):
        '''Establishes len domain consistency.

        w.r.t. the assignment curvar: value.'''
        A = csp.get_assignment()
        ims = self.__impactables(A, curvar, self.__impact_map)
        if len(ims) == 0:
            return (DOMAINS_INTACT, set([]))
        D = csp.get_domains()
        lowers = self.__lowers(A, D, curvar, value)
        uppers = self.__uppers(A, D, curvar, value)
        _len = self.__len
        new_domains = self.__new_domains(D, lowers, uppers, ims, _len)
        return self.__update(csp, new_domains, ims)

    def propagate(self, csp, reduced_vars):
        '''Maintains bounds consistency for hole6 due to propagation.'''
        A = csp.get_assignment()
        ims = set([])
        for reduced_var in reduced_vars:
            _ims = self.__impactables(A, reduced_var, self.__impact_map)
            ims.update(_ims)
        if len(ims) == 0:
            return (DOMAINS_INTACT, set([]))
        D = csp.get_domains()
        lowers = self.__lowers(A, D)
        uppers = self.__uppers(A, D)
        _len = self.__len
        if self.__bounds_contradiction(lowers, uppers, ims, _len):
            return (CONTRADICTION, ims)
        new_domains = self.__new_domains(D, lowers, uppers, ims, _len)
        return self.__update(csp, new_domains, ims)

    def __lowers(self, A, D, curvar=None, value=None):
        '''A mathematical function.'''
        lowers = {}
        for var in {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}:
            if var in A:
                lowers[var] = A[var]
            else:
                lowers[var] = D[var]["min"]
        if curvar != None:
            lowers[curvar] = value
        return lowers

    def __uppers(self, A, D, curvar=None, value=None):
        '''A mathematical function.'''
        uppers = {}
        for var in {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}:
            if var in A:
                uppers[var] = A[var]
            else:
                uppers[var] = D[var]["max"]
        if curvar != None:
            uppers[curvar] = value
        return uppers

    def __impactables(self, A, curvar, imap):
        '''Returns the variables that could be reduced.
        
        A mathematical function.'''
        ims = set([])
        for var in imap[curvar]:
            if not var in A:
                ims.add(var)
        return ims
    
    def __bounds_contradiction(self, lows, ups, ims, _len):
        '''Checks if contradiction due to bounds has occured.

            Contradiction means a bound is not consistent and cannot change.

            max_L1 < len - max_L2 - max_L3 - max_L4 - max_L5 - max_L6 - max_L7
            
            min_L1 > len - min_L2 - min_L3 - min_L4 - min_L5 - min_L6 - min_L7'''
        max_sum = 0
        min_sum = 0
        for var, low in lows.items():
            min_sum += low
        for var, up in ups.items():
            max_sum += up
        for var in ims:
            if ups[var] < _len - (max_sum - ups[var]):
                return True
            if lows[var] > _len - (min_sum - lows[var]):
                return True
        return False
        
    def __new_domains(self, D, lows, ups, ims, _len):
        '''Makes domains consistent if possible.

        min_L1 = len - max_L2 - max_L3 - max_L4 - max_L5 - max_L6 - max_L7
        max_L1 = len - min_L2 - min_L3 - min_L4 - min_L5 - min_L6 - min_L7

        This is a mathematical function.'''
        max_sum = 0
        min_sum = 0
        for var, low in lows.items():
            min_sum += low
        for var, up in ups.items():
            max_sum += up
        new_domains = {}
        for var in {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}:
            if var in ims:
                new_domains[var] = copy.deepcopy(D[var])
                new_upper = _len - (min_sum - lows[var])
                new_lower = _len - (max_sum - ups[var])
                if new_upper > D[var]["max"] or new_lower > D[var]["min"]:
                    return CONTRADICTION
                if new_upper < D[var]["max"]:
                    new_domains[var]["max"] = new_upper
                if new_lower > D[var]["min"]:
                    new_domains[var]["min"] = new_lower
                if new_domains[var] == copy.deepcopy(D[var]):
                    del new_domains[var]
        return new_domains

    def __update(self, csp, new_domains, ims):
        '''Carries out the final domain updates.'''
        if new_domains == CONTRADICTION:
            return (CONTRADICTION, ims)
        elif len(new_domains) > 0:
            for var, new_domain in new_domains.items():
                csp.update_domain(var, new_domain)
            return (DOMAINS_REDUCED, ims, set(new_domains.keys()))
        else:
            return (DOMAINS_INTACT, ims)