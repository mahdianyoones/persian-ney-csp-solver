import os
from sys import path as sp
import json
from spec import specs
from solver import SOLVER
from csp import CSP
from catalog import CATALOG
from unary import UNARY
from mac import MAC
from pickup import SELECT
from constants import *
from verify import is_valid

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sp.append(parent)

def main():
    kook = "F_short"
    data_set_path = current+"/pieces.csv"
    catalog = CATALOG(data_set_path)
    csp = CSP()
    select = SELECT(csp)
    mac = MAC(csp, catalog, specs[kook])
    UNARY.init_domains(csp, catalog)
    res = UNARY.unarify(csp, specs[kook])
    if res == CONTRADICTION:
        print("No solution could exist. Unary constaints violated!")
    solver = SOLVER(csp, select, mac)
    indicator, solution = solver.find_independent(catalog, specs[kook])
    if is_valid(solution, catalog, kook):
        print("Found a solution: ")
        print(json.dumps(solution, indent=1))
 
if __name__ == "__main__":
    main()