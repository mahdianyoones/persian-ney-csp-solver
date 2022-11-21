import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
sp.append(parent)

from csp import CSP
from sameround import SAMEROUND
from constants import *
import case_runner

class test_SAMEROUND(unittest.TestCase):
    '''Tests the behavior of sameround constraint.'''

    def setUp(self):
        self.__csp = CSP()
        self.__sut = SAMEROUND()
        self.__case_runner = case_runner.test_CASE_RUNNER()
    
    def test_establish_reduces_all(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"R2": 2.5},
            "D": {
                "R1": {2.5, 2},
                "R2": {2.5, 5, 4},
                "R3": {0, 2.5},
                "R4": {0, 2.5},
                "R5": {0, 2.5},
                "R6": {0, 2.5},
                "R7": {0, 2.5}
            },
            "curvar": "R2",
            "value": 2.5
        }
        expect = {
            "out": (MADE_CONSISTENT, {"R1", "R3", "R4", "R5", "R6", "R7"}),
            "D": {
                "R1": {2.5},
                "R2": {2.5, 5, 4},
                "R3": {2.5},
                "R4": {2.5},
                "R5": {2.5},
                "R6": {2.5},
                "R7": {2.5}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_contradiction_occurs(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"R2": 2.5},
            "D": {
                "R1": {0},
                "R2": {2.5},
                "R3": {0, 2.5},
                "R4": {0, 2.5},
                "R5": {0, 2.5},
                "R6": {0, 2.5},
                "R7": {0, 2.5}
            },
            "curvar": "R2",
            "value": 2.5
        }
        expect = {
            "out": (CONTRADICTION, {"R1", "R3", "R4", "R5", "R6", "R7"})
        }
        assert_constraint(csp, sut, "establish", given, expect)
    
    def test_establishes_once_only(self):
        '''Enforces the case that the algorithm simply does nothing!
        
        The algorithm only checks domains if THE FIRST R variable is being
        established. Otherwise, we are sure that domains are consistent AND further
        reduction is impossible.
        
        The domains remain intact in this case, and they are NOT examined.'''
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"R1": 2.5},
            "D": {
                "R1": {2.5},
                "R2": {2.5},
                "R3": {2.5},
                "R4": {2.5},
                "R5": {2.5},
                "R6": {2.5},
                "R7": {2.5}
            },
            "curvar": "R2",
            "value": 2.5
        }
        expect = {
            "out": REVISED_NONE
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_all_contain_the_same_value(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "R1": {2.5},
                "R2": {2.5},
                "R3": {2.5},
                "R4": {2.5},
                "R5": {2.5},
                "R6": {2.5},
                "R7": {2.5}
            },
            "curvar": "R1",
            "value": 2.5
        }
        expect = {
            "out": ALREADY_CONSISTENT
        }
        assert_constraint(csp, sut, "establish", given, expect)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_SAMEROUND)
    runner.run(suite)        