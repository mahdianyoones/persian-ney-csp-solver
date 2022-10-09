from functools import reduce
from constants import *
import math

class LENDEC():
    '''Implements length decrement consistency.
    
    The following relations must hold between L2 through L7:
    
    L2 > L3 > 2/3 L2
    L3 > L4 > 2/3 L3
    L4 > L5 > 2/3 L4
    L5 > L6 > 2/3 L5
    L6 > L7'''
    
    def establish(self, csp, curvar, value):
        '''Establishes consistency after curvar: value assignment.'''
        if curvar == "L7":
            return (DOMAINS_INTACT, set([]))
        A = csp.get_assignment()
        D = csp.get_domains()
        (newbounds, examined) = self.__newbounds(A, D, curvar)
        if newbounds == CONTRADICTION:
            confset = self.__confset(csp)
            return (CONTRADICTION, examined, confset)
        for Li, new_domain in newbounds.items():
            csp.update_domain(Li, new_domain)
        reduced = set(newbounds.keys())
        if len(reduced) == 0:
            return (DOMAINS_INTACT, examined)
        return (DOMAINS_REDUCED, examined, reduced)

    def propagate(self, csp, reduced_vars):
        '''Establishes consistency after reduction of some variables.'''
        reduced_sorted = sorted(reduced_vars)
        if reduced_sorted[0] == "L7":
            return (DOMAINS_INTACT, set([]))
        A = csp.get_assignment()
        D = csp.get_domains()
        (newbounds, examined) = self.__newbounds(A, D, reduced_sorted[0])
        if newbounds == CONTRADICTION:
            confset = self.__confset(csp)
            return (CONTRADICTION, examined, confset)
        for Li, new_domain in newbounds.items():
            csp.update_domain(Li, new_domain)
        reduced = set(newbounds.keys())
        if len(reduced) == 0:
            return (DOMAINS_INTACT, examined)
        return (DOMAINS_REDUCED, examined, reduced)
    
    def __in_range(self, range, value):
        return value >= range["min"] and value <= range["max"]
    
    def __reduced(self, upper, lower, domain):
        return upper - lower < domain["max"] - domain["min"]

    def __confset(self, csp):
        '''Returns the conflict set.'''
        confset = set([])
        A = csp.get_assignment()
        for v in {"L2", "L3", "L4", "L5", "L6", "L7"}:
            if v in A:
                confset.add(v)
        return confset

    def __newbounds(self, A, D, start_var):
        '''Calculates new consistent bounds.
    
        This is a mathematical function.'''
        newbounds = {}
        examined = set([])
        for i in range(int(start_var[1]) + 1, 8):
            lprev = "L" + str(i-1)
            if lprev in newbounds:
                Dprev = {"min": lower, "max": upper}
            elif lprev in A:
                Dprev = {"min": A[lprev], "max": A[lprev]}
            else:
                Dprev = {"min": D[lprev]["min"], "max": D[lprev]["max"]}
            li = "L" + str(i)
            if li in A:
                continue
            examined.add(li)
            if i < 7:
                lower = math.ceil(2/3 * Dprev["min"])
            else:
                lower = Dprev["min"] - 1
            upper = Dprev["max"] - 1
            if not self.__in_range(D[li], lower):
                return (CONTRADICTION, examined)
            if not self.__in_range(D[li], upper):
                return (CONTRADICTION, examined)
            if self.__reduced(upper, lower, D[li]):
                newbounds[li] = {"min": lower, "max": upper}
        return (newbounds, examined)