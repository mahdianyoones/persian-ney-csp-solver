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
    binary constraints as follows:
    
    1- P1 & P2
    2- P2 & P3
    3- P3 & P4
    4- P4 & P5
    5- P5 & P6
    6- P6 & P7
    
    Every call to establish or propagate only revises the variables of one
    of these 6 constraints.'''
    
    def setUp(self):
        self.__csp = CSP(S=2)
        self.__spec = {
            "ddiff":    {"min": 0.5, "max": 1.0},                
        }
        self.__sut = DIAMDEC()
        self.__case_runner = case_runner.test_CASE_RUNNER()
    
    def test_establish_finds_all_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"P1": (1, 1, 1, 1, 14)},
            "D": {
                "P2": {(0, 0, 0, 0, 13)},
            },
            "spec": self.__spec,
            "curvar": "P1",
            "value": (1, 1, 1, 1, 14),
            "participants": {"P1", "P2"}
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
                "P1": {(1, 1, 1, 1, 14), (1, 1, 1, 1, 15)},
                "P2": {(1, 1, 1, 1, 13), (1, 1, 1, 1, 14)},
            },
            "spec": self.__spec,
            "reduced_vars": {"P1"},
            "participants": {"P1", "P2"}
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
            "A": {"P6": (1, 1, 1, 1, 10)},
            "D": {
                "P7": {
                    (1, 1, 1, 1, 5),
                    (1, 1, 1, 1, 8),
                    (1, 1, 1, 1, 8.5),
                    (1, 1, 1, 1, 9),
                    (1, 1, 1, 1, 9.5),
                    (1, 1, 1, 1, 10),
                    (1, 1, 1, 1, 10.5),
                    (1, 1, 1, 1, 11),
                    (1, 1, 1, 1, 11.5),
                    (1, 1, 1, 1, 13)
                }
            },
            "spec": self.__spec,
            "curvar": "P6",
            "value": (1, 1, 1, 1, 10),
            "participants": {"P6", "P7"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"P7"}),
            "D": {
                "P7": {
                    (1, 1, 1, 1, 9),
                    (1, 1, 1, 1, 9.5)
                }
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_establish_detects_contradiction(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"P6": (1, 1, 1, 1, 10)},
            "D": {
                "P7": {
                    (1, 1, 1, 1, 5),
                    (1, 1, 1, 1, 8.9)                    
                },
            },
            "spec": self.__spec,
            "curvar": "P6",
            "value": (1, 1, 1, 1, 10),
            "participants": {"P6", "P7"}
        }
        expect = {
            "out": (CONTRADICTION, {"P7"})
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_propagate_detects_contradiction(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "P6": {
                    (1, 1, 1, 1, 10),
                    (1, 1, 1, 1, 11)
                },
                "P7": {
                    (1, 1, 1, 1, 5),
                    (1, 1, 1, 1, 8.9)                    
                },
            },
            "spec": self.__spec,
            "reduced_vars": {"P6"},
            "participants": {"P6", "P7"}
        }
        expect = {
            "out": (CONTRADICTION, {"P6"})
        }
        assert_constraint(csp, sut, "propagate", given, expect)

if __name__ == "__main__":
    unittest.main()