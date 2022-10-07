import unittest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from csp import CSP
from spec import specs
from constants import *
from pickup import SELECT

class test_SELECT(unittest.TestCase):
    '''Tests the behavior of pickup class: select next variable and value.'''

    def setUp(self):
        self.__csp = CSP()
        self.__sut = SELECT()
        self.__sut.init_degree(self.__csp)

    def test_impact_heuristic_works(self):
        # arrange
        csp = self.__csp
        for i in range(1, 8):
            csp.update_domain("D"+str(i), {10})
            csp.update_domain("T"+str(i), {2})
            csp.update_domain("R"+str(i), {0})
            csp.update_domain("L"+str(i), {"min": 1, "max": 1})
        D = csp.get_domains()
        for i in range(0, 14):
            # act
            nextvar = self.__sut.nextvar(csp)
            csp.assign(nextvar, D[nextvar].pop())
        # assess
        assigned = csp.get_assigned_vars()
        e = {"T1","T2","T3","T4","T5","T6","T7","R1","R2","R3","R4","R5",\
            "R6","R7"}
        self.assertEqual(set(assigned), e)
        for i in range(0, 7):
            # act
            nextvar = self.__sut.nextvar(csp)
            csp.assign(nextvar, D[nextvar].pop())
        # assess
        assigned = csp.get_assigned_vars()
        e = {"D1","D2","D3","D4","D5","D6","D7"}
        self.assertTrue(set(assigned).intersection(e) == e)
        for i in range(0, 7):
            # act
            nextvar = self.__sut.nextvar(csp)
            csp.assign(nextvar, 1)
        assigned = csp.get_assigned_vars()
        e = {"L1","L2","L3","L4","L5","L6","L7"}
        self.assertTrue(set(assigned).intersection(e) == e)
    
    def test_degree_and_mrv_heuristics_work(self):
        # arrange
        selected_vars = []
        csp = self.__csp
        for i in range(1, 8):
            csp.update_domain("D"+str(i), {1})
            csp.update_domain("T"+str(i), {1})
            csp.update_domain("R"+str(i), {1,2})
            csp.update_domain("L"+str(i), {"min": 1, "max": 1})
        csp.update_domain("L7", {"min": 1, "max": 2})
        csp.update_domain("L3", {"min": 1, "max": 2})
        # act
        D = csp.get_domains()
        for i in range(0, 28):
            nextvar = self.__sut.nextvar(csp)
            selected_vars.append(nextvar)
            csp.assign(nextvar, 1)
        # assess
        for i in range(0, 7):
            self.assertEqual(selected_vars[i][0], "T")
        for i in range(7, 14):
            self.assertEqual(selected_vars[i][0], "R")
        for i in range(14, 21):
            self.assertEqual(selected_vars[i][0], "D")
        e = ["L2","L1","L3","L4","L5","L6","L7"]
        for i in range(21, 28):
            self.assertEqual(selected_vars[i], e[i-21])
