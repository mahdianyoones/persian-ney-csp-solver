from spec import specs
from csp import CSP
from mac import MAC
from catalog import CATALOG
from pickup import SELECT
from conflict import CONFLICT
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
        self.__confset = CONFLICT(csp.get_variables())
                            
    def __assign(self, curvar, value):
        '''Tries assigning curvar: value.
        
        If the assignment would cause coontradiction, a conflict set is
        returned.
        
        Note: If the contradiction occurs due to propagation, no conflict set
        is returned. In fact, only curvar is responsible for this.'''
        csp = self.__csp
        csp.assign(curvar, value)
        res = self.__mac.establish(curvar, value)
        if res[0] == CONTRADICTION:
            return (INCONSISTENT_ASSIGNMENT, res[2])
        if res[0] == DOMAINS_REDUCED:
            propagate_res = self.__mac.propagate(res[2])
            if propagate_res[0] == CONTRADICTION:
                return (INCONSISTENT_ASSIGNMENT, set([]))
        return (CONSISTENT_ASSIGNMENT, set([]))
        
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
        if csp.unassigned_count() == 0: # solution
            return (SOLUTION, csp.get_assignment())
        curvar = self.__select.nextvar(csp)
        domain = copy.deepcopy(csp.get_domain(curvar))
        while True:
            val = self.__select.nextval(curvar, domain)				
            if val == DOMAIN_EXHAUSTED:
                if csp.assigned_count() == 0:
                    return (SEARCH_SPACE_EXHAUSTED, None)
                if self.__confset.canbackjump(curvar):
                    (confvars, jump_target) = self.__confset.backjump(curvar)
                    return (BACKJUMP, confvars, jump_target)
                return (BACKTRACK, None)
            csp.backup_domains()
            assign_res = self.__assign(curvar, val)
            if assign_res[0] == INCONSISTENT_ASSIGNMENT:
                confvars = assign_res[1]
                self.__confset.accumulate(csp, curvar, confvars)
                csp.unassign(curvar)
                csp.revert_domains() # undo establish and propagation effects
                continue # try the next value
            dfs_res = self.__dfs()
            if dfs_res[0] in {SOLUTION, SEARCH_SPACE_EXHAUSTED}:
                return dfs_res
            csp.unassign(curvar)
            csp.revert_domains()
            if dfs_res[0] == BACKTRACK:
                continue
            if dfs_res[0] == BACKJUMP:
                if dfs_res[2] != curvar:
                    return dfs_res
                else:
                    confvars = dfs_res[1]
                    self.__confset.absorb(csp, curvar, confvars)
                    continue
    
    def find(self, catalog, spec):
        '''Runs MAC for all variables first and then calls DFS.
        
        If MAC figures out any contradiction before search begins, no
        solution could ever be found.'''
        UNARY.unarify(self.__csp, catalog, spec)
        X = copy.deepcopy(self.__csp.get_variables())
        res = self.__mac.propagate(X)
        if res[0] == CONTRADICTION:
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
    csp = CSP()
    select = SELECT(csp)
    mac = MAC(csp, catalog, specs["C"])
    solver = SOLVER(csp, select, mac)
    res = solver.find(catalog, specs["C"])
    if res[0] == SOLUTION:
        human_readable(res[1])
    else:
        print("No solution was found!")
            
if __name__ == "__main__":	
    main()
