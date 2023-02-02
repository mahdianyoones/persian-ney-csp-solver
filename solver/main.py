import os
from sys import path as sp
import json
from spec import specs
from solver import SOLVER
from csp import CSP
from unary import UNARY
from mac import MAC
from pickup import SELECT
from constants import *
from verify import is_valid

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sp.append(parent)

def main():
    kook = "Bb"
    data_set_path = current+"/pieces.csv"
    csp = CSP()
    select = SELECT(csp)
    mac = MAC(csp, specs[kook])
    UNARY.init_domains(csp, data_set_path)
    res = UNARY.unarify(csp, specs[kook])
    if res == CONTRADICTION:
        print("No solution could exist. Unary constaints violated!")
    solver = SOLVER(csp, select, mac)
    indicator, solution = solver.find_independent(specs[kook], data_set_path)
    if indicator == SOLUTION:
        if is_valid(solution, kook):
            print("Found a solution: ")
            print(json.dumps(solution, indent=4))
        else:
            print("Found a solution, but invalid!:")    
            print(json.dumps(solution, indent=4))
    else:
        print("Could not find a solution.")
        
if __name__ == "__main__":
    main()