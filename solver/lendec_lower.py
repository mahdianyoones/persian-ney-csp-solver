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

    def establish(self, csp, curvar, value, participants, spec):
        '''Establishes consistency after curvar: value assignment.'''
        Li, Lj = sorted(participants, key=lambda p: int(p[1:]))      
        A = csp.get_assignment()
        D = csp.get_domains()
        return self.__revise(csp, Li, Lj, A, D)

    def propagate(self, csp, reduced_vars, participants, spec):
        '''Establishes consistency after reduction of some variables.'''
        Li, Lj = sorted(participants)
        A = csp.get_assignment()
        D = csp.get_domains()
        return self.__revise(csp, Li, Lj, A, D)

    def __revise(self, csp, Li, Lj, A, D):
        '''Canculates new consistent bounds for Lj, if possible.
        
        Or checks the boundaries of Li if Lj is assigned.

        Enforces Lj >= 2/3 Li'''
        reduced_vars = set([])
        if Li in A:
            threshold = math.ceil(2/3 * A[Li])
            if threshold > D[Lj]["min"]:
                newDj = {"min": threshold, "max": D[Lj]["max"]}
                csp.update_domain(Lj, newDj)
                reduced_vars.add(Lj)
        elif Lj in A:
            threshold = math.ceil(3/2 * A[Lj])
            if threshold < D[Li]["max"]:
                newDi = {"min": D[Li]["min"], "max": threshold}
                csp.update_domain(Li, newDi)
                reduced_vars.add(Li)
        else:
            threshold = math.ceil(2/3 * D[Li]["min"])
            if threshold > D[Lj]["max"]:
                return (CONTRADICTION, {Li, Lj})
            if threshold > D[Lj]["min"]:
                newDj = {"min": threshold, "max": D[Lj]["max"]}
                reduced_vars.add(Lj)
                csp.update_domain(Lj, newDj)
        if reduced_vars != set([]):
            return (MADE_CONSISTENT, reduced_vars)
        return ALREADY_CONSISTENT

    def __failed_set(self, csp, participants):
        '''Returns the failed set.'''
        unassigned = csp.get_unassigned_vars()
        return participants.intersection(unassigned)