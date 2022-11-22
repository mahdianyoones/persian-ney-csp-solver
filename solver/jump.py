import copy
from constants import *

class JUMP():
    '''Implements the backjumping mechanism through conflict sets.
    
        The core notion of a conflict set is to create a time machine where
        jumping happens to the nearest conflicting past, if any.
        
        Example:
        
        D1 is assigned 18
        
        If by establishing this assignment, L7 sheds some values,
        L7's has now a conflict set:

        {
            D1: 18
        }

        Later, T7 is assigned 2 which impacts L7 too. L7's conflict set
        accumulates this assignment as well:

        {
            D1: 18,
            T7: 2
        }
        
        Some time later, when L7 is selected for assignment, its domain gets
        drained hence prompting a jump back. 

        Assume the assignments are as follows:

        D1, D2, D3, T7, T1, T2, T3, L7

        T7 is selected as a jump target since it's the latest assigned
        variable in the conflict set of L7.

        Jumping must happen to the near past not distant past.
        
        Why would we repeat a long history? Why not jump to yesterday and
        make a tiny change and quicky get back to today?
        
        If we jumped to the last year instead, we would have to repeat a
        full year again to see if that solves the issue of today!

        Also, when jump happens to a variable, since it's value is changed,
        it must be removed from the conflict set of variables that it
        conflicted with before.

        i.e. assigning different values to the same variable may cause
        different variables shed values.
        
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
        when a bad decision was made) abrobs the conflict set of the jump
        origin.

        If making different decisions at the jumped-to date does not fix
        the problem, people at this date know what to do; if future people
        have provided them with a set of suspicious dates, further jumping
        happens according to that set.'''

    def __init__(self):
        self.__confsets = {}

    def accumulate(self, curvar, value, reduced_vars):
        '''Accumulates the conflict set for curvar.'''
        if len(reduced_vars) == 0:
            return
        for v in reduced_vars:
            if not v in self.__confsets:
                self.__confsets[v] = {}
            self.__confsets[v][curvar] = value

    def absorb(self, target, origin):
        '''Absorbs conflict set from jump origin.'''
        if not origin in self.__confsets:
            return # nothing to absrob
        if not target in self.__confsets:
            self.__confsets[target] = {}
        for v, val in self.__confsets[origin].items():
            if v == target:
                continue
            self.__confsets[target][v] = val
        
    def unaccumulate(self, A, curvar):
        '''Removes curvar: value from all confsets.'''
        for _var in self.__confsets.keys():
            if curvar in self.__confsets[_var]:
                del self.__confsets[_var][curvar]

    def canbackjump(self, curvar):
        '''Is there any variable in conflict with curvar?
        
        i.e. did any assignment in the past make curvar shed values?'''
        if curvar in self.__confsets:
            if len(self.__confsets[curvar].keys()) > 0:
                return True
        return False
    
    def jump_target(self, csp, curvar):
        '''Returns the most recent assignment in conflict with curvar.'''
        A = csp.get_assigned_vars()
        for i in range(len(A) - 1, -1, -1):
            jump_target = A[i]
            if jump_target in self.__confsets[curvar]:
                return jump_target
        raise Exception("Jump target does not exists!")

    def get_confset(self, var):
        return self.__confsets[var]