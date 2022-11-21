import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
grandparent = op.dirname(op.dirname(current))
sp.append(parent)
sp.append(grandparent)

from csp import CSP
from len import LEN
from spec import specs
from constants import *
import case_runner

class test_LEN(unittest.TestCase):
    '''Test the behavior of len constraint.'''
    
    def setUp(self):
        self.__csp = CSP()
        len = 524
        self.__sut = LEN(len)
        self.__case_runner = case_runner.test_CASE_RUNNER()
    
    def test_contradiction_is_detected_by_propagate(self):
        '''Asserts two contradiction cases.

        in one which sum of the lower bounds are greater than len
        and in the other the sum of the upper bounds are smaller than len.'''
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        # case 1
        given = {
            "D": {
                "L1": {"min": 100, "max": 476},
                "L2": {"min": 100, "max": 86},
                "L3": {"min": 100, "max": 86},
                "L4": {"min": 100, "max": 86},
                "L5": {"min": 100, "max": 86},
                "L6": {"min": 12, "max": 86},
                "L7": {"min": 13, "max": 86}
            },
            "reduced_vars": {"L7"},
        }
        expect = {
            "out": (CONTRADICTION, {"L1", "L2", "L3", "L4", "L5", "L6", "L7"})
        }
        assert_constraint(csp, sut, "propagate", given, expect)
        # case 2
        given = {
            "D": {
                "L1": {"min": 1, "max": 100},
                "L2": {"min": 1, "max": 100},
                "L3": {"min": 1, "max": 100},
                "L4": {"min": 1, "max": 100},
                "L5": {"min": 1, "max": 100},
                "L6": {"min": 1, "max": 12},
                "L7": {"min": 1, "max": 11}
            },
            "reduced_vars": {"L7"},
        }
        expect = {
            "out": (CONTRADICTION, {"L1", "L2", "L3", "L4", "L5", "L6", "L7"})
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_contradiction_is_detected_by_establish(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        # case 1
        given = {
            "A": {"L1": 100, "L2": 100, "L3": 100, "L4": 100, "L5": 100, "L6": 20},
            "D": {
                "L7": {"min": 5, "max": 100}
            },
            "curvar": "L6",
            "value": 20
        }
        expect = {
            "out": (CONTRADICTION, {"L7"})
        }
        assert_constraint(csp, sut, "establish", given, expect)
        # case 2
        given = {
            "A": {"L1": 100, "L2": 100, "L3": 100, "L4": 100, "L5": 100, "L6": 20},
            "D": {
                "L7": {"min": 1, "max": 3}
            },
            "curvar": "L6",
            "value": 19
        }
        expect = {
            "out": (CONTRADICTION, {"L7"})
        }
        assert_constraint(csp, sut, "establish", given, expect)
        # case 3
        given = {
            "A": {"L1": 100, "L2": 100, "L3": 100, "L7": 19, "L5": 100, "L6": 20},
            "D": {
                "L4": {"min": 1, "max": 3}
            },
            "curvar": "L6",
            "value": 20
        }
        expect = {
            "out": (CONTRADICTION, {"L4"})
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_domains_are_reduced(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"L2": 100, "L3": 100, "L4": 100, "L5": 100, "L6": 20, "L7": 100},
            "D": {
                "L1": {"min": 3, "max": 5}
            },
            "curvar": "L6",
            "value": 20
        }
        expect = {
            "out": (MADE_CONSISTENT, {"L1"}),
            "D": {
                "L1": {"min": 4, "max": 4}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_LEN)
    runner.run(suite)