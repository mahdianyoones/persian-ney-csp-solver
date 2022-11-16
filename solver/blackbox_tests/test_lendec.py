import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
grandparent = op.dirname(op.dirname(current))
sp.append(parent)
sp.append(grandparent)

from csp import CSP
from lendec import LENDEC
from constants import *
import case_runner

class test_LENDEC(unittest.TestCase):
    '''Tests the behavior of len decrement constraint.'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = LENDEC()
        self.__case_runner = case_runner.test_CASE_RUNNER()

    def test_establish_finds_all_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L2": {"min": 11, "max": 50},
                "L3": {"min": 10, "max": 49},
            },
            "A": {"L3": 10},
            "curvar": "L3",
            "value": 10,
            "participants": {"L2", "L3"}
        }
        expect = {
            "out": ALREADY_CONSISTENT,
        }
        assert_constraint(csp, sut, "establish", given, expect)
    
    def test_propagate_finds_all_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L2": {"min": 11, "max": 50},
                "L3": {"min": 10, "max": 49}
            },
            "reduced_vars": {"L2"},
            "participants": {"L2", "L3"}
        }
        expect = {
            "out": ALREADY_CONSISTENT,
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_establish_makes_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L2": {"min": 11, "max": 50},
                "L3": {"min": 10, "max": 49},
            },
            "A": {"L3": 11},
            "curvar": "L3",
            "value": 11,
            "participants": {"L2", "L3"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"L2"}),
            "D": {
                "L2": {"min": 12, "max": 50},
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_propagates_makes_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L2": {"min": 11, "max": 50},
                "L3": {"min": 11, "max": 50},
            },
            "reduced_vars": {"L2"},
            "participants": {"L2", "L3"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"L2", "L3"}),
            "D": {
                "L2": {"min": 12, "max": 50},
                "L3": {"min": 11, "max": 49},
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_propagate_detects_contradiction(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L2": {"min": 11, "max": 50},
                "L3": {"min": 50, "max": 50},
            },
            "reduced_vars": {"L2"},
            "participants": {"L2", "L3"}
        }
        expect = {
            "out": CONTRADICTION
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_establish_does_no_revision(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"L2": 12, "L3": 11},
            "curvar": "L3",
            "value": 11,
            "participants": {"L2", "L3"}
        }
        expect = {
            "out": REVISED_NONE
        }
        assert_constraint(csp, sut, "establish", given, expect)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_LENDEC)
    runner.run(suite)