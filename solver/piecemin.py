from constants import *
import copy

class PIECEMIN():

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
        '''Removes illegal values from the domain of Pi, if possible.'''
        if not Pi in A:
            if Li in A:
                min_len = A[Li]
            else:
                min_len = D[Li]["min"]
            reduced_vars = set([])
            for piece in copy.deepcopy(D[Pi]):
                p, _len = piece
                if min_len > _len:
                    D[Pi].remove(piece)
                    reduced_vars.add(Pi)
            if D[Pi] == set([]):
                return CONTRADICTION
            if len(reduced_vars) == 0:
                return ALREADY_CONSISTENT
            return MADE_CONSISTENT, {Pi}
        else:
            if Li in A:
                min_len = A[Li]
            else:
                min_len = D[Li]["min"]
            p, _len = A[Pi]
            if min_len > _len:
                return CONTRADICTION
            return ALREADY_CONSISTENT 
