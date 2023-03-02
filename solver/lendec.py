from constants import *

class LENDEC():
    '''Implements length decrement boundary consistency.
    
    Consecutive nodes must decrease in length. The following relations must
    hold between L2 through L7:
    
    L2 > L3

    L3 > L4

    L4 > L5

    L5 > L6

    L6 > L7
    
    For each relation, a binary constraint is defined. This class establishes
    binary consistency for them all.'''

    def establish(self, csp, curvar, value, participants, spec):
        '''Establishes consistency after curvar: value assignment.
        
        The assumption is that curvar is in the assigned variables.'''
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
        '''Canculates new consistent bounds for Li and Lj where Lj < Li.'''
        reduced_vars = set([])
        if Li in A: # make Lj[max] consistent
            newDj = {
                "min": D[Lj]["min"],
                "max": min(A[Li]-1, D[Lj]["max"])
            }
            if newDj["min"] > newDj["max"]:
                return (CONTRADICTION, {Lj})
            if newDj != D[Lj]:
                csp.update_domain(Lj, newDj)
                reduced_vars.add(Lj)
        elif Lj in A: # make Li[min] consistent
            newDi = {
                "min": max(A[Lj]+1, D[Li]["min"]),
                "max": D[Li]["max"]
            }
            if newDi["min"] > newDi["max"]:
                return (CONTRADICTION, {Li})
            if newDi != D[Li]:
                csp.update_domain(Li, newDi)
                reduced_vars.add(Li)
        else: # try making Li[min] and Lj[max] consistent
            newDi = {
                "min": max(D[Lj]["min"]+1, D[Li]["min"]),
                "max": D[Li]["max"],
            }
            if newDi["min"] > newDi["max"]:
                return (CONTRADICTION, {Li, Lj})
            newDj = {
                "min": D[Lj]["min"],
                "max": min(D[Li]["max"]-1, D[Lj]["max"]),
            }
            if newDj["min"] > newDj["max"]:
                return (CONTRADICTION, {Li, Lj})
            if newDj != D[Lj]:
                csp.update_domain(Lj, newDj)
                reduced_vars.add(Lj)
            if newDi != D[Li]:
                csp.update_domain(Li, newDi)
                reduced_vars.add(Li)
        if len(reduced_vars) == 0:
            return ALREADY_CONSISTENT
        return MADE_CONSISTENT, reduced_vars

    def __failed_set(self, csp, participants):
        '''Returns the failed set.'''
        unassigned = csp.get_unassigned_vars()
        return participants.intersection(unassigned)    