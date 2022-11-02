import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
grandparent = op.dirname(op.dirname(current))
sp.append(grandparent)

from csp import CSP
from hole6 import HOLE6
from constants import *
import case_runner

class test_HOLE6(unittest.TestCase):
    '''Tests the behavior of hole6 constraint.'''
            
    def setUp(self):
        self.__csp = CSP()
        hmarg = 10
        h6 = 467
        self.__sut = HOLE6(h6, hmarg)
        self.__case_runner = case_runner.test_CASE_RUNNER()
    
    def test_contradiction_is_detected(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"L2": 24, "L3": 61, "L4": 24, "L5": 61},
            "D": {
                "L1": {"min": 287, "max": 287},
            },
            "curvar": "L3",
            "value": 61
        }
        expect = {
            "out": (CONTRADICTION, {"L1"}, {"L2", "L3", "L4", "L5"})
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_domains_are_already_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L1": {"min": 286, "max": 286},
                "L2": {"min": 24, "max": 24},
                "L3": {"min": 61, "max": 61},
                "L4": {"min": 24, "max": 24},
                "L5": {"min": 61, "max": 61},

            },
            "reduced_vars": {"L1", "L2", "L3", "L4"},
        }
        expect = {
            "out": (DOMAINS_INTACT, {"L1", "L2", "L3", "L4", "L5"})
        }
        assert_constraint(csp, sut, "propagate", given, expect)
        
    def test_domains_are_reduced(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L1": {"min": 286, "max": 287},
                "L2": {"min": 24, "max": 25},
                "L3": {"min": 61, "max": 62},
                "L4": {"min": 24, "max": 25},
                "L5": {"min": 61, "max": 62},
            },
            "reduced_vars": {"L1", "L2", "L3", "L4"},
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L1", "L2", "L3", "L4", "L5"},
                {"L1", "L2", "L3", "L4", "L5"}),
            "D": {
                "L1": {"min": 286, "max": 286},
                "L2": {"min": 24, "max": 24},
                "L3": {"min": 61, "max": 61},
                "L4": {"min": 24, "max": 24},
                "L5": {"min": 61, "max": 61},
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)
        
if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_HOLE6)
    runner.run(suite)		
