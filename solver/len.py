from os import confstr
from constants import *
import copy

class LEN():
    '''Implements len consistency.
    
    This is probably the last constraint before a solution can be found. It
    enforces the overall length of the Ney.
    
    Formally, it enforces L1 + L2 + L3 + L4 + L5 + L6 + L7 = len.'''

    def __init__(self, len):
        self.__len = len
    
    def establish(self, csp, curvar, value):
        '''Establishes consistency after curvar: value.
        
        Consistency is possible only when at least 6 variables are assigned.'''
        A = csp.get_assignment()
        D = csp.get_domains()
        unassigned = None
        confset = set([])
        assigned_sum = 0
        _len = self.__len
        for v in {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}:
            if not v in A:
                if unassigned != None: # more than two vars are unassigned
                    return self.__examine_bounds(D, A, _len)
                unassigned = v
            else:
                assigned_sum += A[v]
                confset.add(v)
        new_val = _len - assigned_sum
        if new_val > D[unassigned]["max"] or new_val < D[unassigned]["min"]:
            return (CONTRADICTION, {unassigned}, confset)
        if new_val < D[unassigned]["max"] or new_val > D[unassigned]["min"]:
            csp.update_domain(unassigned, {"min": new_val, "max": new_val})
            return (DOMAIN_REDUCED, {unassigned}, {unassigned})

    def propagate(self, csp, reduced_vars):
        '''Establishes consistency after reduction of reduced_vars.
        
        In practice, it only checks if contradiction has occured or not.'''
        A = csp.get_assignment()
        D = csp.get_domains()
        _len = self.__len
        return self.__examine_bounds(D, A, _len)

    def __examine_bounds(self, D, A, _len):
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
        for v in {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}:
            if v in A:
                ups_sum += A[v]
                lows_sum += A[v]
                confset.add(v)
            else:
                ups_sum += D[v]["max"]
                lows_sum += D[v]["min"]
                examined.add(v)
        if ups_sum < _len or lows_sum > _len:
            return (CONTRADICTION, examined, confset)
        return (DOMAINS_INTACT, examined)