import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
sp.append(parent)

from solver import SOLVER
from csp import CSP
from testspec import specs
from mac import MAC
from pickup import SELECT
from constants import *
from verify import is_valid
from pretty_print import print_solution
import random

class test_SOLVER_INTEGRATION_MULTIPLE_INSTRUMENTS(unittest.TestCase):
    '''Tests solver when looking for multiple instrument solutions.
    
    The dataset that is used for testing exhibits a perfect situation.
    As the number of pieces increase in the dataset, the search becomes
    harder.'''

    MULTI_SOLUTIONS_DS = "contains_multiple_solutions"

    def __find(self, data_set_path, specs, csp = None):
        '''Generalises arrange and act of all test cases in this suite.'''
        if csp == None:
            csp = CSP(S=len(specs))
        select = SELECT()
        mac = MAC()
        sut = SOLVER(select, mac)
        res = sut.find(csp, specs, data_set_path)
        return res

    def __assert_finds_multiple_solution(self, regs, dataset, csp = None):
        data_set_path = current+"/"+dataset+".csv"
        specs_sorted = [specs[reg] for reg in regs]        
        res = self.__find(data_set_path, specs_sorted, csp)
        self.assertEqual(res[0], SOLUTION)
        self.assertTrue(is_valid(res[1], regs, specs))
        return res[1]

    def test_finds_1_instrument(self):
        self.__assert_finds_multiple_solution(["Bb"], self.MULTI_SOLUTIONS_DS)
        self.__assert_finds_multiple_solution(["C"], self.MULTI_SOLUTIONS_DS)
        self.__assert_finds_multiple_solution(["E"], self.MULTI_SOLUTIONS_DS)
        self.__assert_finds_multiple_solution(["F_short"], self.MULTI_SOLUTIONS_DS)
        self.__assert_finds_multiple_solution(["D"], self.MULTI_SOLUTIONS_DS)
        self.__assert_finds_multiple_solution(["A"], self.MULTI_SOLUTIONS_DS)
        self.__assert_finds_multiple_solution(["F_tall"], self.MULTI_SOLUTIONS_DS)
        self.__assert_finds_multiple_solution(["G"], self.MULTI_SOLUTIONS_DS)

    def test_finds_2_instruments(self):
        self.__assert_finds_multiple_solution(["Bb", "Bb"], self.MULTI_SOLUTIONS_DS)
        self.__assert_finds_multiple_solution(["Bb", "C"], self.MULTI_SOLUTIONS_DS)
        self.__assert_finds_multiple_solution(["D", "A"], self.MULTI_SOLUTIONS_DS)

if __name__ == "__main__":
    unittest.main()