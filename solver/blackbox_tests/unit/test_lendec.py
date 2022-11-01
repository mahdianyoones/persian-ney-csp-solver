import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
grandparent = op.dirname(op.dirname(current))
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

    def test_domains_are_reduced(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        # case 1
        given = {
            "D": {
                "L2": {"min": 41, "max": 50},
                "L3": {"min": 41, "max": 50},
                "L4": {"min": 40, "max": 49},
                "L5": {"min": 39, "max": 47},
                "L6": {"min": 38, "max": 48},
                "L7": {"min": 37, "max": 45}
            },
            "reduced_vars": {"L2", "L6"},
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L2", "L3", "L4", "L5", "L6", "L7"},
                {"L2", "L3", "L4", "L6"}),
            "D": {
                "L2": {"min": 42, "max": 50},
                "L3": {"min": 41, "max": 49},
                "L4": {"min": 40, "max": 48},
                "L6": {"min": 38, "max": 46},
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)
        # case 2
        given = {
            "D": {
                "L2": {"min": 50, "max": 100},
                "L3": {"min": 50, "max": 100},
                "L4": {"min": 50, "max": 100},
                "L5": {"min": 50, "max": 100},
                "L6": {"min": 50, "max": 100},
                "L7": {"min": 50, "max": 100}
            },
            "reduced_vars": {"L2"},
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L2", "L3", "L4", "L5", "L6", "L7"},
                {"L2", "L3", "L4", "L5", "L6", "L7"}),
            "D": {
                "L2": {"min": 55, "max": 100},
                "L3": {"min": 54, "max": 99},
                "L4": {"min": 53, "max": 98},
                "L5": {"min": 52, "max": 97},
                "L6": {"min": 51, "max": 96},
                "L7": {"min": 50, "max": 95},
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)
        # case 3
        given = {
            "A": {"L2": 50, "L5": 46},
            "D": {
                "L3": {"min": 48, "max": 50},
                "L4": {"min": 47, "max": 49},
            },
            "curvar": "L2",
            "value": 50
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L3", "L4"}, {"L3", "L4"}),
            "D": {
                "L3": {"min": 48, "max": 49},
                "L4": {"min": 47, "max": 48},
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_contradiction_is_detected(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        # case 1
        given = {
            "A": {"L2": 50},
            "D": {
                "L3": {"min": 50, "max": 50},
            },
            "curvar": "L2",
            "value": 50
        }
        expect = {
            "out": (CONTRADICTION, {"L3"}, {"L2"}),
        }
        assert_constraint(csp, sut, "establish", given, expect)
        # case 2
        given = {
            "D": {
                "L2": {"min": 50, "max": 100},
                "L3": {"min": 50, "max": 100},
                "L4": {"min": 50, "max": 100},
                "L5": {"min": 50, "max": 100},
                "L6": {"min": 50, "max": 100},
                "L7": {"min": 100, "max": 100},
            },
            "reduced_vars": {"L2"}
        }
        expect = {
            "out": (CONTRADICTION, {"L2", "L3", "L4", "L5", "L6", "L7"},
            set([])),
        }
        assert_constraint(csp, sut, "propagate", given, expect)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_LENDEC)
    runner.run(suite)