import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
sp.append(parent)


from csp import CSP
from lendec_lower import LENDEC_LOWER
from constants import *
import case_runner

class test_LENDEC_LOWER(unittest.TestCase):
    '''Tests the behavior of len decrement constraint.'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = LENDEC_LOWER()
        self.__case_runner = case_runner.test_CASE_RUNNER()

    def test_consistency_is_eatablished_after_assignment(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"L3": 90},
            "D": {
                "L4": {"min": 59, "max": 91},
            },
            "curvar": "L3",
            "value": 90,
            "participants": {"L3", "L4"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"L4"}),
            "D": {
                "L4": {"min": 60, "max": 91},
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_consistency_is_established_after_propagation(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L3": {"min": 90, "max": 95},
                "L4": {"min": 59, "max": 96},
            },
            "reduced_vars": {"L3"},
            "participants": {"L3", "L4"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"L4"}),
            "D": {
                "L4": {"min": 60, "max": 96},
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_domains_are_found_consistent_after_assignment(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"L3": 93},
            "D": {
                "L4": {"min": 62, "max": 96},
            },
            "curvar": "L3",
            "value": 93,
            "participants": {"L3", "L4"}
        }
        expect = {
            "out": ALREADY_CONSISTENT,
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_domains_are_found_consistent_after_propagation(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L3": {"min": 90, "max": 95},
                "L4": {"min": 60, "max": 96},
            },
            "reduced_vars": {"L3"},
            "participants": {"L3", "L4"}
        }
        expect = {
            "out": ALREADY_CONSISTENT,
        }
        assert_constraint(csp, sut, "propagate", given, expect)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_LENDEC_LOWER)
    runner.run(suite)