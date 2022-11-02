import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
grandparent = op.dirname(op.dirname(current))
sp.append(parent)
sp.append(grandparent)

from csp import CSP
from stock import STOCK
from constants import *
from catalog import CATALOG
import case_runner

class test_STOCK(unittest.TestCase):
    '''Tests the behavior of stock constraints along with catalog.'''
    
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
        self.__case_runner = case_runner.test_CASE_RUNNER()

    def __get_initial_domains(self):
        T_vals = self.__catalog.values("T")
        R_vals = self.__catalog.values("R")
        D_vals = self.__catalog.values("D")
        l = self.__catalog.l()
        return (T_vals, R_vals, D_vals, l)

    def tests_establish_detects_contradiction(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        (T_vals, R_vals, D_vals, l) = self.__get_initial_domains()
        given = {
            "A": {"D1": 18, "R1": 1},
            "D": {
                "T1": T_vals,
                "L1": {"min": 1, "max": l}
            },
            "curvar": "R1",
            "value": 1
        }
        expect = {
            "out": (CONTRADICTION, set([]), {"D1", "R1"})
        }
        assert_constraint(csp, sut, "establish", given, expect)
        given = {
            "A": {"D1": 18, "T1": 2},
            "D": {
                "R1": R_vals,
                "L1": {"min": 1, "max": l}
            },
            "curvar": "T1",
            "value": 2
        }
        expect = {
            "out": (CONTRADICTION, set([]), {"D1", "T1"})
        }
        assert_constraint(csp, sut, "establish", given, expect)
        given = {
            "A": {"T1": 1, "R1": 1},
            "D": {
                "D1": D_vals,
                "L1": {"min": 1, "max": l}
            },
            "curvar": "R1",
            "value": 1
        }
        expect = {
            "out": (CONTRADICTION, set([]), {"T1", "R1"})
        }
        assert_constraint(csp, sut, "establish", given, expect)
    
    def tests_finds_pieces(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        (T_vals, R_vals, D_vals, l) = self.__get_initial_domains()
        given = {
            "A": {"T1": 1, "R1": 0, "D1": 19},
            "D": {
                "L1": {"min": 1, "max": l}
            },
            "curvar": "R1",
            "value": 0
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L1"}, {"L1"}),
            "D": {
                "L1": {"min": 1, "max": 20}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)
        given = {
            "A": {"R1": 0, "D1": 19},
            "D": {
                "T1": T_vals,
                "L1": {"min": 1, "max": l}
            },
            "curvar": "R1",
            "value": 0
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L1", "T1"}, {"L1", "T1"}),
            "D": {
                "L1": {"min": 1, "max": 30},
                "T1": {1, 2}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)
        given = {
            "A": {"T1": 2, "D1": 19},
            "D": {
                "R1": R_vals,
                "L1": {"min": 1, "max": l}
            },
            "curvar": "T1",
            "value": 2
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L1", "R1"}, {"L1", "R1"}),
            "D": {
                "L1": {"min": 1, "max": 20},
                "R1": {1, 0}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)
        given = {
            "A": {"R1": 0},
            "D": {
                "T1": T_vals,
                "D1": D_vals,
                "L1": {"min": 1, "max": l}
            },
            "curvar": "R1",
            "value": 0
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L1", "T1", "D1"}, {"L1", "T1", "D1"}),
            "D": {
                "T1": {1, 2},
                "D1": {18, 19},
                "L1": {"min": 1, "max": 40}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)
        given = {
            "A": {"R1": 0},
            "D": {
                "T1": T_vals,
                "D1": D_vals,
                "L1": {"min": 1, "max": l}
            },
            "curvar": "R1",
            "value": 0
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L1", "T1", "D1"}, {"L1", "T1", "D1"}),
            "D": {
                "T1": {1, 2},
                "D1": {18, 19},
                "L1": {"min": 1, "max": 40}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_does_not_find_enough_pieces(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"D1": 19, "T1": 1, "R1": 0},
            "D": {
                "L1": {"min": 21, "max": 100}
            },
            "curvar": "T1",
            "value": 1
        }
        expect = {
            "out": (CONTRADICTION, set([]), {"T1", "R1", "D1"}),
        }
        assert_constraint(csp, sut, "establish", given, expect)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_STOCK)
    runner.run(suite)        