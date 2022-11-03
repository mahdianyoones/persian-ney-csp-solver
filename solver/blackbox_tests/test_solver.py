import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
sp.append(parent)

import unittest
from solver import SOLVER
from csp import CSP
from testspec import specs
from catalog import CATALOG
from mac import MAC
from pickup import SELECT
from constants import *

class test_SOLVER(unittest.TestCase):

    def __find(self, catalog, kook):
        '''Generalises arrange and act of all test cases in this suite.'''
        csp = CSP()
        select = SELECT(csp)
        mac = MAC(csp, catalog, specs[kook])
        sut = SOLVER(csp, select, mac)
        res = sut.find(catalog, specs[kook])
        return res

    def test_finds_solutions_4_all_kooks_real_pieces(self):
        data_set_path = current+"/real_pieces.csv"
        catalog = CATALOG(data_set_path)
        for kook in {"F_tall", "G", "A", "Bb", "C", "D", "E", "F_short"}:
            res = self.__find(catalog, kook)
            self.assertEqual(res[0], SOLUTION)

    def test_finds_solutions_4_all_kooks(self):
        data_set_path = current+"/contains_solutions.csv"
        catalog = CATALOG(data_set_path)
        for kook in {"F_tall", "G", "A", "Bb", "C", "D", "E", "F_short"}:
            res = self.__find(catalog, kook)
            self.assertEqual(res[0], SOLUTION)
            
    def test_finds_no_solution(self):
        data_set_path = current+"/contains_no_solution.csv"
        catalog = CATALOG(data_set_path)
        for kook in {"F_tall", "G", "A", "Bb", "C", "D", "E", "F_short"}:
            res = self.__find(catalog, kook)
            self.assertNotEqual(res[0], SOLUTION)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_SOLVER)
    runner.run(suite)