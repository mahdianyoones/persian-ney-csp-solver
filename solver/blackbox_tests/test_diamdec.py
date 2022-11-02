import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
grandparent = op.dirname(op.dirname(current))
sp.append(grandparent)

from csp import CSP
from diamdec import DIAMDEC
from constants import *
import case_runner

class test_DIAMDEC(unittest.TestCase):
    '''Test the behavior of diameter decrement constraint.'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = DIAMDEC({"min": 0.5, "max": 1.0})
        self.__case_runner = case_runner.test_CASE_RUNNER()
    
    def test_establish_leaves_all_intact(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"D1": 14},
            "D": {
                "D2": {13},
            },
            "curvar": "D1",
            "value": 14
        }
        expect = {
            "out": (DOMAINS_INTACT, {"D2"})
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_propagation_leaves_all_intact(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"D1": 14},
            "D": {
                "D1": {14},
                "D2": {13},
                "D3": {12.5},
                "D4": {11.5},
                "D5": {10.5},
                "D6": {9.5},
                "D7": {8.5, 8.6, 9},
            },
            "reduced_vars": {"D5", "D4", "D1", "D7"},
        }
        expect = {
            "out": (DOMAINS_INTACT, {"D2","D3","D4","D5","D6","D7"})
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_propagation_causes_reduction(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "D1": {14},
                "D2": {13, 16},
                "D3": {12.5, 13},
                "D4": {11.5, 12},
                "D5": {10.5, 11},
                "D6": {9.5, 10},
                "D7": {8.4, 8.5, 8.6, 9},
            },
            "reduced_vars": {"D1", "D6"},
        }
        expect = {
            "out": (DOMAINS_REDUCED,
                {"D1","D2","D3","D4","D5","D6","D7"},
                {"D2","D3","D7"}),
            "D": {
                "D2": {13},
                "D3": {12.5},
                "D7": {8.5, 8.6, 9}
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)
        given = {
            "D": {
                "D1": {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D2": {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D3": {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D4": {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D5": {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D6": {7, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D7": {6},
            },
            "reduced_vars": {"D7"},
        }
        expect = {
            "out": (DOMAINS_REDUCED,
                {"D1","D2","D3","D4","D5","D6","D7"},
                {"D1", "D2", "D3", "D4", "D5", "D6"}),
            "D": {
                "D1": {10, 10.5, 11, 11.5},
                "D2": {9.5, 10, 10.5, 11},
                "D3": {9, 9.5, 10},
                "D4": {8.5, 9},
                "D5": {8},
                "D6": {7},
                "D7": {6},
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_reduction_by_establish(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"D5": 11, "D6": 10},
            "D": {
                "D7": {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
            },
            "curvar": "D6",
            "value": 10
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"D7"}, {"D7"}),
            "D": {
                "D7": {9, 9.5}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)
        given = {
            "A": {"D1": 10.5},
            "D": {
                "D1": {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D2": {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D3": {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D4": {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D5": {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D6": {7, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D7": {6, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
            },
            "curvar": "D1",
            "value": 10.5
        }
        expect = {
            "out": (DOMAINS_REDUCED, 
            {"D2", "D3", "D4", "D5", "D6", "D7"}, 
            {"D2", "D3", "D4", "D5", "D6", "D7"}),
            "D": {
                "D2": {9.5, 10},
                "D3": {9, 9.5},
                "D4": {8.5, 9},
                "D5": {8},
                "D6": {7},
                "D7": {6},
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)
        given = {
            "A": {"D7": 6},
            "D": {
                "D1": {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D2": {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D3": {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D4": {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D5": {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D6": {7, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
                "D7": {6, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13},
            },
            "curvar": "D7",
            "value": 6
        }
        expect = {
            "out": (DOMAINS_REDUCED, 
            {"D1", "D2", "D3", "D4", "D5", "D6"},
            {"D1", "D2", "D3", "D4", "D5", "D6"}),
            "D": {
                "D1": {10, 10.5, 11, 11.5},
                "D2": {9.5, 10, 10.5, 11},
                "D3": {9, 9.5, 10},
                "D4": {8.5, 9},
                "D5": {8},
                "D6": {7}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_establish_detects_contradiction(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"D1": 12.5},
            "D": {
                "D2": {13, 13.5, 13.6, 14},
            },
            "curvar": "D1",
            "value": 12.5
        }
        expect = {
            "out": (CONTRADICTION, {"D2"}, {"D1"}),
        }
        assert_constraint(csp, sut, "establish", given, expect)
        given = {
            "A": {"D1": 14, "D2": 13, "D3": 12, "D4": 11},
            "D": {
                "D5": {13, 13.5, 13.6, 14},
            },
            "curvar": "D4",
            "value": 11
        }
        expect = {
            "out": (CONTRADICTION, {"D5"}, {"D1", "D2", "D3", "D4"}),
        }
        assert_constraint(csp, sut, "establish", given, expect)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_DIAMDEC)
    runner.run(suite)