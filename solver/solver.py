from spec import specs
from jump import JUMP
from constants import *
from unary import UNARY
import copy
import os

current = os.path.dirname(os.path.realpath(__file__))

class SOLVER():

    def __init__(self, csp, select, mac):
        self.__csp = csp
        self.__select = select
        self.__mac = mac
        self.__jump = JUMP()
                            
    def __assign(self, curvar, value):
        '''Tries assigning curvar: value.'''
        csp = self.__csp
        csp.assign(curvar, value)
        csp.backup_domains()
        result = self.__mac.establish(curvar, value)
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
        csp = self.__csp
        curvar = self.__select.nextvar(csp)
        values = csp.get_values(curvar)
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
                continue
            self.__jump.accumulate(curvar, val, assign_res[1])
            dfs_res = self.__dfs()
            if dfs_res[0] in {SOLUTION, SEARCH_SPACE_EXHAUSTED}:
                return dfs_res
            self.__unassign(csp, curvar)
            if dfs_res[0] == BACKTRACK:
                continue # May not happen at all!
            if dfs_res[0] == BACKJUMP:
                if dfs_res[2] != curvar:
                    return dfs_res
                else:
                    jump_origin = dfs_res[1]
                    jump_target = dfs_res[2]
                    self.__jump.absorb(jump_target, jump_origin)
                    continue
    
    def find_independent(self, catalog, spec):
        '''Runs MAC for all variables first and then calls DFS.
        
        If MAC figures out any contradiction before search begins, no
        solution could ever be found.'''
        res = UNARY.init_domains(self.__csp, catalog)
        if res == CONTRADICTION:
            return CONTRADICTION
        res = UNARY.unarify(self.__csp, spec)
        if res == CONTRADICTION:
            return CONTRADICTION
        X = copy.copy(self.__csp.get_variables())
        res = self.__mac.propagate(X)
        if res == CONTRADICTION:
            return CONTRADICTION
        return self.__dfs()

    def __remove_solution_nodes(self, catalog, solution):
       for i in range(1, 8):
            i = str(i)
            Li = "L" + i
            Pi = "P" + i
            Ti = "T" + i
            Di = "D" + i
            Ri = "R" + i
            Psol, Tsol, Dsol = solution[Pi], solution[Ti], solution[Di]
            Rsol, Lsol = solution[Ri], solution[Li]
            catalog.remove_piece(Psol, Tsol, Dsol, Rsol)
            no_sol, l_piece = Psol
            if l_piece > Lsol:
                no_new = no_sol + "+"
                Lnew = l_piece - Lsol
                catalog.add_piece(no_new, Lnew, Tsol, Dsol, Rsol)

    def find_coexistent(self, catalog, spec):
        '''Runs MAC for all variables first and then calls DFS.
        
        If MAC figures out any contradiction before search begins, no
        solution could ever be found.'''
        res = self.find_independent(catalog, spec)
        if res[0] == SOLUTION:
            solution = res[1]
            self.__remove_solution_nodes(catalog, solution)
        return res