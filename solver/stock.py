from constants import *

class ROUND_STOCK():
    '''Implements consistency for higher-order round_stock contrains.

    This constraint is defined on groups of variables Di, Ti, Ri; therefore, 
    creating 7 distinct constraints
    {round_stock(T1, R1, D1), ..., round_stock(T7, R7, D7)}.

    These constraints limit the values of Ri variables to those found
    in the dataset with regard to assignments to Di and Ti.

    Note: Depending on various assigned variables, each constraint can
    be further factored into the following constraints.
    
    Ti = filter by Ri			(when Ri is assigned only)
    Ti = filter by Di
    Ti = filter by Ri & Di		(when Ri and Di are assigned only)

    where 1 <= i <= 7
    
    However, this algorithm establushes consistency for all of the above 
    constraints at once since the logic of them all are the same.'''

    def __init__(self, catalog):
        self.__catalog = catalog
    
    def establish(self, csp, curvar, value, participants):
        '''Establishes consistency after curvar: value assignment.'''
        i = curvar[1]
        Ri, Di, Ti = "R"+i, "D"+i, "T"+i
        if curvar == Ri:
            return REVISED_NONE
        A = csp.get_assignment()
        D = csp.get_domains()
        catalog = self.__catalog
        filters = {key[0]: A[key] for key in {Di, Ti}.intersection(A.keys())}
        found_values = catalog.values("R", filters)
        if found_values == NODE_NOT_FOUND:
            return (CONTRADICTION, {Ri})
        new_domain = D[Ri].intersection(found_values)
        if len(new_domain) < len(D[Ri]):
            reduced_vars = {Ri}
            csp.update_domain(Ri, new_domain)
            return (MADE_CONSISTENT, reduced_vars)
        return ALREADY_CONSISTENT

    def propagate(self, csp, reduced_vars, participants):
        return REVISED_NONE        

class THICK_STOCK():
    '''Implements consistency for higher_order thick_stock contrains.

    Details and descriptions of round_stock apply here too.'''

    def __init__(self, catalog):
        self.__catalog = catalog
    
    def establish(self, csp, curvar, value, participants):
        '''Establishes consistency after curvar: value assignment.'''
        i = curvar[1]
        Ti, Di, Ri = "T"+i, "D"+i, "R"+i
        if curvar == Ti:
            return REVISED_NONE
        A = csp.get_assignment()
        D = csp.get_domains()
        catalog = self.__catalog
        filters = {key[0]: A[key] for key in {Di, Ri}.intersection(A.keys())}
        found_values = catalog.values("T", filters)
        if found_values == NODE_NOT_FOUND:
            return (CONTRADICTION, {Ti})
        new_domain = D[Ti].intersection(found_values)
        if len(new_domain) < len(D[Ti]):
            reduced_vars = {Ti}
            csp.update_domain(Ti, new_domain)
            return (MADE_CONSISTENT, reduced_vars)
        return ALREADY_CONSISTENT

    def propagate(self, csp, reduced_vars, participants):
        return REVISED_NONE

class DIAM_STOCK():
    '''Implements consistency for higher_order diam_stock contrains.

    Details and descriptions of round_stock apply here too.'''

    def __init__(self, catalog):
        self.__catalog = catalog
    
    def establish(self, csp, curvar, value, participants):
        '''Establishes consistency after curvar: value assignment.'''
        i = curvar[1]
        Ti, Ri, Di = "T"+i, "R"+i, "D"+i
        if curvar == Di:
            return REVISED_NONE
        A = csp.get_assignment()
        D = csp.get_domains()
        catalog = self.__catalog
        filters = {key[0]: A[key] for key in {Ti, Ri}.intersection(A.keys())}
        found_values = catalog.values("D", filters)
        if found_values == NODE_NOT_FOUND:
            return (CONTRADICTION, {Di})
        new_domain = D[Di].intersection(found_values)
        if len(new_domain) < len(D[Di]):
            reduced_vars = {Di}
            csp.update_domain(Di, new_domain)
            return (MADE_CONSISTENT, reduced_vars)
        return ALREADY_CONSISTENT

    def propagate(self, csp, reduced_vars, participants):
        return REVISED_NONE

class PIECE_STOCK():
    '''Implements consistency for higher_order piece_stock contrains.

    Details and descriptions of round_stock apply here too.'''

    def __init__(self, catalog):
        self.__catalog = catalog
    
    def establish(self, csp, curvar, value, participants):
        '''Establishes consistency after curvar: value assignment.'''
        i = curvar[1]
        Pi, Di, Ri, Ti = "P"+i, "D"+i, "R"+i, "T"+i
        A = csp.get_assignment()
        D = csp.get_domains()
        return self.__revise(csp, A, D, Ti, Di, Ri, Pi)

    def propagate(self, csp, reduced_vars, participants):
        '''Propagates reduction of P vars to T, R, and D vars & vice versa.'''
        reduced_P = None
        for reduced_var in reduced_vars:
            if reduced_var[0] == "P":
                reduced_P = reduced_var
                break
        if reduced_P == None:
            return REVISED_NONE
        A = csp.get_assignment()
        i = reduced_P[1]
        Di, Ri, Ti, Pi = "D"+i, "R"+i, "T"+i, "P"+i
        D = csp.get_domains()
        return self.__revise(csp, A, D, Ti, Di, Ri, Pi)

    def __get_pieces(self, A, Pi, D):
        if Pi in A:
            no, L = A[Pi]
            left_numbers = {no}
        else:
            left_numbers = set([])
            for piece in D[Pi]:
                no, L = piece
                left_numbers.add(no)
        return self.__catalog.get_pieces(left_numbers)

    def __get_legal_pieces(self, diams, thicks, rounds, pieces):
        legal_pieces = set([])
        for no, piece in pieces.items():
            right_thick = piece["T"] in thicks
            right_diam = piece["D"] in diams
            right_round = piece["R"] in rounds
            if right_diam and right_round and right_thick:
                legal_pieces.add((no, piece["L"]))
        return legal_pieces

    def __revise(self, csp, A, D, Ti, Di, Ri, Pi):
        pieces = self.__get_pieces(A, Pi, D)
        diams = {A[Di]} if Di in A else D[Di]
        thicks = {A[Ti]} if Ti in A else D[Ti]
        rounds = {A[Ri]} if Ri in A else D[Ri]
        reduced_vars = set([])
        for v in {Ti, Di, Ri, Pi}:
            if not v in A:
                if v == Pi:
                    legals = self.__get_legal_pieces(diams, thicks, rounds, pieces)
                else:
                    legals = {piece[v[0]] for piece in pieces.values()}
                new_domain = legals.intersection(D[v])
                if new_domain == set([]):
                    return CONTRADICTION, {v}
                if D[v] != new_domain:
                    reduced_vars.add(v)
                    csp.update_domain(v, new_domain)
        if len(reduced_vars) == 0:
            return ALREADY_CONSISTENT
        return (MADE_CONSISTENT, reduced_vars)