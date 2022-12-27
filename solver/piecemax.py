from constants import *
import copy

class PIECEMAX():

    def establish(self, csp, curvar, value, participants):
        '''Establishes consistency after curvar: value assignment.
        
        The assumption is that curvar is in the assigned variables.'''
        i = curvar[1]
        Li, Pi = "L" + i, "P" + i
        A = csp.get_assignment()
        if Li in A:
            return REVISED_NONE
        D = csp.get_domains()
        return self.__revise(csp, Li, Pi, A, D)

    def propagate(self, csp, reduced_vars, participants):
        '''Establishes consistency after reduction of some variables.'''
        for p in participants:
            i = p[1]
            break
        Li, Pi = "L"+i, "P"+i
        A = csp.get_assignment()
        D = csp.get_domains()
        return self.__revise(csp, Li, Pi, A, D)

    def __revise(self, csp, Li, Pi, A, D):
        '''Makes the upper bound of Li consistent, if possible.'''
        if Pi in A:
            max_len = A[Pi][1]
        else:
            max_len = 0
            for piece in D[Pi]:
                _len = piece[1]
                if _len > max_len:
                    max_len = _len
        if D[Li]["max"] <= max_len:
            return ALREADY_CONSISTENT
        elif D[Li]["min"] > max_len:
            return (CONTRADICTION, self.__failed_set(csp, {Li, Pi}))
        D[Li]["max"] = max_len
        return MADE_CONSISTENT, {Li}

    def __failed_set(self, csp, participants):
        '''Returns the failed set.'''
        unassigned = csp.get_unassigned_vars()
        return participants.intersection(unassigned)    