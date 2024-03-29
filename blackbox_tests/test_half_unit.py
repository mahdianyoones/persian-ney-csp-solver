import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
grandparent = op.dirname(op.dirname(current))
sp.append(parent)
sp.append(grandparent)

from csp import CSP
from half import HALF
from spec import specs
from constants import *
import case_runner

class test_HALF(unittest.TestCase):
    '''The goal is to test the behavior of half constraint.'''
    
    def setUp(self):
        self.__csp = CSP(S=2)
        self.__sut = HALF()
        self.__case_runner = case_runner.test_CASE_RUNNER()

    def test_propagation_reduces_both(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L1": {"min": 30, "max": 36},
                "L2": {"min": 59, "max": 70}
            },
            "participants": {"L1", "L2"},
            "reduced_vars": {"L1"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"L1", "L2"}),
            "D": {
                "L1": {"min": 30, "max": 35},
                "L2": {"min": 60, "max": 70}
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)
        given = {
            "D": {
                "L1": {"min": 19, "max": 30},
                "L2": {"min": 40, "max": 61}
            },
            "participants": {"L1", "L2"},
            "reduced_vars": {"L1"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"L1", "L2"}),
            "D": {
                "L1": {"min": 20, "max": 30},
                "L2": {"min": 40, "max": 60}
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_propagation_reduces_L1(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L1": {"min": 29, "max": 36},
                "L2": {"min": 60, "max": 70}
            },
            "participants": {"L1", "L2"},
            "reduced_vars": {"L1"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"L1"}),
            "D": {
                "L1": {"min": 30, "max": 35},
                "L2": {"min": 60, "max": 70}
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_propagation_reduces_L2(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L1": {"min": 30, "max": 35},
                "L2": {"min": 59, "max": 72}
            },
            "participants": {"L1", "L2"},
            "reduced_vars": {"L1"}
        }
        expect = {
            "out": (MADE_CONSISTENT, {"L2"}),
            "D": {
                "L1": {"min": 30, "max": 35},
                "L2": {"min": 60, "max": 70}
            }
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_propagation_leaves_intact(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L1": {"min": 30, "max": 35},
                "L2": {"min": 60, "max": 70}
            },
            "participants": {"L1", "L2"},
            "reduced_vars": {"L1"}
        }
        expect = {
            "out": ALREADY_CONSISTENT
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_propagation_detects_contradiction(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L1": {"min": 20, "max": 20},
                "L2": {"min": 41, "max": 70}
            },
            "participants": {"L1", "L2"},
            "reduced_vars": {"L1"},
        }
        expect = {
            "out": (CONTRADICTION, {"L1", "L2"})
        }
        assert_constraint(csp, sut, "propagate", given, expect)
        given = {
            "D": {
                "L1": {"min": 40, "max": 70},
                "L2": {"min": 22, "max": 22}
            },
            "participants": {"L1", "L2"},
            "reduced_vars": {"L1"},
        }
        expect = {
            "out": (CONTRADICTION, {"L1", "L2"})
        }
        assert_constraint(csp, sut, "propagate", given, expect)

    def test_reduction_after_assignment(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L2": {"min": 59, "max": 61}
            },
            "participants": {"L1", "L2"},
            "A": {
                "L1": 30
            },
            "curvar": "L1",
            "value": 30
        }
        expect = {
            "out": (MADE_CONSISTENT, {"L2"}),
            "D": {
                "L2": {"min": 60, "max": 60}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)
        given = {
            "D": {
                "L1": {"min": 29, "max": 31}
            },
            "participants": {"L1", "L2"},
            "A": {
                "L2": 60
            },
            "curvar": "L2",
            "value": 60
        }
        expect = {
            "out": (MADE_CONSISTENT, {"L1"}),
            "D": {
                "L1": {"min": 30, "max": 30}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)
        given = {
            "D": {
                "L8": {"min": 29, "max": 31}
            },
            "participants": {"L8", "L9"},
            "A": {
                "L9": 60
            },
            "curvar": "L9",
            "value": 60
        }
        expect = {
            "out": (MADE_CONSISTENT, {"L8"}),
            "D": {
                "L8": {"min": 30, "max": 30}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def test_assignment_leaves_intact(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "D": {
                "L2": {"min": 60, "max": 60}
            },
            "participants": {"L1", "L2"},
            "A": {
                "L1": 30
            },
            "curvar": "L1",
            "value": 30
        }
        expect = {
            "out": ALREADY_CONSISTENT
        }
        assert_constraint(csp, sut, "establish", given, expect)
        given = {
            "D": {
                "L1": {"min": 30, "max": 30}
            },
            "participants": {"L1", "L2"},
            "A": {
                "L2": 60
            },
            "curvar": "L2",
            "value": 60
        }
        expect = {
            "out": ALREADY_CONSISTENT
        }
        assert_constraint(csp, sut, "establish", given, expect)

if __name__ == "__main__":
    unittest.main()