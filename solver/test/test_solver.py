import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import unittest
from solver import SOLVER
from csp import CSP
from spec import specs
from catalog import CATALOG
from mac import MAC
from pickup import SELECT
from constants import *

class test_SOLVER(unittest.TestCase):

    def __find(self, data_set_path, kook):
        '''Generalises arrange and act of all test cases in this suite.'''
        catalog = CATALOG(data_set_path)
        csp = CSP()
        select = SELECT(csp)
        mac = MAC(csp, catalog, specs[kook])
        sut = SOLVER(csp, select, mac)
        res = sut.find(catalog, specs[kook])
        return res

    def test_finds_solutions_4_all_kooks(self):
        data_set_path = current+"/contains_solutions.csv"
        for kook in {"F_tall", "G", "A", "Bb", "C", "D", "E", "F_short"}:
            res = self.__find(data_set_path, kook)
            self.assertEqual(res[0], SOLUTION)
            
    def test_finds_no_solution(self):
        data_set_path = current+"/contains_no_solution.csv"
        for kook in {"F_tall", "G", "A", "Bb", "C", "D", "E", "F_short"}:
            res = self.__find(data_set_path, kook)
            self.assertNotEqual(res[0], SOLUTION)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_SOLVER)
    runner.run(suite)