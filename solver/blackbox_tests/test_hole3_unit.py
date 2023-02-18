import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
grandparent = op.dirname(op.dirname(current))
sp.append(parent)
sp.append(grandparent)

from csp import CSP
from hole3 import HOLE3
from constants import *
import case_runner

class Test_HOLE3(unittest.TestCase):
    '''Tests the behavior of hole3 constraint.'''
            
    def setUp(self):
        self.__csp = CSP(S=2)
        self.__spec = {
            "h3": 371,
            "hmarg": 10,
            "mp": 0
        }
        self.__sut = HOLE3(self.__csp)
        self.__case_runner = case_runner.test_CASE_RUNNER()
    
    def test_contradiction_is_detected(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        # case 1
        given = {
            "A": {"L2": 24, "L3": 122, "L4": 24},
            "D": {
                "L1": {"min": 191, "max": 191},
            },
            "participants": {"L1", "L2", "L3", "L4"},
            "spec": self.__spec,
            "curvar": "L4",
            "value": 24
        }
        expect = {
            "out": (CONTRADICTION, {"L1"})
        }
        # case 2
        given = {
            "A": {"L9": 24, "L10": 122, "L11": 24},
            "D": {
                "L8": {"min": 191, "max": 191},
            },
            "participants": {"L8", "L9", "L10", "L11"},
            "spec": self.__spec,
            "curvar": "L11",
            "value": 24
        }
        expect = {
            "out": (CONTRADICTION, {"L8"})
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_domains_are_already_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L1": {"min": 190, "max": 190},
                "L2": {"min": 24, "max": 24},
                "L3": {"min": 122, "max": 122},
                "L4": {"min": 24, "max": 24},
            },
            "participants": {"L1", "L2", "L3", "L4"},
            "spec": self.__spec,
            "reduced_vars": {"L1", "L2", "L3"},
        }
        expect = {
            "out": ALREADY_CONSISTENT
        }
        assert_constraint(csp, sut, "propagate", given, expect)
        
    def test_domains_are_reduced(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L1": {"min": 190, "max": 191},
                "L2": {"min": 24, "max": 25},
                "L3": {"min": 122, "max": 123},
                "L4": {"min": 24, "max": 25},
            },
            "participants": {"L1", "L2", "L3", "L4"},
            "spec": self.__spec,
            "reduced_vars": {"L1", "L2", "L3"},
        }
        expect = {
            "out": (MADE_CONSISTENT, {"L1", "L2", "L3", "L4"}),
            "D": {
                "L1": {"min": 190, "max": 190},
                "L2": {"min": 24, "max": 24},
                "L3": {"min": 122, "max": 122},
                "L4": {"min": 24, "max": 24}
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)
        
if __name__ == "__main__":
    unittest.main()