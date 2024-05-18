from constants import *

class DIAMDEC():
    '''Implements diameter decrement consistency.
        
        0.5 <= P3.diameter - P2.diameter <= 1.5
        0.5 <= P4.diameter - P3.diameter <= 1.5
        0.5 <= P5.diameter - P4.diameter <= 1.5
        0.5 <= P6.diameter - P5.diameter <= 1.5
        0.5 <= P7.diameter - P6.diameter <= 1.5

        i.e. the diamater difference between adjacent nodes must 
        fall into an accepted range.

        The accepted range is defined in specs.py as a configuration option,
        having min and max as lower and upper bounds.

        The algorithm assumes that the order of assignments are in the
        order of variables indices. That is P1, P2, P3, P4, P5, P6, and P7.

        This constraint restricts final solutions to conic-shape ones.'''

    def establish(self, csp, curvar, value, participants, spec):
        '''Establishes consistency after curvar: value assignment.
        
        The assumption is that curvar is in the assigned variables.'''
        Pi, Pj = sorted(participants, key=lambda p: int(p[1:]))
        A = csp.get_assignment()
        D = csp.get_domains()
        return self.__revise(csp, Pi, Pj, A, D, spec["ddiff"])

    def propagate(self, csp, reduced_vars, participants, spec):
        '''Establishes consistency after reduction of some variables.'''
        Pi, Pj = sorted(participants, key=lambda p: int(p[1:]))
        A = csp.get_assignment()
        D = csp.get_domains()
        return self.__revise(csp, Pi, Pj, A, D, spec["ddiff"])

    def __revise(self, csp, Pi, Pj, A, D, ddiff):
        '''Removes illegal values from Dvari and Dvarj'''
        domain_i = set([])
        domain_j = set([])
        i_pieces = {A[Pi]} if Pi in A else D[Pi]
        j_pieces = {A[Pj]} if Pj in A else D[Pj]
        for piece_i in i_pieces:              
            for piece_j in j_pieces:
                diff = piece_i[4] - piece_j[4]
                if diff <= ddiff["max"] and diff >= ddiff["min"]:
                    domain_j.add(piece_j)
                    domain_i.add(piece_i)
        reduced_vars = set([])
        if Pi in A or len(domain_i) == len(D[Pi]):
            domain_i = DOMAIN_INTACT
        elif len(domain_i) == 0:
            return (CONTRADICTION, {Pi})
        else:
            reduced_vars.add(Pi)
            csp.update_domain(Pi, domain_i)
        if Pj in A or len(domain_j) == len(D[Pj]):
            domain_j = DOMAIN_INTACT
        elif len(domain_j) == 0:
            return (CONTRADICTION, {Pj})
        else:
            reduced_vars.add(Pj)
            csp.update_domain(Pj, domain_j)
        if domain_i == DOMAIN_INTACT and domain_j == DOMAIN_INTACT:
            return ALREADY_CONSISTENT
        return (MADE_CONSISTENT, reduced_vars)