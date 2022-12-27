import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
grandparent = op.dirname(op.dirname(current))
sp.append(parent)
sp.append(grandparent)

from csp import CSP
from mac import MAC
from unary import UNARY
from testspec import specs
from constants import *

class test_DIAMDEC_INTEGRATION(unittest.TestCase):
    '''Tests the behavior of MAC.'''

    def __assert_domains_are_consistent(self):
        D = self.__csp.get_domains()
        A = self.__csp.get_assignment()
        ddiff = specs["C"]["ddiff"]
        for i in range(2, 8):
            Pi = "P"+str(i-1)
            Pj = "P"+str(i)
            pieces_i = {A[Pi]} if Pi in A else D[Pi]
            pieces_j = {A[Pj]} if Pj in A else D[Pj]
            for piece_i in pieces_i:
                valid_counterparts = 0
                for piece_j in pieces_j:
                    diff = piece_i[4] - piece_j[4]
                    if diff >= ddiff["min"] and diff <= ddiff["max"]:
                        valid_counterparts += 1
                self.assertTrue(valid_counterparts >= 1)

    def setUp(self):
        self.__X = {"P1", "P2", "P3", "P4", "P5", "P6", "P7"}
        self.__C = {
            "diamdec1-2": {"P1", "P2"},
            "diamdec2-3": {"P2", "P3"},
            "diamdec3-4": {"P3", "P4"},
            "diamdec4-5": {"P4", "P5"},
            "diamdec5-6": {"P5", "P6"},
            "diamdec6-7": {"P6", "P7"}
        }
        self.__csp = CSP(self.__X, self.__C)
        current = op.dirname(__file__)
        data_set_path = current+"/real_pieces.csv"
        self.__mac = MAC(self.__csp, specs["C"])
        UNARY.init_domains(self.__csp, data_set_path)
        UNARY.unarify(self.__csp, specs["C"])
    
    def test_P1_reduction_propagates_to_all(self):
        '''Tests the behavior of diamdec for all its related constraints.'''
        # act
        res = self.__mac.propagate({"P1"})
        # assess
        self.assertEqual(res[0], MADE_CONSISTENT)
        self.assertEqual(res[1], {"P1", "P2", "P3", "P4", "P5", "P6", "P7"})
        self.__assert_domains_are_consistent()
    
    def test_P7_reduction_propagates_to_all(self):
        '''Tests the behavior of diamdec for all its related constraints.'''
        # act
        res = self.__mac.propagate({"P7"})
        # assess
        self.assertEqual(res[0], MADE_CONSISTENT)
        self.assertEqual(res[1], {"P1", "P2", "P3", "P4", "P5", "P6", "P7"})
        self.__assert_domains_are_consistent()

    def test_P5_reduction_propagates_to_all(self):
        '''Tests the behavior of diamdec for all its related constraints.'''
        # act
        res = self.__mac.propagate({"P5"})
        # assess
        self.assertEqual(res[0], MADE_CONSISTENT)
        self.assertEqual(res[1], {"P1", "P2", "P3", "P4", "P5", "P6", "P7"})
        self.__assert_domains_are_consistent()

    def test_P1_assignment_gets_established(self):
        # arrange
        self.__csp.assign("P1", (1,1,1,1,18))
        # act
        res = self.__mac.establish("P1", (1,1,1,1,18))
        self.assertEqual(res[0], MADE_CONSISTENT)
        self.assertEqual(res[1], {"P2", "P3", "P4", "P5", "P6", "P7"})
        self.__assert_domains_are_consistent()

    def test_P7_assignment_gets_established(self):
        # arrange
        self.__csp.assign("P7", (1,1,1,1,13.5))
        # act
        res = self.__mac.establish("P7", (1,1,1,1,13.5))
        self.assertEqual(res[0], MADE_CONSISTENT)
        self.assertEqual(res[1], {"P1", "P2", "P3", "P4", "P5", "P6"})
        self.__assert_domains_are_consistent()

    def test_P4_assignment_gets_established(self):
        # arrange
        self.__csp.assign("P4", (1,1,1,1,16))
        # act
        res = self.__mac.establish("P4", (1,1,1,1,16))
        self.assertEqual(res[0], MADE_CONSISTENT)
        self.assertEqual(res[1], {"P1", "P2", "P3", "P5", "P6", "P7"})
        self.__assert_domains_are_consistent()

    def test_P1_reduction_propagates_to_contradiction(self):
        # arrange
        self.__csp.update_domain("P7", {(1,1,1,1,20)})
        # act
        res = self.__mac.propagate({"P1"})
        # assess
        self.assertEqual(res[0], CONTRADICTION)

if __name__ == "__main__":
    unittest.main()