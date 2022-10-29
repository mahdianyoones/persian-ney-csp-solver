import copy
from constants import *

class JUMP():
    '''Implements the backjumping mechanism through conflict sets.'''

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
        existing_confvars = set(self.__confsets[curvar])
        new_confvars = []
        for var in A:
            if var in existing_confvars or var in confvars:
                if var != curvar:
                    new_confvars.append(var)
        self.__confsets[curvar] = new_confvars

    def absorb(self, csp, curvar, confvars):
        '''Absorbs conflict set from jump origin.
        
        Current variable incorporates in itself the conflict set of the
        variable that has failed in the future.
        
        This failure in the future happens due to legal assignments at
        some time in the past.
        
        Conflict set provides a time machine to travel back to the time when
        people made supposedly good moves, but future has proved them wrong!
        
        People may not be able to see the effect of their actions far enough
        because it takes too much time to consider every scenario.

        When backjumping happens (going back to the past), it may turn out
        that further backjumping is needed. i.e. the future people know
        that a wrong decision was made in SOME TIME in the past.
        
        This time may be one of the several dates at hand (conflicting 
        variables), but it is unknown which one is exactly the one--the
        change of which fixes the problem.

        That's why the destination of jump (one of the suspicious dates
        when a bad decision was made) receives the confvars. Confvars is 
        the set of dates, one of which may fix the issue.

        If making different decisions at the jumped-to date does not fix
        the problem, people at this date know what to do; if future people
        have provided them with a set of suspicious dates, further jumping
        happens according to that set.'''
        if len(confvars) == 0:
            return
        A = csp.get_assignment() # time sorted
        existing_confvars = set(self.__confsets[curvar])
        new_confvars = []
        for var in A:
            if var in existing_confvars or var in confvars:
                if var != curvar:
                    new_confvars.append(var)
        self.__confsets[curvar] = new_confvars

    def canbackjump(self, curvar):
        return curvar in self.__confsets and len(self.__confsets[curvar]) > 0
    
    def backjump(self, curvar):
        jump_target = self.__confsets[curvar][-1]
        confvars = copy.deepcopy(self.__confsets[curvar])
        self.__confsets[curvar] = []
        return (confvars, jump_target)

    def get_confset(self, var):
        return self.__confsets[var]