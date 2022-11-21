from constants import *
import copy

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

    def establish(self, csp, curvar, value, participants):
        '''Establishes consistency after curvar: value assignment.
        
        The assumption is that curvar is in the assigned variables.'''
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
        '''Canculates new consistent bounds for Li and Lj where Lj < Li.'''
        Dj = D[Lj]
        Di = D[Li]
        if Li in A:
            Di = {"min": A[Li], "max": A[Li]}
        elif Lj in A:
            Dj = {"min": A[Lj], "max": A[Lj]}
        reduced_vars = set([])
        if Dj["min"] >= Di["max"]:
            return (CONTRADICTION, self.__failed_set(csp, {Li, Lj}))
        if Dj["min"] >= Di["min"]:
            Di["min"] = Dj["min"] + 1
            reduced_vars.add(Li)
        if Dj["max"] >= Di["max"]:
            Dj["max"] = Di["max"] - 1
            reduced_vars.add(Lj)
        if len(reduced_vars) == 0:
            return ALREADY_CONSISTENT
        return MADE_CONSISTENT, reduced_vars

    def __failed_set(self, csp, participants):
        '''Returns the failed set.'''
        unassigned = csp.get_unassigned_vars()
        return participants.intersection(unassigned)    