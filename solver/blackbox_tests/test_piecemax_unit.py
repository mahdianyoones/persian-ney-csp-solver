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
from piecemax import PIECEMAX
import case_runner

class test_PIECEMAX(unittest.TestCase):

    def setUp(self):
        self.__csp = CSP()
        self.__sut = PIECEMAX()
        self.__case_runner = case_runner.test_CASE_RUNNER()

    def test_establish_finds_L_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"P1": ("3", 42)},
            "D": {
                "L1": {"min": 1, "max": 42},
            },
            "curvar": "P1",
            "value": ("3", 42),
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": ALREADY_CONSISTENT
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_establish_revises_nothing(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"L1": 40, "P1": ("3", 42)},
            "curvar": "L1",
            "value": 40,
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": REVISED_NONE
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_establish_does_not_revise_P(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "P1": {("1", 40), ("2", 41), ("3", 42)},
            },
            "A": {"L1": 40},
            "curvar": "L1",
            "value": 40,
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": REVISED_NONE
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_establish_makes_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L1": {"min": 1, "max": 43}
            },
            "A": {"P1": ("3", 42)},
            "curvar": "P1",
            "value": ("3", 42),
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"L1"}),
            "D": {
                "L1": {"min": 1, "max": 42}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_propagate_makes_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "P1": {("1", 40), ("2", 41), ("3", 42)},
                "L1": {"min": 1, "max": 43},
            },
            "reduced_vars": {"L1"},
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"L1"}),
            "D": {
                "L1": {"min": 1, "max": 42}
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_propagate_finds_L_contradictory(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"P1": ("3", 42)},
            "D": {
                "L1": {"min": 43, "max": 100},
            },
            "curvar": "P1",
            "value": ("3", 42),
            "reduced_vars": {"L1"},
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": CONTRADICTION
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_propagate_detects_contradiction(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "P1": {("1", 40), ("2", 41), ("3", 42)},
                "L1": {"min": 43, "max": 100},
            },
            "reduced_vars": {"L1"},
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": CONTRADICTION
        }
        assert_constraint(csp, sut, "propagate", given, expect)

if __name__ == "__main__":
    unittest.main()