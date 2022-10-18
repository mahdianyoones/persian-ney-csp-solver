import queue
from constants import *
import math
import copy

class LENDEC_LOWER():
    '''Implements length decrement lower consistency.
    
    Ensures that nodes do not reduce in length beyond 2/3 of their predecessor
    nodes.
    
    The following relations must hold between L2 through L6:
    
    L3 >= 2/3 L2

    L4 >= 2/3 L3

    L5 >= 2/3 L4

    L6 >= 2/3 L5'''

    def __init__(self):
        self.__neighbors = {("L2", "L3"), ("L3", "L4"),
                ("L4", "L5"), ("L5", "L6")}

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
        D = csp.get_domains()
        queue = set([])
        for rvar in reduced_vars:
            i = int(rvar[1])
            c1 = ("L"+str(i), "L"+str(i+1))
            c2 = ("L"+str(i-1), "L"+str(i))
            if c1 in self.__neighbors:
                queue.add(c1)
            if c2 in self.__neighbors:
                queue.add(c2)        
        return self.__ac3(csp, A, D, queue)

    def __ac3(self, csp, A, D, queue):
        '''Makes the domain of all variables in the queue consistent.
        
        If revision function increase the lower bounds, other variables are
        not rendered inconsistent. Therefore, we don't need recursively revise
        reduced neighbors.'''
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
        '''Canculates a new value to make Li and Lj consistent.
        
        Enforces Lj >= 2/3 Li'''
        new_pairs = set([])
        if Li in A: # Lj is not assigned
            Dj["min"] = math.ceil(2/3 * A[Li])
            if Dj["min"] > D[Lj]["max"]:
                return (DOMAIN_INTACT, CONTRADICTION, set([]))
            if Dj["min"] == D[Lj]["min"]:
                return (DOMAIN_INTACT, DOMAIN_INTACT, set([]))
        elif Lj in A:  # Li is not assigned
            Di["min"] = math.ceil(3/2 * A[Lj])
            if Di["min"] > D[Li]["max"]:
                return (CONTRADICTION, DOMAIN_INTACT, set([]))
            if Di["min"] == D[Li]["min"]:
                return (DOMAIN_INTACT, DOMAIN_INTACT, set([]))
        else:
            Di = copy.deepcopy(D[Li])
            Dj = copy.deepcopy(D[Lj])
            Di["min"] = math.ceil(3/2 * Dj["min"])
            Dj["min"] = math.ceil(2/3 * Di["min"])
            if Di["min"] == D[Li]["min"]: # both already consistent
                return (DOMAIN_INTACT, DOMAIN_INTACT, set([]))
            elif Di["min"] > D[Li]["min"] and Di["max"] <= D[Li]["max"]:
                new_pairs = self.__new_pairs(int(Li[1]))
                return (Di, DOMAIN_INTACT, new_pairs)
            elif Dj["min"] > D[Lj]["min"] and Dj["max"] <= D[Lj]["max"]:
                new_pairs = self.__new_pairs(int(Lj[1]))
                return (DOMAIN_INTACT, Dj, new_pairs)
            else:
                return (CONTRADICTION, CONTRADICTION, set([]))
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