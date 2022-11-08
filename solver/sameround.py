from constants import *

class SAMEROUND():
    '''Applies same roundness constraints.
    
    The variables R1 throught R7 must have the same value in the
    final solution.

    R1 through R7 must be assigned the same value. If at any point, no
    intersection between the domains of these variables exists, contradiction
    has been occured.

    Having no intersection between the domains means that the constraint
    cannot be satisfied.

    However, given that R1 is assigned first before other variables, we
    can implement a simpler and more efficient algorithm.

    Upon assigning any value to R1, we clean the domain of other R variables
    and only leave the assigned value.

    For example, if R1 is assigned 0.5mm and other domains are:

    R2 = {0, 0.5, 1, 1.5}
    R3 = {0.5, 1, 1.5, 2}
    R4 = {0.5, 2}
    and etc

    the domains will be come as such:

    R2 = {0.5}
    R3 = {0.5}
    R4 = {0.5}
    and etc

    and the contradiction can be easily detected if the assigned value cannot
    be found in the current domain of any R variable.

    Note that after assignment of R1 and consistency, propagation does not 
    occur since the domains contain only one value. If any other algorithm
    removes this single value, it issues contradiction itself.'''
    
    def propagate(self, csp, reduced_vars, participants):
        '''Establishes indirect consistency W.R.T. same_r.'''
        return REVISED_NONE
    
    def __new_domains(self, value, D, examined):
        '''Returns new domains for participating variables.'''
        newdomains = {}
        for _var in examined:
            if not value in D[_var]:
                return CONTRADICTION
            elif len(D[_var]) == 1:
                continue
            newdomains[_var] = {value}
        return newdomains
             
    def establish(self, csp, curvar, value, participants):
        '''Establishes consistency after assignment curvar: value.'''
        A = csp.get_assignment()
        examined = set([])
        for v in {"R1", "R2", "R3", "R4", "R5", "R6", "R7"}:
            if v in A and v != curvar:
                return REVISED_NONE
            if not v in A and v != curvar:
                examined.add(v)
        D = csp.get_domains()
        newdomains = self.__new_domains(value, D, examined)
        reduced = set([])
        if newdomains == CONTRADICTION:
            return CONTRADICTION
        if len(newdomains.keys()) == 0:
            return ALREADY_CONSISTENT
        for vi, new_domain in newdomains.items():
            csp.update_domain(vi, new_domain)
            reduced.add(vi)
        return (MADE_CONSISTENT, reduced)