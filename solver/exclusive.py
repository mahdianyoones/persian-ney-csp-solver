from constants import *
import copy

class EXCLUSIVE():
    '''Implements exclusive consistency algorith,
    
    When a P and its corresponding L variable is assigned,
    the rest of P variables must be updated accordingly.
    
    For example, if 
    A  = {
        P1: (1, 20, 0, 0, 19),
        L1: 10
    }
    
    The piece (1, 20, 0, 0, 19) must be deleted from
    the domain of all P variables and the remaining of it,
    that is (1, 10, 0, 0, 19) must be added to the domain of
    all P variables.
    
    If a P variables becomes empty, it is a contradiction.'''

    def establish(self, csp, curvar, value, participants, spec):
        i = curvar[1:]
        Li = "L"+i
        Pi = "P"+i
        A = csp.get_assignment()
        D = csp.get_domains()
        if curvar == Li and not Pi in A:
            return self.__check_for_all_assigned_pieces(csp, A, D)            
        assigned_piece = value if curvar == Pi else A[Pi]
        return self.__check_for_piece(csp, assigned_piece, A, D)

    def propagate(self, csp, reduced_vars, participants, spec):
        '''If there is at least one reduced L, the rest of variables
        must be checked for consistency.
        
        However, reductions in P variables may not impact consistency of
        variables.'''
        A = csp.get_assignment()
        D = csp.get_domains()
        for rv in reduced_vars:
            if rv[0] == "L":
                return self.__check_for_all_assigned_pieces(csp, A, D)
        return REVISED_NONE

    def __check_for_all_assigned_pieces(self, csp, A, D):
        p_vars = [_var for _var in csp.get_assigned_vars() if _var[0] == "P"]
        reduced_vars = set([])
        for p_var in p_vars:
            assigned_piece = A[p_var]
            res = self.__check_for_piece(csp, assigned_piece, A, D)
            if type(res) == tuple:
                if res[0] == CONTRADICTION:
                    return res
                elif res[0] == MADE_CONSISTENT:
                    reduced_vars.update(res[1])
        if len(reduced_vars) == 0:
            return REVISED_NONE
        return MADE_CONSISTENT, reduced_vars

    def __check_for_piece(self, csp, assigned_piece, A, D):
        reduced_vars = set([])
        assigned_ps = [_var for _var in csp.get_assigned_vars() if _var[0] == "P"]
        do_share = set([p_var for p_var in assigned_ps if A[p_var] == assigned_piece])
        allocated_sum = self.__allocated_sum(do_share, assigned_piece, A, D)
        if type(allocated_sum) == tuple:
            return (CONTRADICTION, allocated_sum[1])
        remaining_length = assigned_piece[1] - allocated_sum
        res = self.__adjust_upper_bounds(csp, do_share, remaining_length, D)
        reduced_vars.update(res[1])
        res = self.__remove_illegal_pieces(csp, assigned_piece, remaining_length, D, A)
        if res[0] == CONTRADICTION:
            return res
        else:
            reduced_vars.update(res[1])
        if len(reduced_vars) > 0:
            return MADE_CONSISTENT, reduced_vars
        return ALREADY_CONSISTENT

    def __allocated_sum(self, do_share, assigned_piece, A, D):
        allocated_sum = 0
        for p_var in do_share:
            corresLi = "L" + p_var[1:]
            if corresLi in A:
                allocated_sum += A[corresLi]
                if allocated_sum > assigned_piece[1]:
                    raise Exception("Domains are not consistent!")
            else:
                allocated_sum += D[corresLi]["min"]
                if allocated_sum > assigned_piece[1]:
                    return (CONTRADICTION, {corresLi})
        return allocated_sum

    def __adjust_upper_bounds(self, csp, do_share, remaining_length, D):
        reduced_vars = set([])
        do_share_corresLs = set(["L"+p[1:] for p in do_share])
        unassigned_do_share = do_share_corresLs.intersection(csp.get_unassigned_vars())
        for p_var in unassigned_do_share:
            corresLi = "L" + p_var[1:]
            if D[corresLi]["max"] > D[corresLi]["min"] + remaining_length:
                D[corresLi]["max"] = D[corresLi]["min"] + remaining_length
                reduced_vars.add(corresLi)
        return MADE_CONSISTENT, reduced_vars

    def __remove_illegal_pieces(self, csp, assigned_piece, remaining_length, D, A):
        unassigned_ps = [_var for _var in csp.get_unassigned_vars() if _var[0] == "P"]
        may_share = [p_var for p_var in unassigned_ps if assigned_piece in D[p_var]]
        reduced_vars = set([])
        for p_var in may_share:
            corresLi = "L" + p_var[1:]
            node_length = A[corresLi] if corresLi in A else D[corresLi]["min"]
            if node_length > remaining_length:
                D[p_var].remove(assigned_piece)
                if len(D[p_var]) == 0:
                    return (CONTRADICTION, {p_var})
                reduced_vars.add(p_var)
        return (MADE_CONSISTENT, reduced_vars)