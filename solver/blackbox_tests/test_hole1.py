import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
grandparent = op.dirname(op.dirname(current))
sp.append(parent)
sp.append(grandparent)

from csp import CSP
from hole1 import HOLE1
from constants import *
import case_runner

class Test_HOLE1(unittest.TestCase):
    '''Tests the behavior of hole1 constraint.'''
            
    def setUp(self):
        self.__csp = CSP()
        hmarg = 10
        h1 = 312
        self.__sut = HOLE1(h1, hmarg)
        self.__case_runner = case_runner.test_CASE_RUNNER()
    
    def test_contradiction_is_detected(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        # case 1
        given = {
            "D": {
                "L1": {"min": 132, "max": 132},
                "L2": {"min": 48, "max": 48},
                "L3": {"min": 122, "max": 122}
            },
            "reduced_vars": {"L1"},
        }
        expect = {
            "out": CONTRADICTION
        }
        assert_constraint(csp, sut, "propagate", given, expect)
        # case 2
        given = {
            "A": {"L1": 132, "L2": 48},
            "D": {
                "L3": {"min": 122, "max": 122}
            },
            "curvar": "L2",
            "value": 48
        }
        expect = {
            "out": CONTRADICTION
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_domains_remain_intact(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L1": {"min": 131, "max": 131},
                "L2": {"min": 48, "max": 48},
                "L3": {"min": 122, "max": 122}
            },
            "reduced_vars": {"L1", "L2"},
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
                "L1": {"min": 131, "max": 132},
                "L2": {"min": 48, "max": 49},
                "L3": {"min": 122, "max": 123}
            },
            "reduced_vars": {"L1", "L2"},
        }
        expect = {
            "out": (MADE_CONSISTENT, {"L1", "L2", "L3"}),
            "D": {
                "L1": {"min": 131, "max": 131},
                "L2": {"min": 48, "max": 48},
                "L3": {"min": 122, "max": 122}
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(Test_HOLE1)
    runner.run(suite)		