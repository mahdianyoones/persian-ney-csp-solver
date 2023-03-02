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

class test_SOLVER_INTEGRATION(unittest.TestCase):

    NO_SOLUTION_DS = "contains_no_solution"
    SOLUTION_DS = "contains_solutions"
    REAL_DS = "real_pieces"
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

    def __assert_finds_solution(self, reg, dataset, csp = None):
        data_set_path = current+"/"+dataset+".csv"
        res = self.__find(data_set_path, [specs[reg]], csp)
        self.assertEqual(res[0], SOLUTION)
        self.assertTrue(is_valid(res[1], [reg], specs))

    def __assert_finds_multiple_solution(self, regs, dataset, csp = None):
        data_set_path = current+"/"+dataset+".csv"
        specs_sorted = [specs[reg] for reg in regs]        
        res = self.__find(data_set_path, specs_sorted, csp)
        self.assertEqual(res[0], SOLUTION)
        self.assertTrue(is_valid(res[1], regs, specs))
        return res[1]

    def __assert_finds_no_solution(self, reg, dataset, csp = None):
        data_set_path = current+"/"+dataset+".csv"
        res = self.__find(data_set_path, [specs[reg]], csp)
        self.assertNotEqual(res[0], SOLUTION)

    # Existing solutions are found in an artificial dataset

    # def test_finds_F_short_artificial_ds(self):
    #     self.__assert_finds_solution("F_short", self.SOLUTION_DS)

    # def test_finds_E_artificial_ds(self):
    #     self.__assert_finds_solution("E", self.SOLUTION_DS)

    # def test_finds_D_artificial_ds(self):
    #     self.__assert_finds_solution("D", self.SOLUTION_DS)

    # def test_finds_C_artificial_ds(self):
    #     self.__assert_finds_solution("C", self.SOLUTION_DS)

    # def test_finds_Bb_artificial_ds(self):
    #     self.__assert_finds_solution("Bb", self.SOLUTION_DS)

    # def test_finds_A_artificial_ds(self):
    #     self.__assert_finds_solution("A", self.SOLUTION_DS)

    # def test_finds_G_artificial_ds(self):
    #     self.__assert_finds_solution("G", self.SOLUTION_DS)

    # def test_finds_F_tall_artificial_ds(self):
    #     self.__assert_finds_solution("F_tall", self.SOLUTION_DS)

    # Multiple existing solutions are found in an artificial ds

    def test_finds_C_C_artificial_ds(self):
        solutions = self.__assert_finds_multiple_solution(["C", "C"], self.MULTI_SOLUTIONS_DS)
        print(solutions)    

    # Existing solutions are found in a real dataset

    # def test_finds_F_short_real_ds(self):
    #     self.__assert_finds_solution("F_short", self.REAL_DS)

    # def test_finds_E_real_ds(self):
    #     self.__assert_finds_solution("E", self.REAL_DS)

    # def test_finds_D_real_ds(self):
    #     self.__assert_finds_solution("D", self.REAL_DS)

    # def test_finds_C_real_ds(self):
    #     self.__assert_finds_solution("C", self.REAL_DS)

    # def test_finds_Bb_real_ds(self):
    #     self.__assert_finds_solution("Bb", self.REAL_DS)

    # def test_finds_A_real_ds(self):
    #     self.__assert_finds_solution("A", self.REAL_DS)

    # def test_finds_G_real_data(self):
    #     self.__assert_finds_solution("G", self.REAL_DS)

    # def test_finds_A_A_real_ds(self):
    #     solutions = self.__assert_finds_multiple_solution(["C", "C"], self.REAL_DS)
    #     print(solutions)

    # def test_finds_G_A_C_D_A_E_F_short_real_ds(self):
    #     regs = ["G", "A", "C", "D", "A", "E", "F_short"]
    #     self.__assert_finds_multiple_solution(regs, self.REAL_DS)

    # def test_finds_A_A_A_A_real_ds(self):
    #     self.__assert_finds_multiple_solution(["A", "A", "A", "A"], self.REAL_DS)

    # def test_finds_14_F_short_real_ds(self):
    #     regs = ["F_short" for i in range(0, 14)]
    #     self.__assert_finds_multiple_solution(regs, self.REAL_DS)

    # No solution is found in an artificial ds

    # def test_detects_failure_F_short_artificial_ds(self):
    #     self.__assert_finds_no_solution("F_short", self.NO_SOLUTION_DS)

    # def test_detects_failure_E_artificial_ds(self):
    #     self.__assert_finds_no_solution("E", self.NO_SOLUTION_DS)

    # def test_detects_failure_D_artificial_ds(self):
    #     self.__assert_finds_no_solution("D", self.NO_SOLUTION_DS)

    # def test_detects_failure_C_artificial_ds(self):
    #     self.__assert_finds_no_solution("C", self.NO_SOLUTION_DS)

    # def test_detects_failure_Bb_artificial_ds(self):
    #     self.__assert_finds_no_solution("Bb", self.NO_SOLUTION_DS)

    # def test_detects_failure_A_artificial_ds(self):
    #     self.__assert_finds_no_solution("A", self.NO_SOLUTION_DS)

    # def test_detects_failure_G_artificial_ds(self):
    #     self.__assert_finds_no_solution("G", self.NO_SOLUTION_DS)

    # def test_detects_failure_F_tall_artificial_ds(self):
    #     self.__assert_finds_no_solution("F_tall", self.NO_SOLUTION_DS)

    # # No solution is found in a real dataset

    # def test_detects_failure_F_tall_real_data(self):
    #     self.__assert_finds_no_solution("F_tall", self.REAL_DS)

if __name__ == "__main__":
    unittest.main()