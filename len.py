from constants import *

class LEN():
    '''Implements len consistency.
    
    This is probably the last constraint before a solution can be found. It
    enforces the overall length of the Ney.
    
    Formally, it enforces L1 + L2 + L3 + L4 + L5 + L6 + L7 = len.'''
    
    def establish(self, csp, curvar, value, participants, spec):
        '''Establishes consistency after curvar: value.
        
        Consistency is possible only when at exactly 6 variables are assigned.
        Contradiction, however, can be detected by examining variables bounds
        at any time.'''
        A = csp.get_assignment()
        D = csp.get_domains()
        unassigned = None
        assigned_members = set([])
        assigned_sum = 0
        _len = spec["len"] - spec["mp"]
        for v in participants:
            if v in A:
                assigned_members.add(v)
                assigned_sum += A[v]
            else:
                unassigned = v
        if len(assigned_members) == 7:
            return REVISED_NONE
        if len(assigned_members) < 6:
            return self.__examine_bounds(csp, D, A, _len, participants)                
        new_val = _len - assigned_sum
        if new_val > D[unassigned]["max"] or new_val < D[unassigned]["min"]:
            return (CONTRADICTION, {unassigned})
        if new_val < D[unassigned]["max"] or new_val > D[unassigned]["min"]:
            csp.update_domain(unassigned, {"min": new_val, "max": new_val})
            return (MADE_CONSISTENT, {unassigned})
        return ALREADY_CONSISTENT
        
    def propagate(self, csp, reduced_vars, participants, spec):
        '''Establishes consistency after reduction of reduced_vars.
        
        In practice, it only checks if contradiction has occured or not.'''
        A = csp.get_assignment()
        D = csp.get_domains()
        _len = spec["len"] - spec["mp"]
        return self.__examine_bounds(csp, D, A, _len, participants)

    def __examine_bounds(self, csp, D, A, _len, participants):
        '''Checks if contradiction due to bounds has occured.

            Contradiction cases:

            1. len > max_L1 + max_L2 + max_L3 + max_L4 + max_L5 + max_L6 + max_L7
            
            2. len < min_L1 + min_L2 + min_L3 + min_L4 + min_L5 + min_L6 + min_L7
            
            In case 1, even if all L vars are assigned the largest value in
            their domains, they will not add up to len; i.e. the sum will be
            smaller than len.
            
            In case 2, even if all L vars are assigned the smallest value in
            their domains, they will not add up to len; i.e. the sum will be
            larger than len.'''
        examined = set([])
        lows_sum = 0
        ups_sum = 0
        confset = set([])
        for v in participants:
            if v in A:
                ups_sum += A[v]
                lows_sum += A[v]
                confset.add(v)
            else:
                ups_sum += D[v]["max"]
                lows_sum += D[v]["min"]
                examined.add(v)
        if ups_sum < _len or lows_sum > _len:
            return (CONTRADICTION, self.__failed_set(csp, participants))
        return ALREADY_CONSISTENT

    def __failed_set(self, csp, participants):
        '''Returns the failed set.'''
        unassigned = csp.get_unassigned_vars()
        return participants.intersection(unassigned)