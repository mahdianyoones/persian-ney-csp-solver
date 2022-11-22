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

@unittest.skip("")
class test_SOLVER(unittest.TestCase):

    NO_SOLUTION_DS = "contains_no_solution"
    SOLUTION_DS = "contains_solutions"

    def __find(self, catalog, kook, csp = None):
        '''Generalises arrange and act of all test cases in this suite.'''
        if csp == None:
            csp = CSP()
        select = SELECT(csp)
        mac = MAC(csp, catalog, specs[kook])
        UNARY.init_domains(csp, catalog)
        UNARY.unarify(csp, specs[kook])
        sut = SOLVER(csp, select, mac)
        res = sut.find(catalog, specs[kook])
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

    def test_finds_no_solution_for_F_short(self):
        self.__assert_finds_no_solution("F_short", self.NO_SOLUTION_DS)

    def test_finds_no_solution_for_E(self):
        self.__assert_finds_no_solution("E", self.NO_SOLUTION_DS)

    def test_finds_no_solution_for_D(self):
        self.__assert_finds_no_solution("D", self.NO_SOLUTION_DS)

    def test_finds_no_solution_for_C(self):
        self.__assert_finds_no_solution("C", self.NO_SOLUTION_DS)

    def test_finds_no_solution_for_Bb(self):
        self.__assert_finds_no_solution("Bb", self.NO_SOLUTION_DS)

    def test_finds_no_solution_for_A(self):
        self.__assert_finds_no_solution("A", self.NO_SOLUTION_DS)

    def test_finds_no_solution_for_G(self):
        self.__assert_finds_no_solution("G", self.NO_SOLUTION_DS)

    def test_finds_no_solution_for_F_tall(self):
        self.__assert_finds_no_solution("F_tall", self.NO_SOLUTION_DS)

    def test_finds_a_solution_for_F_short(self):
        self.__assert_finds_solution("F_short", self.SOLUTION_DS)

    def test_finds_a_solution_for_E(self):
        self.__assert_finds_solution("E", self.SOLUTION_DS)

    def test_finds_a_solution_for_D(self):
        self.__assert_finds_solution("D", self.SOLUTION_DS)

    def test_finds_a_solution_for_C(self):
        self.__assert_finds_solution("C", self.SOLUTION_DS)

    def test_finds_a_solution_for_Bb(self):
        self.__assert_finds_solution("Bb", self.SOLUTION_DS)

    def test_finds_a_solution_for_A(self):
        self.__assert_finds_solution("A", self.SOLUTION_DS)

    def test_finds_a_solution_for_G(self):
        self.__assert_finds_solution("G", self.SOLUTION_DS)

    def test_finds_a_solution_for_F_tall(self):
        self.__assert_finds_solution("F_tall", self.SOLUTION_DS)
    
    @unittest.skip("")
    def test_finds_solution_for_all_real_data(self):
        dataset = "real_pieces"
        self.__assert_finds_solution("F_short", dataset)
        self.__assert_finds_solution("E", dataset)
        self.__assert_finds_solution("D", dataset)
        self.__assert_finds_solution("C", dataset)
        self.__assert_finds_solution("Bb", dataset)
        self.__assert_finds_solution("A", dataset)
        self.__assert_finds_solution("G", dataset)
        self.__assert_finds_solution("F_tall", dataset)

if __name__ == "__main__":
    unittest.main()