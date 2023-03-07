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

class test_LENDEC_INTEGRATION(unittest.TestCase):
    '''Tests the behavior of MAC.'''

    def __assert_domains_are_consistent(self):
        D = self.__csp.get_domains()
        A = self.__csp.get_assignment()
        for i in range(3, 7):
            Dprev = "L"+str(i-1)
            _min = A[Dprev] if Dprev in A else D[Dprev]["min"]
            _max = A[Dprev] if Dprev in A else D[Dprev]["max"]
            valid_range = {
                "min": 2/3 * _min, 
                "max": _max - 1, 
            }
            Dcur = "L"+str(i)
            if Dcur in A:
                self.assertTrue(A[Dcur] >= valid_range["min"])
                self.assertTrue(A[Dcur] <= valid_range["max"])
            else:
                self.assertTrue(D[Dcur]["min"] >= valid_range["min"])
                self.assertTrue(D[Dcur]["max"] <= valid_range["max"])

    def setUp(self):
        self.__X = {
            "L1","L2", "L3", "L4", "L5", "L6", "L7",
            "P1","P2", "P3", "P4", "P5", "P6", "P7",
            "L8","L9", "L10", "L11", "L12", "L13", "L14",
            "P8","P9", "P10", "P11", "P12", "P13", "P14",
            }
        self.__C = {
            "lendec2-3_0":        {"L2", "L3"},
            "lendec3-4_0":        {"L3", "L4"},
            "lendec4-5_0":        {"L4", "L5"},
            "lendec5-6_0":        {"L5", "L6"},
            "lendec6-7_0":        {"L6", "L7"},
            "lendeclower2-3_0":   {"L2", "L3"},
            "lendeclower3-4_0":   {"L3", "L4"},
            "lendeclower4-5_0":   {"L4", "L5"},
            "lendeclower5-6_0":   {"L5", "L6"},
            "lendec2-3_1":        {"L9", "L10"},
            "lendec3-4_1":        {"L10", "L11"},
            "lendec4-5_1":        {"L11", "L12"},
            "lendec5-6_1":        {"L12", "L13"},
            "lendec6-7_1":        {"L13", "L14"},
            "lendeclower2-3_1":   {"L9", "L10"},
            "lendeclower3-4_1":   {"L10", "L11"},
            "lendeclower4-5_1":   {"L11", "L12"},
            "lendeclower5-6_1":   {"L12", "L13"}
        }
        self.__csp = CSP(S = 2, X = self.__X, C = self.__C)
        current = op.dirname(__file__)
        data_set_path = current+"/real_pieces.csv"
        UNARY.init_domains(self.__csp, data_set_path)
        UNARY.unarify(self.__csp, [specs["C"], specs["C"]])
        self.__mac = MAC()
        
    def test_L2_propagates_to_all(self):
        # act
        res = self.__mac.propagate(self.__csp, [None, None], {"L2"})
        self.assertEqual(res[0], MADE_CONSISTENT)
        self.__assert_domains_are_consistent()

    def test_L4_propagates_to_all(self):
        # act
        res = self.__mac.propagate(self.__csp, [None, None], {"L4"})
        self.assertEqual(res[0], MADE_CONSISTENT)
        self.__assert_domains_are_consistent()
    
    def test_L2_gets_established(self):
        # arrange
        self.__csp.assign("L2", 80)
        # act
        res = self.__mac.establish(self.__csp, [None, None], "L2", 80)
        # assess
        self.assertEqual(res[0], MADE_CONSISTENT)
        self.assertEqual(res[1], {"L3", "L4", "L5", "L6", "L7"})
        self.__assert_domains_are_consistent()
        D = self.__csp.get_domains()
        self.assertEqual(D["L3"]["max"], 79)
        self.assertEqual(D["L4"]["max"], 78)
        self.assertEqual(D["L5"]["max"], 77)
        self.assertEqual(D["L6"]["max"], 76)
        self.assertEqual(D["L7"]["max"], 75)

    def test_L7_gets_established(self):
        # arrange
        D = self.__csp.get_domains()
        self.__csp.assign("L7", 100)
        # act
        res = self.__mac.establish(self.__csp, [None, None], "L7", 100)
        # assess
        self.assertEqual(res[0], MADE_CONSISTENT)
        self.assertEqual(res[1], {"L2", "L3", "L4", "L5", "L6"})
        self.__assert_domains_are_consistent()
        self.assertEqual(D["L6"]["min"], 101)
        self.assertEqual(D["L5"]["min"], 102)
        self.assertEqual(D["L4"]["min"], 103)
        self.assertEqual(D["L3"]["min"], 104)
        self.assertEqual(D["L2"]["min"], 105)

if __name__ == "__main__":
    unittest.main()