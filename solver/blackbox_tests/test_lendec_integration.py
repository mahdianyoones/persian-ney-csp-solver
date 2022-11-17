import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
grandparent = op.dirname(op.dirname(current))
sp.append(parent)
sp.append(grandparent)

from csp import CSP
from catalog import CATALOG
from mac import MAC
from unary import UNARY
from testspec import specs
from constants import *

class test_LENDEC_INTEGRATION(unittest.TestCase):
    '''Tests the behavior of MAC.

    samethick:	    (T1, T2, T3, T4, T5, T6, T7)
    sameround:	    (R1, R2, R3, R4, R5, R6, R7)
    len:	 	    (L1, L2, L3, L4, L5, L6, L7)
    hole6:		    (L1, L2, L3, L4, L5)
    hole3:		    (L1, L2, L3, L4)
    hole1:		    (L1, L2, L3)
    half:           (L1, L2)

    lendec2:        (L2, L3)
    lendec3:        (L3, L4)
    lendec4:        (L4, L5)
    lendec5:        (L5, L6)
    lendec6:        (L6, L7)

    lendeclower2:   (L2, L3)
    lendeclower3:   (L3, L4)
    lendeclower4:   (L4, L5)
    lendeclower5:   (L5, L6)

    diamdec1:       (D1, D2)
    diamdec2:       (D2, D3)
    diamdec3:       (D3, D4)
    diamdec4:       (D4, D5)
    diamdec5:       (D5, D6)
    diamdec6:       (D6, D7)

    pstock1:        (T1, R1, D1, P1)
    pstock2:        (T2, R2, D2, P2)
    pstock3:        (T3, R3, D3, P3)
    pstock4:        (T4, R4, D4, P4)
    pstock5:        (T5, R5, D5, P5)
    pstock6:        (T6, R6, D6, P6)
    pstock7:        (T7, R7, D7, P7)

    dstock1:        (T1, R1, D1)
    dstock2:        (T2, R2, D2)
    dstock3:        (T3, R3, D3)
    dstock4:        (T4, R4, D4)
    dstock5:        (T5, R5, D5)
    dstock6:        (T6, R6, D6)
    dstock7:        (T7, R7, D7)

    rstock1:        (T1, R1, D1)
    rstock2:        (T2, R2, D2)
    rstock3:        (T3, R3, D3)
    rstock4:        (T4, R4, D4)
    rstock5:        (T5, R5, D5)
    rstock6:        (T6, R6, D6)
    rstock7:        (T7, R7, D7)

    tstock1:        (T1, R1, D1)
    tstock2:        (T2, R2, D2)
    tstock3:        (T3, R3, D3)
    tstock4:        (T4, R4, D4)
    tstock5:        (T5, R5, D5)
    tstock6:        (T6, R6, D6)
    tstock7:        (T7, R7, D7)

    piecemin1:      (L1, P1)
    piecemin2:      (L2, P2)
    piecemin3:      (L3, P3)
    piecemin4:      (L4, P4)
    piecemin5:      (L5, P5)
    piecemin6:      (L6, P6)
    piecemin7:      (L7, P7)

    nodemax1:       (L1, P1)
    nodemax2:       (L2, P2)
    nodemax3:       (L3, P3)
    nodemax4:       (L4, P4)
    nodemax5:       (L5, P5)
    nodemax6:       (L6, P6)
    nodemax7:       (L7, P7)
    '''

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
        self.__X = {"L2", "L3", "L4", "L5", "L6", "L7"}
        self.__C = {
            "lendec2":        {"L2", "L3"},
            "lendec3":        {"L3", "L4"},
            "lendec4":        {"L4", "L5"},
            "lendec5":        {"L5", "L6"},
            "lendec6":        {"L6", "L7"},
            "lendeclower2":   {"L2", "L3"},
            "lendeclower3":   {"L3", "L4"},
            "lendeclower4":   {"L4", "L5"},
            "lendeclower5":   {"L5", "L6"}
        }
        self.__csp = CSP(self.__X, self.__C)
        current = op.dirname(__file__)
        self.__catalog = CATALOG()
        self.__catalog.setup(current+"/real_pieces.csv")
        UNARY.init_domains(self.__csp, self.__catalog)
        UNARY.unarify(self.__csp, specs["C"])
        self.__mac = MAC(self.__csp, self.__catalog, specs["C"])
        
    def test_L2_propagates_to_all(self):
        # act
        res = self.__mac.propagate({"L2"})
        self.assertEqual(res[0], MADE_CONSISTENT)
        self.__assert_domains_are_consistent()

    def test_L4_propagates_to_all(self):
        # act
        res = self.__mac.propagate({"L4"})
        self.assertEqual(res[0], MADE_CONSISTENT)
        self.__assert_domains_are_consistent()
    
    def test_L2_gets_established(self):
        # arrange
        self.__csp.assign("L2", 80)
        # act
        res = self.__mac.establish("L2", 80)
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
        res = self.__mac.establish("L7", 100)
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