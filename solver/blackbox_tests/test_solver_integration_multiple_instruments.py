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

    def __get_random_instrument_regs(self, quantity):
        all_regs = ["F_short", "E", "D", "C", "Bb", "A", "G", "F_tall"]
        return [all_regs[i] for i in [random.randint(0, 7) for j in range(0, quantity)]]

    def test_finds_one_instrument_artificial_ds(self):
        specs_needed = self.__get_random_instrument_regs(1)
        print(specs_needed)
        self.__assert_finds_multiple_solution(specs_needed, self.MULTI_SOLUTIONS_DS)

    def test_finds_two_instruments_artificial_ds(self):
        specs_needed = self.__get_random_instrument_regs(2)
        print(specs_needed)
        self.__assert_finds_multiple_solution(specs_needed, self.MULTI_SOLUTIONS_DS)

    def test_finds_3_instruments_artificial_ds(self):
        specs_needed = self.__get_random_instrument_regs(3)
        print(specs_needed)
        self.__assert_finds_multiple_solution(specs_needed, self.MULTI_SOLUTIONS_DS)

    def test_finds_10_instruments_artificial_ds(self):
        specs_needed = self.__get_random_instrument_regs(10)
        print(specs_needed)
        self.__assert_finds_multiple_solution(specs_needed, self.MULTI_SOLUTIONS_DS)

    def test_finds_11_instruments_artificial_ds(self):
        specs_needed = self.__get_random_instrument_regs(11)
        print(specs_needed)
        self.__assert_finds_multiple_solution(specs_needed, self.MULTI_SOLUTIONS_DS)

if __name__ == "__main__":
    unittest.main()