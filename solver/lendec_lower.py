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
                continue
            if not Li in A:
                examined.add(Li)
            if not Lj in A:
                examined.add(Lj)
            (Dj, new_pairs) = self.__revise(Li, Lj, A, D)
            if Dj == CONTRADICTION:
                confset = self.__confset(csp)
                return (CONTRADICTION, examined, confset)
            elif Dj != DOMAIN_INTACT:
                reduced.add(Lj)
                csp.update_domain(Lj, Dj)
                queue.update(new_pairs)
        if len(reduced) > 0:
            return (DOMAINS_REDUCED, examined, reduced)
        return (DOMAINS_INTACT, examined)

    def __revise(self, Li, Lj, A, D):
        '''Canculates new consistent bounds for Lj, if possible.
        
        Or checks the boundaries of Li if Lj is assigned.

        Enforces Lj >= 2/3 Li
        
        The assumption is that at least one of Li and Lj are not assigned.'''
        new_pairs = set([])
        Di = DOMAIN_INTACT
        Dj = DOMAIN_INTACT
        if Li in A:
            threshold = math.ceil(2/3 * A[Li])        
        else:
            threshold = math.ceil(2/3 * D[Li]["min"])
        if Lj in A:
            if A[Lj] < threshold:
                Dj = CONTRADICTION
        elif D[Lj]["min"] < threshold:
            if D[Lj]["max"] >= threshold:
                Dj = {"min": threshold, "max": D[Lj]["max"]}
                idx = int(Lj[1])
                new_pair = ("L"+str(idx), "L"+str(idx+1))
                if new_pair in self.__neighbors:
                    new_pairs.add(new_pair)
            else:
                Dj = CONTRADICTION
        return (Dj, new_pairs)

    def __confset(self, csp):
        '''Returns the conflict set.'''
        members = {"L2", "L3", "L4", "L5", "L6"}
        assigned = csp.get_assigned_vars()
        return members.intersection(assigned)
