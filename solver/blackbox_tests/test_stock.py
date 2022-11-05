import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
grandparent = op.dirname(op.dirname(current))
sp.append(parent)
sp.append(grandparent)

from csp import CSP
from stock import STOCK
from constants import *
from catalog import CATALOG
from unary import UNARY
import case_runner

class test_STOCK(unittest.TestCase):
    '''Tests the behavior of stock constraints.
    
    Assumes catalog is well-tested.'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__catalog = CATALOG(current+"/stock.csv")
        self.__sut = STOCK(self.__catalog)
        UNARY.init_domains(self.__csp, self.__catalog)
        self.__case_runner = case_runner.test_CASE_RUNNER()

    def tests_R_is_assigned_PDT_get_reduced(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"R1": 1},
            "curvar": "R1",
            "value": 1
        }
        expect = {
            "out": (DOMAINS_REDUCED, set([]), {"D1", "P1", "T1"}),
            "D": {
                "D1": {13},
                "T1": {2},
                "P1": {("8", 170)}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)
        
    def tests_RDT_are_assigned_P_gets_reduced(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"R1": 0, "T1": 2, "D1": 14},
            "curvar": "R1",
            "value": 0
        }
        expect = {
            "out": (DOMAINS_REDUCED, set([]), {"P1"}),
            "D": {
                "P1": {("6", 130), ("7", 60)}
            }
        }
        assert_constraint(csp, sut, "establish", given, expect)

    def tests_establish_detects_contradiction(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "A": {"D1": 18, "R1": 1},
            "curvar": "R1",
            "value": 1
        }
        expect = {
            "out": (CONTRADICTION, set([]), {"D1", "R1", "P1"})
        }
        assert_constraint(csp, sut, "establish", given, expect)
    
    def tests_propagate_takes_no_action(self):
        sut = self.__sut
        csp = self.__csp
        assert_constraint = self.__case_runner.assert_constraint
        given = {
            "reduced_vars": {"R1"},
        }
        expect = {
            "out": (DOMAINS_INTACT, set([]))
        }
        assert_constraint(csp, sut, "propagate", given, expect)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_STOCK)
    runner.run(suite)        