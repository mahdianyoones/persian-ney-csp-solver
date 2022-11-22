import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
grandparent = op.dirname(op.dirname(current))
sp.append(parent)
sp.append(grandparent)

from csp import CSP
from diamdec import DIAMDEC
from constants import *
import case_runner

class test_DIAMDEC(unittest.TestCase):
    '''Test the behavior of diameter decrement constraints.
    
    This consistency algorithm covers 6 similar constraints on 6
    groups of variables as follows:
    
    1- D1 & D2
    2- D2 & D3
    3- D3 & D4
    4- D4 & D5
    5- D5 & D6
    6- D6 & D7
    
    Every call to establish or propagate only revises the variables of one
    of these 6 constraints.'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = DIAMDEC({"min": 0.5, "max": 1.0})
        self.__case_runner = case_runner.test_CASE_RUNNER()
    
    def test_establish_finds_all_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"D1": 14},
            "D": {
                "D2": {13},
            },
            "curvar": "D1",
            "value": 14,
            "participants": {"D1", "D2"}
        }
        expect = {
            "out": ALREADY_CONSISTENT
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_propagate_finds_all_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "D1": {15, 14},
                "D2": {13, 14},
            },
            "reduced_vars": {"D1"},
            "participants": {"D1", "D2"}
        }
        expect = {
            "out": ALREADY_CONSISTENT
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_establish_makes_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"D6": 10},
            "D": {
                "D7": {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
            },
            "curvar": "D6",
            "value": 10,
            "participants": {"D6", "D7"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"D7"}),
            "D": {
                "D7": {9, 9.5}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_establish_detects_contradiction(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"D6": 10},
            "D": {
                "D7": {5, 8.9},
            },
            "curvar": "D6",
            "value": 10,
            "participants": {"D6", "D7"}
        }
        expect = {
            "out": (CONTRADICTION, {"D7"})
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_propagate_detects_contradiction(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "D6": {10, 11},
                "D7": {5, 8.9},
            },
            "reduced_vars": {"D6"},
            "participants": {"D6", "D7"}
        }
        expect = {
            "out": (CONTRADICTION, {"D6"})
        }
        assert_constraint(csp, sut, "propagate", given, expect)

if __name__ == "__main__":
    unittest.main()