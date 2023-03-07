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

class test_SOLVER_NO_SOLUTION_INTEGRATION(unittest.TestCase):

    NO_SOLUTION_DS = "contains_no_solution"

    def __find(self, data_set_path, specs, csp = None):
        '''Generalises arrange and act of all test cases in this suite.'''
        if csp == None:
            csp = CSP(S=len(specs))
        select = SELECT()
        mac = MAC()
        sut = SOLVER(select, mac)
        res = sut.find(csp, specs, data_set_path)
        return res

    def __assert_finds_no_solution(self, reg, dataset, csp = None):
        data_set_path = current+"/"+dataset+".csv"
        res = self.__find(data_set_path, [specs[reg]], csp)
        self.assertNotEqual(res[0], SOLUTION)

    def test_detects_failure_F_short(self):
        self.__assert_finds_no_solution("F_short", self.NO_SOLUTION_DS)

    def test_detects_failure_E(self):
        self.__assert_finds_no_solution("E", self.NO_SOLUTION_DS)

    def test_detects_failure_D(self):
        self.__assert_finds_no_solution("D", self.NO_SOLUTION_DS)

    def test_detects_failure_C(self):
        self.__assert_finds_no_solution("C", self.NO_SOLUTION_DS)

    def test_detects_failure_Bb(self):
        self.__assert_finds_no_solution("Bb", self.NO_SOLUTION_DS)

    def test_detects_failure_A(self):
        self.__assert_finds_no_solution("A", self.NO_SOLUTION_DS)

    def test_detects_failure_G(self):
        self.__assert_finds_no_solution("G", self.NO_SOLUTION_DS)

    def test_detects_failure_F_tall(self):
        self.__assert_finds_no_solution("F_tall", self.NO_SOLUTION_DS)

if __name__ == "__main__":
    unittest.main()