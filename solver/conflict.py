from constants import *

class CONFLICT():
    '''Implements the conflict set.'''

    def __init__(self, X):
        self.__confsets = {v: [] for v in X}

    def accumulate(self, csp, curvar, confvars):
        '''Accumulates the conflict set for curvar.
        
        Conflict set must be sorted based on the time of assignment.
        The core notion of a conflict set is to create a time machine where
        order of variables in the set must follow the order of variables in 
        the assignment.
        
        Example:
        
        D1 -> R1 -> T1 -> L1 (if failes due to T1 and D1)
        
        confset[L1] = [D1, T1] so that jump happens first to T1 not D1
        
        Jumping must happen to the near past not distant past.
        
        Why would we repeat a long history? Why not jump to yesterday and
        make a tiny change and quicky get back to today?
        
        If we jumped to the last year instead, we would have to repeat a
        full year again to see if that solves the issue of today!
        '''
        if len(confvars) == 0:
            return
        A = csp.get_assignment() # time sorted
        confset = self.__confsets[curvar]	
        confvars = self.__confvars(A, confvars, confset, curvar)
        if len(confvars) > 0:
            self.__confsets[curvar].extend(confvars)

    def absorb(self, csp, curvar, confvars):
        '''Absorbs conflict set from jump origin.
        
        Current variable incorporates in itself the conflict set of the
        variable that has failed in the future.
        
        This failure in the future happens due to legal assignments at
        some time in the past. Conflict set provides a time machine
        to travel back to the time when people made good moves, but
        future proves it wrong!
        
        People may not be able to see the effect of their actions far enough
        because it takes too much time to consider every scenario.
        '''
        if len(confvars) == 0:
            return
        A = csp.get_assignment() # time sorted
        confset = self.__confsets[curvar]		
        confvars = self.__confvars(A, confvars, confset, curvar)
        if len(confvars) > 0:
            self.__confsets[curvar].extend(confvars)

    def canbackjump(self, curvar):
        return curvar in self.__confsets and len(self.__confsets[curvar]) > 0
    
    def backjump(self, curvar):
        jump_target = self.__confsets[curvar][-1]
        confvars = self.__confsets[curvar]
        return (confvars, jump_target)

    def __confvars(self, A, inconsistents, confset, curvar):
        '''Decides which variables can be added to the conflict set.
        
        Returns conflicting variables in the order of assignment.'''
        confvars = []
        for var in A:
            if not var in inconsistents:
                continue
            if var == curvar: # would be redundant
                continue
            if var in confset: # prevent duplicates
                continue
            confvars.append(var)
        return confvars