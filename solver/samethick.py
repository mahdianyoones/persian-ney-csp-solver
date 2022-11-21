from constants import *

class SAMETHICK():
    '''Applies same thickness constraints.
    
    The variables T1 Trought T7 must have the same value in the
    final solution.'''
    
    def propagate(self, csp, reduced_vars, participants):
        '''Establishes indirect consistency W.R.T. same_th.'''
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
        for v in {"T1", "T2", "T3", "T4", "T5", "T6", "T7"}:
            if v in A and v != curvar:
                return REVISED_NONE
            if not v in A and v != curvar:
                examined.add(v)
        D = csp.get_domains()
        newdomains = self.__new_domains(value, D, examined)
        reduced = set([])
        if newdomains == CONTRADICTION:
            return (CONTRADICTION, self.__failed_set(csp))
        if len(newdomains.keys()) == 0:
            return ALREADY_CONSISTENT
        for vi, new_domain in newdomains.items():
            csp.update_domain(vi, new_domain)
            reduced.add(vi)
        return (MADE_CONSISTENT, reduced)

    def __failed_set(self, csp):
        '''Returns the failed set.'''
        participants = {"T1", "T2", "T3", "T4", "T5", "T6", "T7"}
        unassigned = csp.get_unassigned_vars()
        return participants.intersection(unassigned)                    