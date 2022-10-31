import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
grandparent = op.dirname(op.dirname(current))
sp.append(grandparent)

from csp import CSP
from stock import STOCK
from constants import *
from catalog import CATALOG
from unary import UNARY

class test_STOCK(unittest.TestCase):
    '''Tests the behavior of stock constraints.'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__catalog = CATALOG()
        self.__catalog.setup()
        pieces = [
          # (T, D,  R, L)
            [1, 18, 0, 10],
            [1, 19, 0, 10],
            [1, 19, 0, 10],
            [2, 19, 1, 10],
            [2, 19, 0, 10],
            [3, 20, 2, 10]
        ]
        for piece in pieces:
            self.__catalog.add_piece(piece[0], piece[1], piece[2], piece[3]) 
        self.__sut = STOCK(self.__catalog)
    
    def __set_domains(self):
        csp = self.__csp
        T_vals = self.__catalog.values("T")
        R_vals = self.__catalog.values("R")
        D_vals = self.__catalog.values("D")
        l = self.__catalog.l()
        csp.update_domain("T1", T_vals)
        csp.update_domain("D1", D_vals)
        csp.update_domain("R1", R_vals)
        csp.update_domain("L1", {"min": 1, "max": l})

    def test_initial_domains(self):
        csp = self.__csp
        # act
        self.__set_domains()
        # assess
        D = csp.get_domains()
        self.assertEqual(D["T1"], {1, 2, 3})
        self.assertEqual(D["R1"], {0, 1, 2})
        self.assertEqual(D["D1"], {18, 19, 20})
        self.assertEqual(D["L1"], {"min": 1, "max": 60}) 

    def tests_finds_no_pieces(self):
        csp = self.__csp
        cases = [
            {
                "A": {"D1": 18, "R1": 1},
                "curvar": "R1",
                "val": 1
            },
            {
                "A": {"R1": 18, "T1": 1},
                "curvar": "T1",
                "val": 1
            },
            {
                "A": {"R1": 18, "T1": 1},
                "curvar": "R1",
                "val": 1
            }
        ]
        for case in cases:
            # arrange
            for var, val in case["A"].items():
                csp.assign(var, val)
            # act
            out = self.__sut.establish(csp, case["curvar"], case["val"])
            # assess
            self.assertEqual(out[0], CONTRADICTION)
            csp.unassign_all()
            self.__set_domains()

    def tests_finds_pieces(self):
        csp = self.__csp
        D = csp.get_domains()
        cases = [
            {
                "A": {"T1": 1, "R1": 0, "D1": 19},
                "curvar": "R1",
                "val": 0,
                "examined": {"L1"},
                "reduced": {"L1"},
                "D": {
                    "L1": {"min": 1, "max": 20}
                }
            },
            {
                "A": {"R1": 0, "D1": 19},
                "curvar": "R1",
                "val": 0,
                "examined": {"L1", "T1"},
                "reduced": {"L1", "T1"},
                "D": {
                    "T1": {1, 2},
                    "L1": {"min": 1, "max": 30}
                }
            },
            {
                "A": {"T1": 2, "D1": 19},
                "curvar": "t1",
                "val": 2,
                "examined": {"L1", "R1"},
                "reduced": {"L1", "R1"},
                "D": {
                    "R1": {1, 0},
                    "L1": {"min": 1, "max": 20}
                }
            },
            {
                "A": {"R1": 0},
                "curvar": "R1",
                "val": 0,
                "examined": {"L1", "T1", "D1"},
                "reduced": {"L1", "T1", "D1"},
                "D": {
                    "T1": {1, 2},
                    "D1": {18, 19},
                    "L1": {"min": 1, "max": 40}
                }
            },
            {
                "A": {"R1": 0},
                "curvar": "R1",
                "val": 0,
                "examined": {"L1", "T1", "D1"},
                "reduced": {"L1", "T1", "D1"},
                "D": {
                    "T1": {1, 2},
                    "D1": {18, 19},
                    "L1": {"min": 1, "max": 40}
                }
            }
        ]
        for case in cases:
            # arrange
            self.__set_domains()
            for var, val in case["A"].items():
                csp.assign(var, val)
            # act
            out = self.__sut.establish(csp, case["curvar"], case["val"])
            # assess
            self.assertEqual(out[0], DOMAINS_REDUCED)
            self.assertEqual(out[1], case["examined"])
            self.assertEqual(out[2], case["reduced"])
            for var, expected_domain in case["D"].items():
                self.assertEqual(D[var], expected_domain)
            csp.unassign_all()

    def test_does_not_find_enough_pieces(self):
        # arrange
        self.__set_domains()
        csp = self.__csp
        csp.assign("D1", 19)
        csp.assign("R1", 0)
        csp.assign("T1", 1)
        csp.update_domain("L1", {"min": 21, "max": 100}) # arbitrary upper
        # act
        out = self.__sut.establish(csp, "T1", 1)
        # assess
        D = csp.get_domains()
        self.assertEqual(out[0], CONTRADICTION)
        self.assertEqual(out[1], {"L1"})
        self.assertEqual(out[2], {"D1", "R1", "T1"})

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_STOCK)
    runner.run(suite)        