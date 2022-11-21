import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
grandparent = op.dirname(op.dirname(current))
sp.append(parent)
sp.append(grandparent)

from csp import CSP
from samethick import SAMETHICK
from constants import *
import case_runner

class test_SAMETHICK(unittest.TestCase):
    '''Tests the behavior of samethick constraint.'''

    def setUp(self):
        self.__csp = CSP()
        self.__sut = SAMETHICK()
        self.__case_runner = case_runner.test_CASE_RUNNER()
    
    def test_establish_reduces_all(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"T2": 2.5},
            "D": {
                "T1": {2.5, 2},
                "T2": {2.5, 5, 4},
                "T3": {0, 2.5},
                "T4": {0, 2.5},
                "T5": {0, 2.5},
                "T6": {0, 2.5},
                "T7": {0, 2.5}
            },
            "curvar": "T2",
            "value": 2.5
        }
        expect = {
            "out": (MADE_CONSISTENT,{"T1", "T3", "T4", "T5", "T6", "T7"}),
            "D": {
                "T1": {2.5},
                "T2": {2.5, 5, 4},
                "T3": {2.5},
                "T4": {2.5},
                "T5": {2.5},
                "T6": {2.5},
                "T7": {2.5}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_contradiction_occurs(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"T2": 2.5},
            "D": {
                "T1": {0},
                "T2": {2.5},
                "T3": {0, 2.5},
                "T4": {0, 2.5},
                "T5": {0, 2.5},
                "T6": {0, 2.5},
                "T7": {0, 2.5}
            },
            "curvar": "T2",
            "value": 2.5
        }
        expect = {
            "out": (CONTRADICTION, {"T1", "T3", "T4", "T5", "T6", "T7"})
        }
        assert_constraint(csp, sut, "establish", given, expect)
    
    def test_establishes_once_only(self):
        '''Enforces the case that the algorithm simply does nothing!
        
        The algorithm only checks domains if THE FIRST T variable is being
        established. Otherwise, we are sure that domains are consistent AND further
        reduction is impossible.
        
        The domains remain intact in this case, and they are NOT examined.'''
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"T1": 2.5},
            "D": {
                "T1": {2.5},
                "T2": {2.5},
                "T3": {2.5},
                "T4": {2.5},
                "T5": {2.5},
                "T6": {2.5},
                "T7": {2.5}
            },
            "curvar": "T2",
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
                "T1": {2.5},
                "T2": {2.5},
                "T3": {2.5},
                "T4": {2.5},
                "T5": {2.5},
                "T6": {2.5},
                "T7": {2.5}
            },
            "curvar": "T1",
            "value": 2.5
        }
        expect = {
            "out": ALREADY_CONSISTENT
        }
        assert_constraint(csp, sut, "establish", given, expect)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_SAMETHICK)
    runner.run(suite)        