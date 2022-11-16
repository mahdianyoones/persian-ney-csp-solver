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

class test_PIECEMIN(unittest.TestCase):

    def setUp(self):
        self.__csp = CSP()
        self.__sut = PIECEMIN()

    def test_establish_finds_P_consistent(self):
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
            "out": ALREADY_CONSISTENT
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_establish_finds_L_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L1": {"min": 41, "max": 100},
            },
            "curvar": "P1",
            "value": ("3", 42),
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": ALREADY_CONSISTENT
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_propagate_finds_all_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "P1": {("1", 40), ("2", 41), ("3", 42)},
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
                "P1": {("1", 40), ("2", 41), ("3", 42)},
            },
            "A": {"L1": 41},
            "curvar": "L1",
            "value": 41,
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"P1"}),
            "D": {
                "P1": {("2", 41), ("3", 42)},
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_propagate_makes_consistent(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L1": {"min": 41, "max": 100},
                "P1": {("1", 40), ("2", 41), ("3", 42)}
            },
            "reduced_vars": {"P1"},
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"P1"}),
            "D": {
                "P1": {("2", 41), ("3", 42)},
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_propagate_detects_L_contradictory(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "P1": {("1", 40), ("2", 41), ("3", 42)},
                "L1": {"min": 43, "max": 100}
            },
            "reduced_vars": {"L1"},
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": CONTRADICTION
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_propagate_detects_P_contradictory(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L1": {"min": 43, "max": 100}
            },
            "A": {"P1": ("1", 40)},
            "reduced_vars": {"L1"},
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": CONTRADICTION
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_establish_revises_nothing(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"P1": ("1", 40), "L1": 30},
            "curvar": "L1",
            "value": 30,
            "participants": {"L1", "P1"}
        }
        expect = {
            "out": REVISED_NONE
        }
        assert_constraint(csp, sut, "propagate", given, expect)
