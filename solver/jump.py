import copy
from constants import *

class JUMP():
    '''Implements the backjumping mechanism through conflict sets.'''

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
        
    def unaccumulate(self, curvar):
        '''Removes curvar: value from all confsets.'''
        for _var in self.__confsets.keys():
            if curvar in self.__confsets[_var]:
                del self.__confsets[_var][curvar]

    def canbackjump(self, curvar):
        '''Is there any variable in conflict with curvar?
        
        i.e. did any assignment in the past make curvar or subsequent
        variables shed values?'''
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