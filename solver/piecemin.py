from constants import *

class PIECEMIN():
    '''Establishes Pi.len <= Li.min when Li is not assigned,
    and Pi.len <= Li.value when assigned.
    
    Ensures that pieces suitable for a node (Pi) are at least as tall as the
    length of the node (Li). Illegal pieces are removed from the domain of Pi.'''

    def establish(self, csp, curvar, value, participants, kook):
        '''Establishes consistency after curvar: value assignment.
        
        The assumption is that curvar is in the assigned variables.'''
        i = curvar[1:]
        Li, Pi = "L" + i, "P" + i
        A = csp.get_assignment()
        if Pi in A:
            return REVISED_NONE
        D = csp.get_domains()
        return self.__revise(csp, Li, Pi, A, D)

    def propagate(self, csp, reduced_vars, participants, kook):
        '''Establishes consistency after reduction of some variables.'''
        for p in participants:
            i = p[1:]
            break
        Li, Pi = "L" + i, "P" + i
        A = csp.get_assignment()
        if Pi in A:
            return REVISED_NONE
        D = csp.get_domains()
        return self.__revise(csp, Li, Pi, A, D)

    def __revise(self, csp, Li, Pi, A, D):
        '''Removes illegal values from the domain of Pi, if possible.'''
        if Li in A:
            min_len = A[Li]
        else:
            min_len = D[Li]["min"]
        new_domain = set([])
        for piece in D[Pi]:
            _len = piece[1]
            if min_len <= _len:
                new_domain.add(piece)
        if new_domain == set([]):
            return (CONTRADICTION, {Pi})
        elif len(new_domain) == len(D[Pi]):
            return ALREADY_CONSISTENT
        csp.update_domain(Pi, new_domain)
        return (MADE_CONSISTENT, {Pi})