import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
grandparent = op.dirname(op.dirname(current))
sp.append(parent)
sp.append(grandparent)

from csp import CSP
from exclusive import EXCLUSIVE
from constants import *
from unary import UNARY
import case_runner

class test_EXCLUSIVE(unittest.TestCase):
    '''Tests the behavior of exclusive consistency algorithm.
    
    
    Cases:

    Nothing is revised
    Some pieces are removed and consistency is achieved
    Some L[max] are adjusted and consistency is achieved
    Both pieces are removed and some L[max] are adjusted and consistency is achieved
    Some pieces are removed and contradiction occurs
    '''
    
    def setUp(self):
        self.__X = {
            "P1", "P2", "P3", "P4", "P5",
            "L1", "L2", "L3", "L4", "L5"
        }
        C = {
            "exclusive": self.__X
        }
        self.__csp = CSP(X=self.__X, C=C)
        self.__sut = EXCLUSIVE()
        self.__case_runner = case_runner.test_CASE_RUNNER()
    
    def test_propagate_revises_nothing(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "reduced_vars": {"P1", "P2"},
            "participants": self.__X
        }
        expect = {
            "out": REVISED_NONE
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def __reduction_in_one_L_propagates_to_all(self, reduced_vars):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {
                "P1": ('01', 100.0, 2.0, 0.0, 19.0),
                "P2": ('01', 100.0, 2.0, 0.0, 19.0),
                "P3": ('01', 100.0, 2.0, 0.0, 19.0),
                "L2": 25,
            },
            "D": {
                "L1": {"min": 50, "max": 100},      # => 50, 51
                "L3": {"min": 24, "max": 100},      # => 24, 25
                "L4": {"min": 2, "max": 100},
                "L5": {"min": 1, "max": 100},
                "P4": {
                    ('01', 100.0, 2.0, 0.0, 19.0),  # gets removed
                    ('02', 60.0, 1.0, 0.5, 15.0)
                },
                "P5": {
                    ('01', 100.0, 2.0, 0.0, 19.0),  # remains
                    ('02', 60.0, 1.0, 0.5, 15.0)
                },
            },
            "reduced_vars": reduced_vars,
            "participants": self.__X
        }
        expect = {
            "out": (MADE_CONSISTENT, {"L1", "L3", "P4"}),
            "D": {
                "L1": {"min": 50, "max": 51},
                "L3": {"min": 24, "max": 25},
                "P4": {
                    ('02', 60.0, 1.0, 0.5, 15.0)
                }
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_L_reduction_propagates_to_all(self):
        self.__reduction_in_one_L_propagates_to_all({"L1"})
        self.__reduction_in_one_L_propagates_to_all({"L4"})
        self.__reduction_in_one_L_propagates_to_all({"L1", "L4"})

    def test_reduction_in_one_L_causes_contradiction(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {
                "P1": ('01', 100.0, 2.0, 0.0, 19.0),
                "P2": ('01', 100.0, 2.0, 0.0, 19.0),
                "P3": ('01', 100.0, 2.0, 0.0, 19.0),
            },
            "D": {
                "L1": {"min": 50, "max": 100},      # => 50, 51
                "L2": {"min": 25, "max": 100},      # => 25, 26
                "L3": {"min": 24, "max": 100},      # => 24, 25
                "L4": {"min": 2, "max": 100},      # no change
                "L5": {"min": 1, "max": 100},
                "P4": {
                    ('01', 100.0, 2.0, 0.0, 19.0),  # gets removed
                },
                "P5": {
                    ('01', 100.0, 2.0, 0.0, 19.0),  # remains
                    ('02', 60.0, 1.0, 0.5, 15.0)
                },
            },
            "reduced_vars": {"L4"},
            "participants": self.__X
        }
        expect = {
            "out": (CONTRADICTION, {"P4"}),
        }
        assert_constraint(csp, sut, "propagate", given, expect)

if __name__ == "__main__":
    unittest.main()