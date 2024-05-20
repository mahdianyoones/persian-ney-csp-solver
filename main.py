import os
import copy
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

def run(regs):
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
    statf = open("stats.txt", '+a')
    statf.write('Desired instruments: ' + ', '.join(regs) + "\n\n")
    indicator, solution = solver.find(csp, specs_sorted, data_set_path, statf)
    success = False
    if indicator == SOLUTION:
        if is_valid(solution, specs_sorted):
            print("Found a solution: ")
            msg = print_solution(solution, regs)
            statf.write(msg)
            success = True
        else:
            msg = "Found a solution, but invalid!:"
            msg += print_solution(solution, regs)
            statf.write(msg)
    else:
        msg = "\n\nCould not find a solution."
        msg = f"{msg}  -  cause: {indicator}\n\n"
        print(msg)
        statf.write(msg)
    msg = print_stats(stats)
    statf.write(msg)
    statf.close()
    return success

def generate_desired_instruments():
    # total length of all pieces are 40,520 millimeters
    # the length of a C instrument = 524
    # average number of all instruments possible = 77
    fixed_wanted = ["G", "A", "D"]
    output = []
    for i in range(1, 10):
        possibility = copy.deepcopy(fixed_wanted)
        possibility.extend(["Bb"] * i)
        possibility.extend(["C"] * i)
        output.append(possibility)
    return output

if __name__ == "__main__":
    run(['C'])
    # possibilities = generate_desired_instruments()
    # while True:
    #     if len(possibilities) == 0:
    #         break
    #     regs = possibilities.pop()
    #     success = run(regs)
    #     if success:
    #         break