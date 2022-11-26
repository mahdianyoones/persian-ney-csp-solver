import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
sp.append(parent)

from spec import specs
from solver import SOLVER
from csp import CSP
from catalog import CATALOG
from unary import UNARY
from mac import MAC
from pickup import SELECT
from constants import *
from verify import is_valid

def find():
    kook = "A"
    data_set_path = current+"/pieces.csv"
    catalog = CATALOG(data_set_path)
    csp = CSP()
    select = SELECT(csp)
    mac = MAC(csp, catalog, specs[kook])
    UNARY.init_domains(csp, catalog)
    UNARY.unarify(csp, specs[kook])
    solver = SOLVER(csp, select, mac)
    solutions, solutions_counter = solver.find_independent(catalog, specs[kook], find_all = True)
    print("Found: {:} solutions".format(solutions_counter))
    valid_counter = 0
    for solution in solutions:
        if is_valid(solution, catalog, kook):
            valid_counter += 1
    if valid_counter == len(solutions):
        print("Verified {a:} solutions, {b:} are valid".format(a=len(solutions), b=valid_counter))
        
def main():
    find()

if __name__ == "__main__":
    main()