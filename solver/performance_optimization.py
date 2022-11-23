import cProfile
import pstats
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
sp.append(parent)

from solver import SOLVER
from csp import CSP
from spec import specs
from catalog import CATALOG
from unary import UNARY
from mac import MAC
from pickup import SELECT
from constants import *

NO_SOLUTION_DS = "contains_no_solution"
SOLUTION_DS = "contains_solutions"
REAL_DS = "real_pieces"

def __find(catalog, kook, csp = None):
    '''Generalises arrange and act of all test cases in this suite.'''
    if csp == None:
        csp = CSP()
    select = SELECT(csp)
    mac = MAC(csp, catalog, specs[kook])
    UNARY.init_domains(csp, catalog)
    UNARY.unarify(csp, specs[kook])
    solver = SOLVER(csp, select, mac)
    res = solver.find_independent(catalog, specs[kook])
    return res

def main():
    data_set_path = current+"/pieces.csv"
    catalog = CATALOG(data_set_path)
    res = __find(catalog, "C")

if __name__ == "__main__":
    cProfile.run("main()", "speed_profile")
    p = pstats.Stats('speed_profile')
    p.strip_dirs()
    p.sort_stats(pstats.SortKey.TIME).print_stats(1).print_callers(.1)