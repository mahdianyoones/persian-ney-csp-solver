from functools import reduce
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
        self.__neighbors = {("D1", "D2"), ("D2", "D3"), ("D3", "D4"),
                ("D4", "D5"), ("D5", "D6"), ("D6", "D7")}

    def establish(self, csp, curvar, value):
        '''Establishes consistency after curvar: value assignment.'''
        A = csp.get_assignment()
        queue = set([])
        i = int(curvar[1])
        c1 = ("D"+str(i), "D"+str(i+1))
        c2 = ("D"+str(i-1), "D"+str(i))
        if c1 in self.__neighbors:
            queue.add(c1)
        if c2 in self.__neighbors:
            queue.add(c2)
        D = csp.get_domains()
        ddiff = self.__ddiff
        return self.__ac3(csp, A, D, queue, ddiff)

    def propagate(self, csp, reduced_vars):
        '''Establishes consistency after reduction of some variables.'''
        A = csp.get_assignment()
        queue = set([])
        for rvar in reduced_vars:
            i = int(rvar[1])
            c1 = ("D"+str(i), "D"+str(i+1))
            c2 = ("D"+str(i-1), "D"+str(i))
            if c1 in self.__neighbors:
                queue.add(c1)
            if c2 in self.__neighbors:
                queue.add(c2)        
        D = csp.get_domains()
        ddiff = self.__ddiff
        return self.__ac3(csp, A, D, queue, ddiff)

    def __ac3(self, csp, A, D, queue, ddiff):
        examined = set([])
        confset = set([])
        reduced = set([])
        while len(queue) > 0:
            (Dvari, Dvarj) = queue.pop()
            if Dvari in A and Dvarj in A:
                confset.update({Dvari, Dvarj})
                continue
            if Dvari in A:
                confset.add(Dvari)
            else:
                examined.add(Dvari)
            if Dvarj in A:
                confset.add(Dvarj)
            else:
                examined.add(Dvarj)
            (Di, Dj, new_pairs) = self.__revise(Dvari, Dvarj, A, D, ddiff)
            if Di == CONTRADICTION or Dj == CONTRADICTION:
                return (CONTRADICTION, examined, confset)
            if Di != DOMAIN_INTACT:
                reduced.add(Dvari)
                csp.update_domain(Dvari, Di)
            if Dj != DOMAIN_INTACT:
                reduced.add(Dvarj)
                csp.update_domain(Dvarj, Dj)
            if len(new_pairs) > 0:
                queue.update(new_pairs)
        if len(reduced) > 0:
            return (DOMAINS_REDUCED, examined, reduced)
        return (DOMAINS_INTACT, examined)

    def __revise(self, Dvari, Dvarj, A, D, ddiff):
        '''Canculates new consistent bounds for Diam_i and Diam_j.'''
        Di = set([])
        Dj = set([])
        new_pairs = set([])
        i_diams = {A[Dvari]} if Dvari in A else D[Dvari]
        j_diams = {A[Dvarj]} if Dvarj in A else D[Dvarj]
        for di in i_diams:
            for dj in j_diams:
                diff = di - dj
                if diff <= ddiff["max"] and diff >= ddiff["min"]:
                    Di.add(di)
                    Dj.add(dj)
        if len(Di) == 0:
            Di = CONTRADICTION
        elif Dvari in A or len(Di) == len(D[Dvari]):
            Di = DOMAIN_INTACT
        else: # i reduced
            reduced_idx = int(Dvari[1])
            new_pairs.update(self.__new_pairs(reduced_idx, Dvari, Dvarj))
        if len(Dj) == 0:
            Dj = CONTRADICTION
        elif Dvarj in A or len(Dj) == len(D[Dvarj]):
            Dj = DOMAIN_INTACT
        else: # j reduced
            reduced_idx = int(Dvarj[1])
            new_pairs.update(self.__new_pairs(reduced_idx, Dvari, Dvarj))
        return (Di, Dj, new_pairs)

    def __new_pairs(self, reduced_idx, Dvari, Dvarj):
        pair1 = ("D"+str(reduced_idx), "D"+str(reduced_idx+1))
        pair2 = ("D"+str(reduced_idx-1), "D"+str(reduced_idx))
        new_pairs = set([])
        if pair1 in self.__neighbors and pair1 != (Dvari, Dvarj):
            new_pairs.add(pair1)
        if pair2 in self.__neighbors and pair2 != (Dvari, Dvarj):
            new_pairs.add(pair2)
        return new_pairs
