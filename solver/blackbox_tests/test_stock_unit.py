import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
grandparent = op.dirname(op.dirname(current))
sp.append(parent)
sp.append(grandparent)

from csp import CSP
from stock import PIECE_STOCK, THICK_STOCK, ROUND_STOCK, DIAM_STOCK
from constants import *
from catalog import CATALOG
from unary import UNARY
import case_runner

class test_STOCK(unittest.TestCase):
    '''Tests the behavior of stock constraints.
    
    There are 4 groups of constraints that involve making inquiry to catalog
    in order to establish consistency: tstock, rstock, dstock, & pstock.

    partitions:

    full behavior of pstock
    full behavior of tstock
    some behaviors rstock, and dstock.
    Assumes catalog is well-tested.'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__catalog = CATALOG(current+"/stock.csv")
        self.__sut_pstock = PIECE_STOCK(self.__catalog)
        self.__sut_tstock = THICK_STOCK(self.__catalog)
        self.__sut_rstock = ROUND_STOCK(self.__catalog)
        self.__sut_dstock = DIAM_STOCK(self.__catalog)
        UNARY.init_domains(self.__csp, self.__catalog)
        self.__case_runner = case_runner.test_CASE_RUNNER()

    def test_pstock_establishes_consistency(self):
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"R1": 0, "T1": 2, "D1": 14},
            "D": {
                "P1": {("6", 130), ("7", 60), ("4", 70)}
            },
            "curvar": "R1",
            "value": 0,
            "participants": {"R1", "T1", "D1", "P1"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"P1"}),
            "D": {
                "P1": {("6", 130), ("7", 60)}
            }
        }
        assert_constraint(csp, self.__sut_pstock, "establish", given, expect)

    def test_pstock_finds_all_consistent(self):
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"R1": 0, "D1": 13},
            "D": {
                "P1": {("9", 220), ("10", 300)}
            },
            "curvar": "R1",
            "value": 0,
            "participants": {"R1", "T1", "D1", "P1"}
        }
        expect = {
            "out": ALREADY_CONSISTENT
        }
        assert_constraint(csp, self.__sut_pstock, "establish", given, expect)

    def tests_pstock_establishes_after_P_assigned(self):
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "curvar": "P1",
            "value": ("11", 120),
            "participants": {"R1", "T1", "D1", "P1"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"D1", "T1", "R1"}),
            "D": {
                "D1": {12.4},
                "T1": {2},
                "R1": {0}
            }
        }
        assert_constraint(csp, self.__sut_pstock, "establish", given, expect)

    def tests_pstock_propagates_after_P_reduced(self):
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "P1": {("11", 120), ("3", 80)}
            },
            "reduced_vars": {"P1"},
            "participants": {"R1", "T1", "D1", "P1"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"D1", "T1", "R1"}),
            "D": {
                "D1": {12.4, 17},
                "T1": {2},
                "R1": {0}
            }
        }
        assert_constraint(csp, self.__sut_pstock, "propagate", given, expect)

    def test_pstock_detect_contradiction(self):
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"D1": 18, "R1": 1},
            "curvar": "R1",
            "value": 1,
            "participants": {"D1", "R1", "T1", "P1"}
        }
        expect = {
            "out": (CONTRADICTION, {"P1"})
        }
        assert_constraint(csp, self.__sut_pstock, "establish", given, expect)

    def test_tstock_detect_contradiction(self):
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"D1": 18, "R1": 1},
            "curvar": "R1",
            "value": 1,
            "participants": {"D1", "R1", "T1"}
        }
        expect = {
            "out": (CONTRADICTION, {"T1"})
        }
        assert_constraint(csp, self.__sut_tstock, "establish", given, expect)
    
    def tests_propagate_does_no_revision_in_all(self):
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "reduced_vars": {"R1"},
            "participants": {}
        }
        expect = {
            "out": REVISED_NONE
        }
        assert_constraint(csp, self.__sut_pstock, "propagate", given, expect)
        assert_constraint(csp, self.__sut_dstock, "propagate", given, expect)
        assert_constraint(csp, self.__sut_rstock, "propagate", given, expect)
        assert_constraint(csp, self.__sut_tstock, "propagate", given, expect)

if __name__ == "__main__":
    unittest.main()