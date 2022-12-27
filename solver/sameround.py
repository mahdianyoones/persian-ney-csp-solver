from constants import *

class SAMEROUND():
    '''Applies same roundness constraints.'''
    
    def propagate(self, csp, reduced_vars, participants):
        '''Establishes indirect consistency W.R.T. same_r.'''
        return REVISED_NONE
    
    def __new_domains(self, value, D, revising_vars):
        '''Returns new domains for participating variables.'''
        newdomains = {}
        assigned_roundness = value[3]
        for revising_var in revising_vars:
            newdomains[revising_var] = set([])
            for piece in D[revising_var]:
                if piece[3] == assigned_roundness:
                    newdomains[revising_var].add(piece)
            if len(newdomains[revising_var]) == 0:
                return CONTRADICTION
            elif D[revising_var] == newdomains[revising_var]:
                del newdomains[revising_var]
                continue
        return newdomains
             
    def establish(self, csp, curvar, value, participants):
        '''Establishes consistency after assignment curvar: value.'''
        A = csp.get_assignment()
        revising_vars = set([])
        for v in participants: # P1 thorugh P7
            if v in A and v != curvar:
                return REVISED_NONE
            if not v in A and v != curvar:
                revising_vars.add(v)
        D = csp.get_domains()
        newdomains = self.__new_domains(value, D, revising_vars)
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
        participants = {"P1", "P2", "P3", "P4", "P5", "P6", "P7"}
        unassigned = csp.get_unassigned_vars()
        return participants.intersection(unassigned)            