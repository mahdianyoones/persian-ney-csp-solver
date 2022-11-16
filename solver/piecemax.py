from constants import *
import copy

class PIECEMAX():

    def establish(self, csp, curvar, value, participants):
        '''Establishes consistency after curvar: value assignment.
        
        The assumption is that curvar is in the assigned variables.'''
        unassigned_vars = csp.get_unassigned_vars()
        participants = participants.intersection(unassigned_vars)
        if len(participants) == 0:
            return REVISED_NONE
        i = curvar[1]
        Li, Pi = "L" + i, "P" + i
        A = csp.get_assignment()
        if Li in A:
            return REVISED_NONE
        D = csp.get_domains()
        return self.__revise(Li, Pi, A, D)

    def propagate(self, csp, reduced_vars, participants):
        '''Establishes consistency after reduction of some variables.'''
        unassigned_vars = csp.get_unassigned_vars()
        participants = participants.intersection(unassigned_vars)
        if len(participants) == 0:
            raise Exception("Members are all assigned; no call is needed.")
        one_of_them = participants.pop()
        i = one_of_them[1]
        Li, Pi = "L" + i, "P" + i
        A = csp.get_assignment()
        D = csp.get_domains()
        return self.__revise(Li, Pi, A, D)

    def __revise(self, Li, Pi, A, D):
        '''Makes the upper bound of Li consistent, if possible.'''
        if Pi in A:
            p, max_len = A[Pi]
        else:
            max_len = 0
            for piece in D[Pi]:
                p, _len = piece
                if _len > max_len:
                    max_len = _len
        if D[Li]["max"] <= max_len:
            return ALREADY_CONSISTENT
        elif D[Li]["min"] > max_len:
            return CONTRADICTION
        D[Li]["max"] = max_len
        return MADE_CONSISTENT, {Li}
