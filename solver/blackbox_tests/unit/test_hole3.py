import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
grandparent = op.dirname(op.dirname(current))
sp.append(grandparent)

from csp import CSP
from hole3 import HOLE3
from constants import *
import case_runner

class Test_HOLE3(unittest.TestCase):
    '''Tests the behavior of hole3 constraint.'''
            
    def setUp(self):
        self.__csp = CSP()
        hmarg = 10
        h3 = 371
        self.__sut = HOLE3(h3, hmarg)
        self.__case_runner = case_runner.test_CASE_RUNNER()

    def __set_domains(self):
        domain = {"min": 1, "max": 1000}
        for var in {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}:
            self.__csp.update_domain(var, domain)	
    
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
            "curvar": "L4",
            "value": 24
        }
        expect = {
            "out": (CONTRADICTION, {"L1"}, {"L2", "L3", "L4"})
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_domains_remain_intact(self):
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
            "reduced_vars": {"L1", "L2", "L3"},
        }
        expect = {
            "out": (DOMAINS_INTACT, {"L1", "L2", "L3", "L4"})
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
            "reduced_vars": {"L1", "L2", "L3"},
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L1", "L2", "L3", "L4"},
                {"L1", "L2", "L3", "L4"}),
            "D": {
                "L1": {"min": 190, "max": 190},
                "L2": {"min": 24, "max": 24},
                "L3": {"min": 122, "max": 122},
                "L4": {"min": 24, "max": 24}
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)
        
if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(Test_HOLE3)
    runner.run(suite)