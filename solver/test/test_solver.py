import unittest
import sys
import os

from catalog import CATALOG
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

    @unittest.skip
    def test_finds_a_solution_4_all_cooks(self):
        for kook in {"F_tall", "G", "A", "Bb", "C", "D", "E", "F_short"}:
            # arrange
            catalog = CATALOG(current+"/contains_solutions.csv")
            csp = CSP()
            select = SELECT(csp)
            mac = MAC(csp, catalog, specs[kook])
            sut = SOLVER(csp, select, mac)
            # act
            res = sut.find(catalog, specs[kook])
            # assess
            self.assertEqual(res[0], SOLUTION)

    def test_finds_a_solution_every_time(self):
        for i in range(0, 100):
            catalog = CATALOG(current+"/contains_solutions.csv")
            csp = CSP()
            select = SELECT(csp)
            mac = MAC(csp, catalog, specs["C"])
            sut = SOLVER(csp, select, mac)
            # act
            res = sut.find(catalog, specs["C"])
            # assess
            self.assertEqual(res[0], SOLUTION)

    def test_finds_no_solution(self):
        for kook in {"F_tall", "G", "A", "Bb", "C", "D", "E", "F_short"}:
            # arrange
            catalog = CATALOG(current+"/contains_no_solution.csv")
            csp = CSP()
            select = SELECT(csp)
            mac = MAC(csp, catalog, specs[kook])
            sut = SOLVER(csp, select, mac)
            # act
            res = sut.find(catalog, specs[kook])
            # assess
            self.assertNotEqual(res[0], SOLUTION)
