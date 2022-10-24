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

    def setUp(self):
        self.__catalog = CATALOG(current+"/pieces2.csv")
        self.__csp = CSP()
        self.__select = SELECT(self.__csp)
        self.__mac = MAC(self.__csp, self.__catalog, specs["C"])
        self.__sut = SOLVER(self.__csp, self.__select, self.__mac)

    def test_finds_a_solution(self):
        # arrange
        # act
        res = self.__sut.find(self.__catalog, specs["C"])
        # assess
        self.assertEqual(res[0], SOLUTION)