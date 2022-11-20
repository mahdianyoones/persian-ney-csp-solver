import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
sp.append(parent)

from csp import CSP
from constants import *
from pickup import SELECT

class test_SELECT(unittest.TestCase):

    def setUp(self):
        self.__csp = CSP()
        self.__sut = SELECT(self.__csp)

    def test_selects_var_with_biggest_impact(self):
        # arrange
        csp = self.__csp
            # sets all domains sizes = 1
        for i in range(1, 8):
            csp.update_domain("D"+str(i), {10})
            csp.update_domain("T"+str(i), {2})
            csp.update_domain("R"+str(i), {0})
            csp.update_domain("L"+str(i), {"min": 1, "max": 1})
            csp.update_domain("P"+str(i), {("1", 10)})
        for i in range(0, 14):
            # act
            nextvar = self.__sut.nextvar(csp)
            self.assertTrue(nextvar[0] == "T" or nextvar[0] == "R")
            csp.assign(nextvar, 10)
    
    def test_breaks_impact_ties_with_degree(self):
        # arrange
        csp = self.__csp
            # sets all domains sizes = 1, assigns all but D vars
        for i in range(1, 8):
            csp.update_domain("D"+str(i), {10})
            csp.update_domain("T"+str(i), {2})
            csp.update_domain("R"+str(i), {0})
            csp.update_domain("L"+str(i), {"min": 1, "max": 1})
            csp.update_domain("P"+str(i), {("1", 10)})
            csp.assign("T"+str(i), 2)
            csp.assign("R"+str(i), 0)
            csp.assign("P"+str(i), ("1", 10))
            csp.assign("L"+str(i), 1)
        five_first = set([])
        for i in range(0, 5):
            # act
            nextvar = self.__sut.nextvar(csp)
            five_first.add(nextvar)
            csp.assign(nextvar, 10)
        self.assertEqual(five_first, {"D2", "D3", "D4", "D5", "D6"})
        next_two = set([])
        nextvar = self.__sut.nextvar(csp)
        next_two.add(nextvar)
        csp.assign(nextvar, 10)
        nextvar = self.__sut.nextvar(csp)
        next_two.add(nextvar)
        self.assertEqual(next_two, {"D1", "D7"})
    
    def test_breaks_impact_and_degree_ties_with_mrv(self):
        # arrange
        csp = self.__csp
            # sets all domains sizes = 1, assigns all but D vars
        for i in range(1, 8):
            csp.update_domain("T"+str(i), {2})
            csp.update_domain("R"+str(i), {0})
            csp.update_domain("L"+str(i), {"min": 1, "max": 1})
            csp.update_domain("P"+str(i), {("1", 10)})
            csp.assign("T"+str(i), 2)
            csp.assign("R"+str(i), 0)
            csp.assign("P"+str(i), ("1", 10))
            csp.assign("L"+str(i), 1)
        csp.assign("D1", 10)
        csp.update_domain("D2", {10, 11, 12, 13, 16})
        csp.update_domain("D3", {10, 11, 14, 15})
        csp.update_domain("D4", {10, 11, 12})
        csp.update_domain("D5", {10, 11})
        csp.update_domain("D6", {10})
        csp.assign("D7", 10)
        selected_vars = []
        for i in range(2, 7): # 2 to 6
            nextvar = self.__sut.nextvar(csp)
            selected_vars.append(nextvar)
            csp.assign(nextvar, 10)
        self.assertEqual(selected_vars, ["D6", "D5", "D4", "D3", "D2"])

if __name__ == "__main__":
    unittest.main()