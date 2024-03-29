import os
from sys import path as sp
from spec import specs
from solver import SOLVER
from csp import CSP
from unary import UNARY
from mac import MAC
from pickup import SELECT
from constants import *
from verify import is_valid
from pretty_print import print_solution, print_stats

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sp.append(parent)

def main():
    regs = ["A", "Bb", "C", "D", "Bb", "C"]
    data_set_path = current+"/pieces.csv"
    csp = CSP(S=len(regs))
    select = SELECT()
    mac = MAC()
    UNARY.init_domains(csp, data_set_path)
    specs_sorted = [specs[reg] for reg in regs]
    res = UNARY.unarify(csp, specs_sorted)
    if res == CONTRADICTION:
        print("No solution could exist. Unary constaints violated!")
    stats = {"nodes": 0, "backjumps": 0, "backtracks": 0}
    solver = SOLVER(select, mac, stats)
    statf = open("stats.txt", "w")
    indicator, solution = solver.find(csp, specs_sorted, data_set_path, statf)
    if indicator == SOLUTION:
        if is_valid(solution, specs_sorted):
            print("Found a solution: ")
            msg = print_solution(solution, regs)
            statf.write(msg)
        else:
            msg = "Found a solution, but invalid!:"
            msg += print_solution(solution, regs)
            statf.write(msg)
    else:
        msg += "Could not find a solution."
        statf.write(msg)
    msg = print_stats(stats)
    statf.write(msg)
    statf.close()

if __name__ == "__main__":
    main()