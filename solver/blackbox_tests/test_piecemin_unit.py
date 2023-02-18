import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
grandparent = op.dirname(op.dirname(current))
sp.append(parent)
sp.append(grandparent)

from csp import CSP
from constants import *
from piecemin import PIECEMIN
import case_runner

class test_PIECEMIN(unittest.TestCase):

    def setUp(self):
        self.__csp = CSP()
        self.__sut = PIECEMIN()
        self.__case_runner = case_runner.test_CASE_RUNNER()

    def test_establish_finds_P_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "P1": {
                    (1,40,1,1,1),
                    (1,41,1,1,1),
                    (1,42,1,1,1),
                },
            },
            "A": {"L1": 40},
            "curvar": "L1",
            "value": 40,
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": ALREADY_CONSISTENT
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_establish_does_not_revise_L(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"P1": (1,42,1,1,1)},
            "D": {
                "L1": {"min": 41, "max": 100},
            },
            "curvar": "P1",
            "value": (1,42,1,1,1),
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": REVISED_NONE
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_propagate_finds_all_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "P1": {
                    (1,40,1,1,1),
                    (1,41,1,1,1),
                    (1,42,1,1,1),                    
                },
                "L1": {"min": 40, "max": 100}
            },
            "reduced_vars": {"L1"},
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": ALREADY_CONSISTENT
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_establish_makes_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "P1": {
                    (1,40,1,1,1),
                    (1,41,1,1,1),
                    (1,42,1,1,1),                    
                },
            },
            "A": {"L1": 41},
            "curvar": "L1",
            "value": 41,
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"P1"}),
            "D": {
                "P1": {
                    (1,41,1,1,1),
                    (1,42,1,1,1)
                },
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_propagate_makes_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        # case 1
        given = {
            "D": {
                "L1": {"min": 41, "max": 100},
                "P1": {
                    (1,40,1,1,1),
                    (1,41,1,1,1),
                    (1,42,1,1,1),                    
                }
            },
            "reduced_vars": {"P1"},
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"P1"}),
            "D": {
                "P1": {
                    (1,41,1,1,1),
                    (1,42,1,1,1),                    
                },
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)
        # case 2
        given = {
            "D": {
                "L10": {"min": 41, "max": 100},
                "P10": {
                    (1,40,1,1,1),
                    (1,41,1,1,1),
                    (1,42,1,1,1),                    
                }
            },
            "reduced_vars": {"P10"},
            "participants": {"L10", "P10"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"P10"}),
            "D": {
                "P10": {
                    (1,41,1,1,1),
                    (1,42,1,1,1),                    
                },
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_propagate_detects_L_contradictory(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "P1": {
                    (1,40,1,1,1),
                    (1,41,1,1,1),
                    (1,42,1,1,1),                    
                },
                "L1": {"min": 43, "max": 100}
            },
            "kook": "anything",
            "reduced_vars": {"L1"},
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": (CONTRADICTION, {"P1"})
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_propagate_does_not_revise_L(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L1": {"min": 43, "max": 100}
            },
            "kook": "anything",
            "A": {"P1": (1,40,1,1,1)},
            "reduced_vars": {"L1"},
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": REVISED_NONE
        }
        assert_constraint(csp, sut, "propagate", given, expect)

if __name__ == "__main__":
    unittest.main()