from constants import *
import copy

class LENDEC():
    '''Implements length decrement consistency.
    
    Consecutive nodes must decrease in length. The following relations must
    hold between L2 through L7:
    
    L2 > L3

    L3 > L4

    L4 > L5

    L5 > L6

    L6 > L7'''
    def __init__(self):
        self.__neighbors = {("L2", "L3"), ("L3", "L4"),
                ("L4", "L5"), ("L5", "L6"), ("L6", "L7")}

    def establish(self, csp, curvar, value):
        '''Establishes consistency after curvar: value assignment.'''
        A = csp.get_assignment()
        queue = set([])
        i = int(curvar[1])
        c1 = ("L"+str(i), "L"+str(i+1))
        c2 = ("L"+str(i-1), "L"+str(i))
        if c1 in self.__neighbors:
            queue.add(c1)
        if c2 in self.__neighbors:
            queue.add(c2)
        D = csp.get_domains()
        return self.__ac3(csp, A, D, queue)

    def propagate(self, csp, reduced_vars):
        '''Establishes consistency after reduction of some variables.'''
        A = csp.get_assignment()
        queue = set([])
        for rvar in reduced_vars:
            i = int(rvar[1])
            c1 = ("L"+str(i), "L"+str(i+1))
            c2 = ("L"+str(i-1), "L"+str(i))
            if c1 in self.__neighbors:
                queue.add(c1)
            if c2 in self.__neighbors:
                queue.add(c2)        
        D = csp.get_domains()
        return self.__ac3(csp, A, D, queue)

    def __ac3(self, csp, A, D, queue):
        examined = set([])
        confset = set([])
        reduced = set([])
        while len(queue) > 0:
            (Li, Lj) = queue.pop()
            if Li in A and Lj in A:
                confset.update({Li, Lj})
                continue
            if Li in A:
                confset.add(Li)
            else:
                examined.add(Li)
            if Lj in A:
                confset.add(Lj)
            else:
                examined.add(Lj)
            (Di, Dj, new_pairs) = self.__revise(Li, Lj, A, D)
            if Di == CONTRADICTION or Dj == CONTRADICTION:
                return (CONTRADICTION, examined, confset)
            if Di != DOMAIN_INTACT:
                reduced.add(Li)
                csp.update_domain(Li, Di)
            elif Dj != DOMAIN_INTACT:
                reduced.add(Lj)
                csp.update_domain(Lj, Dj)
            if len(new_pairs) > 0:
                queue.update(new_pairs)
        if len(reduced) > 0:
            return (DOMAINS_REDUCED, examined, confset)
        return (DOMAINS_INTACT, examined)

    def __revise(self, Li, Lj, A, D):
        '''Canculates new consistent bounds for Li and Lj where Lj < Li.'''
        new_pairs = set([])
        Di = DOMAIN_INTACT
        Dj = DOMAIN_INTACT
        if not Li in A:
            if Lj in A:
                new_min = A[Lj] + 1
            else:
                new_min = D[Lj]["min"] + 1
            Di = {"min": new_min, "max": D[Li]["max"]}
        if not Lj in A:
            if Li in A:
                new_max = A[Li] - 1
            else:
                new_max = D[Li]["max"] - 1
            Dj = {"min": D[Lj]["min"], "max": new_max}
        if Di != DOMAIN_INTACT:
            if Di["min"] > Di["max"]:
                Di = CONTRADICTION
            elif Di["min"] <= D[Li]["min"]:
                Di = DOMAIN_INTACT
            else: # reduced
                new_pairs.update(self.__new_pairs(int(Li[1])))
        if Dj != DOMAIN_INTACT:
            if Dj["max"] < Dj["min"]:
                Dj = CONTRADICTION
            elif Dj["max"] >= D[Lj]["max"]:
                Dj = DOMAIN_INTACT
            else: # reduced
                new_pairs.update(self.__new_pairs(int(Lj[1])))
        return (Di, Dj, new_pairs)

    def __new_pairs(self, i):
        pair1 = ("L"+str(i), "L"+str(i+1))
        pair2 = ("L"+str(i-1), "L"+str(i))
        new_pairs = set([])
        if pair1 in self.__neighbors:
            new_pairs.add(pair1)
        if pair2 in self.__neighbors:
            new_pairs.add(pair2)
        return new_pairs
