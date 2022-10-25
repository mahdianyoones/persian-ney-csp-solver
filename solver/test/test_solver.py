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

    def __find_existing_solution(self, kook):
        catalog = CATALOG(current+"/contains_solutions.csv")
        csp = CSP()
        select = SELECT(csp)
        mac = MAC(csp, catalog, specs[kook])
        sut = SOLVER(csp, select, mac)
        res = sut.find(catalog, specs[kook])
        return res

    def test_finds_Ftall_solution(self):
        res = self.__find_existing_solution("F_tall")
        self.assertEqual(res[0], SOLUTION)

    def test_finds_G_solution(self):
        res = self.__find_existing_solution("G")
        self.assertEqual(res[0], SOLUTION)

    def test_finds_A_solution(self):
        res = self.__find_existing_solution("A")
        self.assertEqual(res[0], SOLUTION)

    def test_finds_Bb_solution(self):
        res = self.__find_existing_solution("Bb")
        self.assertEqual(res[0], SOLUTION)

    def test_finds_C_solution(self):
        res = self.__find_existing_solution("C")
        self.assertEqual(res[0], SOLUTION)

    def test_finds_D_solution(self):
        res = self.__find_existing_solution("D")
        self.assertEqual(res[0], SOLUTION)

    def test_finds_E_solution(self):
        res = self.__find_existing_solution("E")
        self.assertEqual(res[0], SOLUTION)

    def test_finds_Fshort_solution(self):
        res = self.__find_existing_solution("F_short")
        self.assertEqual(res[0], SOLUTION)

    def test_finds_an_existing_solution(self):
        '''Ensures that an existing solution is discovered across executions.'''
        for i in range(0, 20):
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
