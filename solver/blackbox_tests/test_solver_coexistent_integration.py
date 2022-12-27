import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
sp.append(parent)

from solver import SOLVER
from csp import CSP
from testspec import specs
from unary import UNARY
from mac import MAC
from pickup import SELECT
from constants import *

@unittest.skip("")
class test_SOLVER_COEXISTENT_INTEGRATION(unittest.TestCase):

    NO_SOLUTION_DS = "contains_no_solution"
    SOLUTION_DS = "contains_solutions"
    REAL_DS = "real_pieces"

    def __find(self, catalog, spec, csp = None):
        '''Generalises arrange and act of all test cases in this suite.'''
        csp = CSP()
        select = SELECT(csp)
        mac = MAC(csp, catalog, spec)
        UNARY.init_domains(csp, catalog)
        UNARY.unarify(csp, spec)
        sut = SOLVER(csp, select, mac)
        res = sut.find_coexistent(catalog, spec)
        return res

    def __find_coexistent_solutions(self, dataset, _specs):
        data_set_path = current+"/"+dataset+".csv"
        catalog = CATALOG(data_set_path)
        coex_solutions = {}
        for kook, _spec in _specs.items():
            res = self.__find(catalog, _spec)
            if res[0] == SOLUTION:
                coex_solutions[kook] = res[1]
        return coex_solutions

    def test_finds_solutions_for_some_kooks_among_artificial_data(self):
        kooks = ["F_short", "E", "D", "C", "Bb", "A", "G", "F_tall"]
        dsname = "contains_solutions"
        _specs = {kook: specs[kook] for kook in kooks}
        coex_solutions = self.__find_coexistent_solutions(dsname, _specs)
        self.assertTrue(len(coex_solutions) >= 1)

    def test_finds_solutions_for_all_kooks_among_artificial__data(self):
        dsname = "contains_all_coexistent_solutions"
        kooks = ["F_short", "E", "D", "C", "Bb", "A", "G", "F_tall"]
        _specs = {kook: specs[kook] for kook in kooks}
        coex_solutions = self.__find_coexistent_solutions(dsname, _specs)
        self.assertEqual(len(coex_solutions), len(kooks))

    def test_finds_solutions_for_some_kooks_among_real_data(self):
        kooks = ["F_short", "E", "D", "C", "Bb", "A", "G", "F_tall"]
        dsname = "real_pieces"
        _specs = {kook: specs[kook] for kook in kooks}
        coex_solutions = self.__find_coexistent_solutions(dsname, _specs)
        self.assertTrue(len(coex_solutions) >= 1)

if __name__ == "__main__":
    unittest.main()