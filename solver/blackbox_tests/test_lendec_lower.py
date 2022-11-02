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

    def test_domains_are_reduced(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        # case 1
        given = {
            "A": {"L2": 121, "L3": 90},
            "D": {
                "L4": {"min": 59, "max": 89},
                "L5": {"min": 39, "max": 88},
                "L6": {"min": 35, "max": 87}
            },
            "curvar": "L3",
            "value": 90
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L4", "L5", "L6"}, {"L4", "L5"}),
            "D": {
                "L4": {"min": 60, "max": 89},
                "L5": {"min": 40, "max": 88}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)
        # case 2
        given = {
            "D": {
                "L2": {"min": 90, "max": 172},
                "L3": {"min": 89, "max": 171},
                "L4": {"min": 88, "max": 170},
                "L5": {"min": 87, "max": 169},
                "L6": {"min": 30, "max": 248}
            },
            "reduced_vars": {"L2","L3","L4","L5","L6"},
            "value": 90
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L2","L3","L4","L5","L6"}, {"L6"}),
            "D": {
                "L6": {"min": 58, "max": 248}
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_contradiction_is_detected(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"L2": 90},
            "D": {
                "L3": {"min": 1, "max": 59},
            },
            "curvar": "L2",
            "value": 90
        }
        expect = {
            "out": (CONTRADICTION, {"L3"}, {"L2"}),
        }
        assert_constraint(csp, sut, "establish", given, expect)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_LENDEC_LOWER)
    runner.run(suite)