from constants import *
import math

class LENDEC_LOWER():
    '''Implements length decrement lower consistency.
    
    Ensures that nodes do not reduce in length beyond 2/3 of their predecessor
    nodes.
    
    The following relations must hold between L2 through L6:
    
    L3 >= 2/3 L2

    L4 >= 2/3 L3

    L5 >= 2/3 L4

    L6 >= 2/3 L5'''

    def establish(self, csp, curvar, value, participants):
        '''Establishes consistency after curvar: value assignment.'''
        Li, Lj = sorted(participants)
        A = csp.get_assignment()
        D = csp.get_domains()
        return self.__revise(csp, Li, Lj, A, D)

    def propagate(self, csp, reduced_vars, participants):
        '''Establishes consistency after reduction of some variables.'''
        Li, Lj = sorted(participants)
        A = csp.get_assignment()
        D = csp.get_domains()
        return self.__revise(csp, Li, Lj, A, D)

    def __revise(self, csp, Li, Lj, A, D):
        '''Canculates new consistent bounds for Lj, if possible.
        
        Or checks the boundaries of Li if Lj is assigned.

        Enforces Lj >= 2/3 Li'''
        if Li in A:
            threshold = math.ceil(2/3 * A[Li])        
        else:
            threshold = math.ceil(2/3 * D[Li]["min"])
        if Lj in A:
            if A[Lj] < threshold:
                return CONTRADICTION
        elif D[Lj]["min"] < threshold:
            if D[Lj]["max"] >= threshold:
                csp.update_domain(Lj, {"min": threshold, "max": D[Lj]["max"]})
                return (MADE_CONSISTENT, {Lj})
            return CONTRADICTION
        return ALREADY_CONSISTENT