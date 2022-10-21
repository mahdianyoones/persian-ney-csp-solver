from constants import *

class SAMETHICK():
    '''Applies same thickness constraints.
    
    Te variables T1 Trought T7 must have the same value in the
    final solution.'''
    
    def propagate(self, csp, reduced_vars):
        '''Establishes indirect consistency W.R.T. same_th.'''
        return (DOMAINS_INTACT, set([]))
    
    def __new_domains(self, value, D):
        '''Returns new domains for participating variables.
        
        This is a mathematical function.'''
        newdomains = {}
        for _var in {"T2", "T3", "T4", "T5", "T6", "T7"}:
            if not value in D[_var]:
                return CONTRADICTION
            elif len(D[_var]) == 1:
                continue
            newdomains[_var] = {value}
        return newdomains
             
    def establish(self, csp, curvar, value):
        '''Establishes consistency W.R.T. same_t constraint.
        
        W.R.T. the assignment curvar: value.'''
        if curvar != "T1":
            return (DOMAINS_INTACT, set([]))
        D = csp.get_domains()
        newdomains = self.__new_domains(value, D)
        examined_vars = {"T2", "T3", "T4", "T5", "T6", "T7"}
        reduced = set([])
        if newdomains == CONTRADICTION:
            return (CONTRADICTION, examined_vars, set([]))
        if len(newdomains.keys()) == 0:
            return (DOMAINS_INTACT, examined_vars)
        for vi, new_domain in newdomains.items():
            if len(new_domain) < len(D[vi]):
                csp.update_domain(vi, new_domain)
                reduced.add(vi)
        return (DOMAINS_REDUCED, examined_vars, reduced)