import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
grandparent = op.dirname(op.dirname(current))
sp.append(grandparent)

from csp import CSP
from half import HALF
from spec import specs
from constants import *

class test_HALF(unittest.TestCase):
    '''The goal is to test the behavior of half constraint.'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = HALF()

    def __run_case(self, mth, given, expect):
        csp = self.__csp
        csp.unassign_all()
        # arrange
        D = csp.get_domains()
        if "D" in given:
            for var, domain in given["D"].items():
                csp.update_domain(var, domain)
        if "A" in given:
            for var, val in given["A"].items():
                csp.assign(var, val)
        # act
        if mth == "propagate":
            out = self.__sut.propagate(csp, given["reduced_vars"])
        else:
            out = self.__sut.establish(csp, given["curvar"], given["value"])
        # assess
        self.assertEqual(out, expect["out"])
        if "D" in expect:
            for var, domain in expect["D"].items():
                self.assertEqual(D[var], expect["D"][var])

    def test_propagation_reduces_both(self):
        given = {
            "D": {
                "L1": {"min": 30, "max": 36},
                "L2": {"min": 59, "max": 70}
            },
            "reduced_vars": {"L1"}
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L1", "L2"}, {"L1", "L2"}),
            "D": {
                "L1": {"min": 30, "max": 35},
                "L2": {"min": 60, "max": 70}
            }
        }
        self.__run_case("propagate", given, expect)
        given = {
            "D": {
                "L1": {"min": 19, "max": 30},
                "L2": {"min": 40, "max": 61}
            },
            "reduced_vars": {"L1"}
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L1", "L2"}, {"L1", "L2"}),
            "D": {
                "L1": {"min": 20, "max": 30},
                "L2": {"min": 40, "max": 60}
            }
        }

    def test_propagation_reduces_L1(self):
        given = {
            "D": {
                "L1": {"min": 29, "max": 36},
                "L2": {"min": 60, "max": 70}
            },
            "reduced_vars": {"L1"}
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L1", "L2"}, {"L1"}),
            "D": {
                "L1": {"min": 30, "max": 35},
                "L2": {"min": 60, "max": 70}
            }
        }
        self.__run_case("propagate", given, expect)

    def test_propagation_reduces_L2(self):
        given = {
            "D": {
                "L1": {"min": 30, "max": 35},
                "L2": {"min": 59, "max": 72}
            },
            "reduced_vars": {"L1"}
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L1", "L2"}, {"L2"}),
            "D": {
                "L1": {"min": 30, "max": 35},
                "L2": {"min": 60, "max": 70}
            }
        }
        self.__run_case("propagate", given, expect)

    def test_propagation_leaves_intact(self):
        given = {
            "D": {
                "L1": {"min": 30, "max": 35},
                "L2": {"min": 60, "max": 70}
            },
            "reduced_vars": {"L1"}
        }
        expect = {
            "out": (DOMAINS_INTACT, {"L1", "L2"}),
        }
        self.__run_case("propagate", given, expect)

    def test_propagation_detects_contradiction(self):
        given = {
            "D": {
                "L1": {"min": 20, "max": 20},
                "L2": {"min": 41, "max": 70}
            },
            "reduced_vars": {"L1"},
        }
        expect = {
            "out": (CONTRADICTION, {"L1", "L2"}, set([])),
        }
        self.__run_case("propagate", given, expect)
        given = {
            "D": {
                "L1": {"min": 40, "max": 70},
                "L2": {"min": 22, "max": 22}
            },
            "reduced_vars": {"L1"},
        }
        expect = {
            "out": (CONTRADICTION, {"L1", "L2"}, set([])),
        }
        self.__run_case("propagate", given, expect)

    def test_reduction_after_assignment(self):
        given = {
            "D": {
                "L2": {"min": 59, "max": 61}
            },
            "A": {
                "L1": 30
            },
            "curvar": "L1",
            "value": 30
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L2"}, {"L2"}),
            "D": {
                "L2": {"min": 60, "max": 60}
            }
        }
        self.__run_case("establish", given, expect)
        given = {
            "D": {
                "L1": {"min": 29, "max": 31}
            },
            "A": {
                "L2": 60
            },
            "curvar": "L2",
            "value": 60
        }
        expect = {
            "out": (DOMAINS_REDUCED, {"L1"}, {"L1"}),
            "D": {
                "L1": {"min": 30, "max": 30}
            }
        }
        self.__run_case("establish", given, expect)

    def test_assignment_leaves_intact(self):
        given = {
            "D": {
                "L2": {"min": 60, "max": 60}
            },
            "A": {
                "L1": 30
            },
            "curvar": "L1",
            "value": 30
        }
        expect = {
            "out": (DOMAINS_INTACT, {"L2"}),
        }
        self.__run_case("establish", given, expect)
        given = {
            "D": {
                "L1": {"min": 30, "max": 30}
            },
            "A": {
                "L2": 60
            },
            "curvar": "L2",
            "value": 60
        }
        expect = {
            "out": (DOMAINS_INTACT, {"L1"}),
        }
        self.__run_case("establish", given, expect)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_HALF)
    runner.run(suite)