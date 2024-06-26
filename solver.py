from jump import JUMP
from constants import *
from unary import UNARY
import copy
import os
import time, datetime
from pretty_print import print_stats

current = os.path.dirname(os.path.realpath(__file__))

class SOLVER():

    START_TIME = 0

    def __init__(self, select, mac, stats):
        self.__csp = None
        self.__select = select
        self.__mac = mac
        self.__jump = JUMP()
        self.__stats = stats
        self.__start_ts = 0

    def __assign(self, curvar, value):
        '''Tries assigning curvar: value.'''
        csp = self.__csp
        csp.assign(curvar, value)
        csp.backup_domains()
        result = self.__mac.establish(csp, self.__specs_sorted, curvar, value)
        reduced_vars = set([])
        if result[0] == CONTRADICTION:
            self.__unassign(csp, curvar)
            return (INCONSISTENT_ASSIGNMENT, result[1])
        if isinstance(result, tuple) and result[0] == MADE_CONSISTENT:
            reduced_vars.update(result[1])
        return (CONSISTENT_ASSIGNMENT, reduced_vars)
    
    def __unassign(self, csp, curvar):
        csp.unassign(curvar)
        csp.revert_domains() # undo establish and propagation effects
        self.__jump.unaccumulate(curvar)

    def __dfs(self):
        '''Recursively assigns values to variables to find a solution.
        
        When the domain of a variable is exhausted without any solution
        being found, the algorithm marks this as a new constraint and do
        not backjump to the last variable (yesterday), since backtracking
        occurs anyway.
        
        This case does not occur more than once before termination. However,
        adding this contradiction to a new constraint may help optimization 
        in the next phase of the project.
        '''
        if time.time() - self.START_TIME > 900:
            return TIMEDOUT, TIMEDOUT
        csp = self.__csp
        curvar = self.__select.nextvar(csp)
        values = csp.get_shuffled_values(curvar)
        self.__stats["nodes"] += 1
        if self.__stats["nodes"] % 500 == 0:
            time.sleep(1)
            if self.__stats["nodes"] % 1000 == 0:
                msg = print_stats(self.__stats)
                seconds_elapsed = int(time.time() - self.__start_ts)
                seconds_elapsed -= (self.__stats["nodes"] // 1000)
                msg += "\n"
                msg += str(datetime.timedelta(seconds=seconds_elapsed)) + "\n"
                self.__statfile.write(msg)
                self.__statfile.flush()
        while True:
            if len(values) == 0:
                if csp.assigned_count() == 0:
                    return (SEARCH_SPACE_EXHAUSTED, None)
                if self.__jump.canbackjump(curvar):
                    jump_origin = curvar
                    jump_target = self.__jump.jump_target(csp, curvar)
                    return (BACKJUMP, jump_origin, jump_target)
                return (BACKTRACK, None)
            val = values.pop()	
            assign_res = self.__assign(curvar, val)
            if assign_res[0] == INCONSISTENT_ASSIGNMENT:
                for failed_var in assign_res[1]:
                    self.__jump.absorb(curvar, failed_var)
                continue # try the next value
            if csp.unassigned_count() == 0: # solution
                return (SOLUTION, csp.get_assignment())
            self.__jump.accumulate(curvar, val, assign_res[1])
            dfs_res = self.__dfs()
            if dfs_res[0] in {SOLUTION, SEARCH_SPACE_EXHAUSTED}:
                return dfs_res
            if dfs_res[0] == TIMEDOUT:
                return dfs_res
            self.__unassign(csp, curvar)
            if dfs_res[0] == BACKTRACK:
                self.__stats["backtracks"] += 1
                continue
            if dfs_res[0] == BACKJUMP:
                if dfs_res[2] != curvar:
                    return dfs_res
                else:
                    self.__stats["backjumps"] += 1
                    jump_origin = dfs_res[1]
                    jump_target = dfs_res[2]
                    self.__jump.absorb(jump_target, jump_origin)
                    continue

    def find(self, csp, specs_sorted, data_set_path, statf):
        '''Runs MAC for all variables first and then calls DFS.
        
        If MAC figures out any contradiction before search begins, no
        solution could ever be found.'''
        self.START_TIME = time.time()
        self.__csp = csp
        self.__specs_sorted = specs_sorted
        res = UNARY.init_domains(self.__csp, data_set_path)
        if res == CONTRADICTION:
            return CONTRADICTION
        res = UNARY.unarify(self.__csp, specs_sorted)
        if res == CONTRADICTION:
            return CONTRADICTION
        X = copy.copy(self.__csp.get_variables())
        res = self.__mac.propagate(csp, specs_sorted, X)
        if res == CONTRADICTION:
            return CONTRADICTION
        self.__start_ts = time.time()
        self.__statfile = statf
        return self.__dfs()