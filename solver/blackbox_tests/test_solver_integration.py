import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
sp.append(parent)

from solver import SOLVER
from csp import CSP
from testspec import specs
from unary import UNARY
from mac import MAC
from pickup import SELECT
from constants import *

class test_SOLVER_INTEGRATION(unittest.TestCase):

    NO_SOLUTION_DS = "contains_no_solution"
    SOLUTION_DS = "contains_solutions"
    REAL_DS = "real_pieces"

    def __find(self, data_set_path, kook, csp = None):
        '''Generalises arrange and act of all test cases in this suite.'''
        if csp == None:
            csp = CSP()
        select = SELECT(csp)
        mac = MAC(csp, specs[kook])
        UNARY.init_domains(csp, data_set_path)
        UNARY.unarify(csp, specs[kook])
        sut = SOLVER(csp, select, mac)
        res = sut.find_independent(specs[kook], data_set_path)
        return res

    def __assert_finds_solution(self, kook, dataset, csp = None):
        data_set_path = current+"/"+dataset+".csv"
        res = self.__find(data_set_path, kook, csp)
        self.assertEqual(res[0], SOLUTION)

    def __assert_finds_no_solution(self, kook, dataset, csp = None):
        data_set_path = current+"/"+dataset+".csv"
        res = self.__find(data_set_path, kook, csp)
        self.assertNotEqual(res[0], SOLUTION)

    # Existing solutions are found in an artificial dataset

    def test_finds_a_solution_for_F_short_artificial_dataset(self):
        self.__assert_finds_solution("F_short", self.SOLUTION_DS)

    def test_finds_a_solution_for_E_artificial_dataset(self):
        self.__assert_finds_solution("E", self.SOLUTION_DS)

    def test_finds_a_solution_for_D_artificial_dataset(self):
        self.__assert_finds_solution("D", self.SOLUTION_DS)

    def test_finds_a_solution_for_C_artificial_dataset(self):
        self.__assert_finds_solution("C", self.SOLUTION_DS)

    def test_finds_a_solution_for_Bb_artificial_dataset(self):
        self.__assert_finds_solution("Bb", self.SOLUTION_DS)

    def test_finds_a_solution_for_A_artificial_dataset(self):
        self.__assert_finds_solution("A", self.SOLUTION_DS)

    def test_finds_a_solution_for_G_artificial_dataset(self):
        self.__assert_finds_solution("G", self.SOLUTION_DS)

    def test_finds_a_solution_for_F_tall_artificial_dataset(self):
        self.__assert_finds_solution("F_tall", self.SOLUTION_DS)

    # Existing solutions are found in a real dataset

    def test_finds_a_solution_for_F_short_real_dataset(self):
        self.__assert_finds_solution("F_short", self.REAL_DS)

    def test_finds_a_solution_for_E_real_dataset(self):
        self.__assert_finds_solution("E", self.REAL_DS)

    def test_finds_a_solution_for_D_real_dataset(self):
        self.__assert_finds_solution("D", self.REAL_DS)

    def test_finds_a_solution_for_C_real_dataset(self):
        self.__assert_finds_solution("C", self.REAL_DS)

    def test_finds_a_solution_for_Bb_real_dataset(self):
        self.__assert_finds_solution("Bb", self.REAL_DS)

    def test_finds_a_solution_for_A_real_dataset(self):
        self.__assert_finds_solution("A", self.REAL_DS)

    def test_finds_a_solution_for_G_real_data(self):
        self.__assert_finds_solution("G", self.REAL_DS)

    # No solution is found in an artificial dataset

    def test_finds_no_solution_for_F_short_artificial_dataset(self):
        self.__assert_finds_no_solution("F_short", self.NO_SOLUTION_DS)

    def test_finds_no_solution_for_E_artificial_dataset(self):
        self.__assert_finds_no_solution("E", self.NO_SOLUTION_DS)

    def test_finds_no_solution_for_D_artificial_dataset(self):
        self.__assert_finds_no_solution("D", self.NO_SOLUTION_DS)

    def test_finds_no_solution_for_C_artificial_dataset(self):
        self.__assert_finds_no_solution("C", self.NO_SOLUTION_DS)

    def test_finds_no_solution_for_Bb_artificial_dataset(self):
        self.__assert_finds_no_solution("Bb", self.NO_SOLUTION_DS)

    def test_finds_no_solution_for_A_artificial_dataset(self):
        self.__assert_finds_no_solution("A", self.NO_SOLUTION_DS)

    def test_finds_no_solution_for_G_artificial_dataset(self):
        self.__assert_finds_no_solution("G", self.NO_SOLUTION_DS)

    def test_finds_no_solution_for_F_tall_artificial_dataset(self):
        self.__assert_finds_no_solution("F_tall", self.NO_SOLUTION_DS)

    # No solution is found in a real dataset

    def test_finds_no_solution_for_F_tall_real_data(self):
        self.__assert_finds_no_solution("F_tall", self.REAL_DS)

if __name__ == "__main__":
    unittest.main()