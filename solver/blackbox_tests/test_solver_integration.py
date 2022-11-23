import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
sp.append(parent)

from solver import SOLVER
from csp import CSP
from testspec import specs
from catalog import CATALOG
from unary import UNARY
from mac import MAC
from pickup import SELECT
from constants import *
import random

class test_SOLVER_INTEGRATION(unittest.TestCase):

    NO_SOLUTION_DS = "contains_no_solution"
    SOLUTION_DS = "contains_solutions"
    REAL_DS = "real_pieces"

    def __find(self, catalog, kook, csp = None):
        '''Generalises arrange and act of all test cases in this suite.'''
        if csp == None:
            csp = CSP()
        select = SELECT(csp)
        mac = MAC(csp, catalog, specs[kook])
        UNARY.init_domains(csp, catalog)
        UNARY.unarify(csp, specs[kook])
        sut = SOLVER(csp, select, mac)
        res = sut.find_independent(catalog, specs[kook])
        return res

    def __assert_finds_solution(self, kook, dataset, csp = None):
        data_set_path = current+"/"+dataset+".csv"
        catalog = CATALOG(data_set_path)
        res = self.__find(catalog, kook, csp)
        self.assertEqual(res[0], SOLUTION)

    def __assert_finds_no_solution(self, kook, dataset, csp = None):
        data_set_path = current+"/"+dataset+".csv"
        catalog = CATALOG(data_set_path)
        res = self.__find(catalog, kook, csp)
        self.assertNotEqual(res[0], SOLUTION)

    def test_finds_no_solution_for_a_random_kook(self):
        '''Asserts that no solution for no register can be found.'''
        kooks = ["F_short", "E", "D", "C", "Bb", "A", "G", "F_tall"]
        for i in range(0, 3):
            random_kook = kooks[random.randint(0, len(kooks) - 1)]
            self.__assert_finds_no_solution(random_kook, self.NO_SOLUTION_DS)

    def test_finds_a_solution_for_a_random_kook(self):
        '''Asserts that a solution is found.'''
        kooks = ["F_short", "E", "D", "C", "Bb", "A", "G", "F_tall"]
        for i in range(0, 3):
            random_kook = kooks[random.randint(0, len(kooks) - 1)]
            self.__assert_finds_solution(random_kook, self.SOLUTION_DS)
    
    def test_finds_a_solution_for_a_random_kook_real_ds(self):
        '''Asserts that a solution is found.'''
        kooks = ["F_short", "E", "D", "C", "Bb", "A"]
        for i in range(0, 3):
            random_kook = kooks[random.randint(0, len(kooks) - 1)]
            self.__assert_finds_solution(random_kook, self.REAL_DS)

    def test_finds_no_solution_for_G_real_data(self):
        self.__assert_finds_no_solution("G", self.REAL_DS)

    def test_finds_no_solution_for_F_tall_real_data(self):
        self.__assert_finds_no_solution("F_tall", self.REAL_DS)

if __name__ == "__main__":
    unittest.main()