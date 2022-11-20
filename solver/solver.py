from spec import specs
from csp import CSP
from mac import MAC
from catalog import CATALOG
from pickup import SELECT
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
        if result == CONTRADICTION:
            self.__unassign(csp, curvar)
            return INCONSISTENT_ASSIGNMENT
        if isinstance(result, tuple) and result[0] == MADE_CONSISTENT:
            reduced_vars.update(result[1])
        return (CONSISTENT_ASSIGNMENT, reduced_vars)
    
    def __unassign(self, csp, curvar):
        csp.unassign(curvar)
        csp.revert_domains() # undo establish and propagation effects

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
        domain = copy.deepcopy(csp.get_domain(curvar))
        while True:
            if self.__select.domain_exhausted(curvar, domain):
                if csp.assigned_count() == 0:
                    return (SEARCH_SPACE_EXHAUSTED, None)
                if self.__jump.canbackjump(curvar):
                    jump_origin = curvar
                    jump_target = self.__jump.jump_target(csp, curvar)
                    return (BACKJUMP, jump_origin, jump_target)
                return (BACKTRACK, None)
            val = self.__select.nextval(curvar, domain)		
            assign_res = self.__assign(curvar, val)
            if assign_res == INCONSISTENT_ASSIGNMENT:
                continue # try the next value
            if csp.unassigned_count() == 0: # solution
                return (SOLUTION, csp.get_assignment())
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
    
    def find(self, catalog, spec):
        '''Runs MAC for all variables first and then calls DFS.
        
        If MAC figures out any contradiction before search begins, no
        solution could ever be found.'''
        res = UNARY.init_domains(self.__csp, catalog)
        if res == CONTRADICTION:
            return CONTRADICTION
        res = UNARY.unarify(self.__csp, spec)
        if res == CONTRADICTION:
            return CONTRADICTION
        X = copy.deepcopy(self.__csp.get_variables())
        res = self.__mac.propagate(X)
        if res == CONTRADICTION:
            return CONTRADICTION
        return self.__dfs()

def human_readable(solution):
    '''Prints a prettified view of the given solution.'''
    for v in ["L1", "L2", "L3", "L4", "L5", "L6", "L7"]:
        print(v, ": ", solution[v])
    for v in ["D1", "D2", "D3", "D4", "D5", "D6", "D7"]:
        print(v, ": ", solution[v])
    print("T: ", solution["T1"])
    print("R: ", solution["R1"])

def main():
    catalog = CATALOG(current+"/pieces.csv")
    for kook in {"F_tall", "G", "A", "Bb", "C", "D", "E", "F_short"}:
        csp = CSP()
        select = SELECT(csp)
        mac = MAC(csp, catalog, specs[kook])
        solver = SOLVER(csp, select, mac)
        res = solver.find(catalog, specs[kook])
        if res[0] == SOLUTION:
            print("\nSolution for ", kook, "\n")
            human_readable(res[1])
        else:
            print("\nNo solution for ", kook, "\n")
if __name__ == "__main__":	
    main()
