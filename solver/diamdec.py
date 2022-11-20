from constants import *
import copy

class DIAMDEC():
    '''Implements diameter decrement consistency.
    
        The constraint makes sure the following relations exist between D
        variables:
    
        0.5 <= D2 - D1 <= 1.5
        0.5 <= D3 - D2 <= 1.5
        0.5 <= D4 - D3 <= 1.5
        0.5 <= D5 - D4 <= 1.5
        0.5 <= D6 - D5 <= 1.5
        0.5 <= D7 - D6 <= 1.5

        i.e. the diamater difference between adjacent nodes must 
        fall into an accepted range.

        The accepted range is defined in specs.py as a configuration option,
        having min and max as lower and upper bounds.

        The algorithm assumes that the order of assignments are in the
        order of variables indices. That is D1, D2, D3, D4, D5, D6, and D7.

        This constraint restricts final solutions to conic-shape ones.'''

    def __init__(self, ddiff):
        self.__ddiff = ddiff

    def establish(self, csp, curvar, value, participants):
        '''Establishes consistency after curvar: value assignment.
        
        The assumption is that curvar is in the assigned variables.'''
        Dvari, Dvarj = sorted(participants)
        A = csp.get_assignment()
        D = csp.get_domains()
        return self.__revise(csp, Dvari, Dvarj, A, D, self.__ddiff)

    def propagate(self, csp, reduced_vars, participants):
        '''Establishes consistency after reduction of some variables.'''
        unassigned_vars = csp.get_unassigned_vars()
        if len(participants.intersection(unassigned_vars)) == 0:
            raise Exception("Members are all assigned; no call is needed.")
        Dvari, Dvarj = sorted(participants)
        A = csp.get_assignment()
        D = csp.get_domains()
        return self.__revise(csp, Dvari, Dvarj, A, D, self.__ddiff)

    def __revise(self, csp, Dvari, Dvarj, A, D, ddiff):
        '''Removes illegal values from Dvari and Dvarj'''
        Di = set([])
        Dj = set([])
        i_diams = {A[Dvari]} if Dvari in A else D[Dvari]
        j_diams = {A[Dvarj]} if Dvarj in A else D[Dvarj]
        for di in i_diams:              
            for dj in j_diams:
                diff = di - dj
                if diff <= ddiff["max"] and diff >= ddiff["min"]:
                    Dj.add(dj)
                    Di.add(di)
        reduced_vars = set([])
        if Dvari in A or len(Di) == len(D[Dvari]):
            Di = DOMAIN_INTACT
        elif len(Di) == 0:
            return CONTRADICTION
        else:
            reduced_vars.add(Dvari)
            csp.update_domain(Dvari, Di)
        if Dvarj in A or len(Dj) == len(D[Dvarj]):
            Dj = DOMAIN_INTACT
        elif len(Dj) == 0:
            return CONTRADICTION
        else:
            reduced_vars.add(Dvarj)
            csp.update_domain(Dvarj, Dj)
        if Di == DOMAIN_INTACT and Dj == DOMAIN_INTACT:
            return ALREADY_CONSISTENT
        return (MADE_CONSISTENT, reduced_vars)