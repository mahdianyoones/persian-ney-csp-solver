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
            "A": {"P2": (1,1,1,2.5,1)},
            "D": {
                "P1": {(1,1,1,2,1), (1,1,1,2.5,1)},
                "P2": {(1,1,1,5,1), (1,1,1,2.5,1), (1,1,1,4,1)},
                "P3": {(1,1,1,0,1), (1,1,1,2.5,1)},
                "P4": {(1,1,1,0,1), (1,1,1,2.5,1)},
                "P5": {(1,1,1,0,1), (1,1,1,2.5,1)},
                "P6": {(1,1,1,0,1), (1,1,1,2.5,1)},
                "P7": {(1,1,1,0,1), (1,1,1,2.5,1)}
            },
            "curvar": "P2",
            "value": (1,1,1,2.5,1),
            "participants": {"P1", "P2", "P3", "P4", "P5", "P6", "P7"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"P1", "P3", "P4", "P5", "P6", "P7"}),
            "D": {
                "P1": {(1,1,1,2.5,1)},
                "P2": {
                    (1,1,1,2.5,1),
                    (1,1,1,5,1),
                    (1,1,1,4,1)
                },
                "P3": {(1,1,1,2.5,1)},
                "P4": {(1,1,1,2.5,1)},
                "P5": {(1,1,1,2.5,1)},
                "P6": {(1,1,1,2.5,1)},
                "P7": {(1,1,1,2.5,1)}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_contradiction_occurs(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"P2": (1,1,1,2.5,1)},
            "D": {
                "P1": {(1,1,1,0,1)},
                "P2": {(1,1,1,2.5,1)},
                "P3": {(1,1,1,0,1), (1,1,1,2.5,1)},
                "P4": {(1,1,1,0,1), (1,1,1,2.5,1)},
                "P5": {(1,1,1,0,1), (1,1,1,2.5,1)},
                "P6": {(1,1,1,0,1), (1,1,1,2.5,1)},
                "P7": {(1,1,1,0,1), (1,1,1,2.5,1)}
            },
            "curvar": "P2",
            "value": (1,1,1,2.5,1),
            "participants": {"P1", "P2", "P3", "P4", "P5", "P6", "P7"}
        }
        expect = {
            "out": (CONTRADICTION, {"P1", "P3", "P4", "P5", "P6", "P7"})
        }
        assert_constraint(csp, sut, "establish", given, expect)
    
    def test_establishes_once_only(self):
        '''Enforces the case that the algorithm simply does nothing!
        
        The algorithm only checks domains if THE FIRST P variable is being
        established. Otherwise, we are sure that domains are consistent AND further
        reduction is impossible.
        
        The domains remain intact in this case, and they are NOT examined.'''
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"P1": (1,1,1,2.5,1)},
            "D": {
                "P1": {(1,1,1,2.5,1)},
                "P2": {(1,1,1,2.5,1)},
                "P3": {(1,1,1,2.5,1)},
                "P4": {(1,1,1,2.5,1)},
                "P5": {(1,1,1,2.5,1)},
                "P6": {(1,1,1,2.5,1)},
                "P7": {(1,1,1,2.5,1)}
            },
            "curvar": "P2",
            "value": (1,1,1,2.5,1),
            "participants": {"P1", "P2", "P3", "P4", "P5", "P6", "P7"}
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
                "P1": {(1,1,1,2.5,1)},
                "P2": {(1,1,1,2.5,1)},
                "P3": {(1,1,1,2.5,1)},
                "P4": {(1,1,1,2.5,1)},
                "P5": {(1,1,1,2.5,1)},
                "P6": {(1,1,1,2.5,1)},
                "P7": {(1,1,1,2.5,1)}
            },
            "curvar": "P1",
            "value": (1,1,1,2.5,1),
            "participants": {"P1", "P2", "P3", "P4", "P5", "P6", "P7"}
        }
        expect = {
            "out": ALREADY_CONSISTENT
        }
        assert_constraint(csp, sut, "establish", given, expect)

if __name__ == "__main__":
    unittest.main()