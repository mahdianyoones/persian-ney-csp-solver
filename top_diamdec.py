from constants import *

class TOP_DIAMDEC():
    '''Implements diameter decrement consistency between top and second nodes.
        
        0.5 <= P2.diameter - P1.diameter <= 1.5

        i.e. enforces a wider diamter for top node'''

    def establish(self, csp, curvar, value, participants, spec):
        '''Establishes consistency after curvar: value assignment.
        
        The assumption is that curvar is in the assigned variables.'''
        # TODO: assert existence of curvar in assigned vars
        P_top, P_second = sorted(participants, key=lambda p: int(p[1:]))
        A = csp.get_assignment()
        D = csp.get_domains()
        return self.__revise(csp, P_top, P_second, A, D, spec["top_ddiff"])

    def propagate(self, csp, reduced_vars, participants, spec):
        '''Establishes consistency after reduction of some variables.'''
        P_top, P_second = sorted(participants, key=lambda p: int(p[1:]))
        A = csp.get_assignment()
        D = csp.get_domains()
        return self.__revise(csp, P_top, P_second, A, D, spec["top_ddiff"])

    def __revise(self, csp, P_top, P_second, A, D, ddiff):
        '''Removes illegal values from Dvari and Dvarj'''
        domain_top = set([])
        domain_second = set([])
        top_pieces = {A[P_top]} if P_top in A else D[P_top]
        second_pieces = {A[P_second]} if P_second in A else D[P_second]
        for piece_top in top_pieces:              
            for piece_second in second_pieces:
                diff = piece_top[4] - piece_second[4]
                if diff <= ddiff["max"] and diff >= ddiff["min"]:
                    domain_second.add(piece_second)
                    domain_top.add(piece_top)
        reduced_vars = set([])
        if P_top in A or len(domain_top) == len(D[P_top]):
            domain_top = DOMAIN_INTACT
        elif len(domain_top) == 0:
            return (CONTRADICTION, {P_top})
        else:
            reduced_vars.add(P_top)
            csp.update_domain(P_top, domain_top)
        if P_second in A or len(domain_second) == len(D[P_second]):
            domain_second = DOMAIN_INTACT
        elif len(domain_second) == 0:
            return (CONTRADICTION, {P_second})
        else:
            reduced_vars.add(P_second)
            csp.update_domain(P_second, domain_second)
        if domain_top == DOMAIN_INTACT and domain_second == DOMAIN_INTACT:
            return ALREADY_CONSISTENT
        return (MADE_CONSISTENT, reduced_vars)