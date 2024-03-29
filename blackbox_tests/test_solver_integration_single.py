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

class test_SOLVER_INTEGRATION_SINGLE(unittest.TestCase):
    '''Test solver when looking for single instrument solutions.'''

    SOLUTION_DS = "contains_solutions"

    def __find(self, data_set_path, specs, csp = None):
        '''Generalises arrange and act of all test cases in this suite.'''
        if csp == None:
            csp = CSP(S=len(specs))
        select = SELECT()
        mac = MAC()
        sut = SOLVER(select, mac)
        res = sut.find(csp, specs, data_set_path)
        return res

    def __assert_finds_solution(self, reg, dataset, csp = None):
        data_set_path = current+"/"+dataset+".csv"
        res = self.__find(data_set_path, [specs[reg]], csp)
        self.assertEqual(res[0], SOLUTION)
        self.assertTrue(is_valid(res[1], [reg], specs))
        return res[1]

    def test_finds_F_short(self):
        solution = self.__assert_finds_solution("F_short", self.SOLUTION_DS)
        print("")
        print_solution(solution)

    def test_finds_E(self):
        solution = self.__assert_finds_solution("E", self.SOLUTION_DS)
        print("")
        print_solution(solution)

    def test_finds_D(self):
        solution = self.__assert_finds_solution("D", self.SOLUTION_DS)
        print("")
        print_solution(solution)

    def test_finds_C(self):
        solution = self.__assert_finds_solution("C", self.SOLUTION_DS)
        print("")
        print_solution(solution)

    def test_finds_Bb(self):
        solution = self.__assert_finds_solution("Bb", self.SOLUTION_DS)
        print("")
        print_solution(solution)

    def test_finds_A(self):
        solution = self.__assert_finds_solution("A", self.SOLUTION_DS)
        print("")
        print_solution(solution)

    def test_finds_G(self):
        solution = self.__assert_finds_solution("G", self.SOLUTION_DS)
        print("")
        print_solution(solution)

    def test_finds_F_tall(self):
        solution = self.__assert_finds_solution("F_tall", self.SOLUTION_DS)
        print("")
        print_solution(solution)

if __name__ == "__main__":
    unittest.main()