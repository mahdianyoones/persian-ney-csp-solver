import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
sp.append(parent)

from constants import *
from csp import CSP
from unary import UNARY
from testspec import specs

class test_UNARY(unittest.TestCase):
    '''Tests the behavior of unary.'''

    def setUp(self):
        self.__csp = CSP()
        self.__sut = UNARY

    def test_inits_domains_correctly(self):
        # act
        self.__sut.init_domains(self.__csp, current+"/unary.csv")
        # assess
        expected_pieces = {
            ("1", 100, 2, 0, 19), 
            ("2", 200, 2, 0, 18), 
            ("3", 80, 2, 0, 17),
            ("4", 70, 2, 0, 16), 
            ("5", 150, 2, 0, 15), 
            ("6", 130, 2, 0, 14), 
            ("7", 60, 2, 0, 14), 
            ("8", 170, 2, 1, 13), 
            ("9", 220, 2.5, 0, 13), 
            ("10", 300, 2, 0, 13), 
            ("11", 120, 2, 0, 12.4)
        }
        D = self.__csp.get_domains()
        for p in {"P1", "P2", "P3", "P4", "P5", "P6", "P7"}:
            self.assertEqual(D[p], expected_pieces)
        
    def test_establishes_unary_consistency_correctly(self):
        # arrange
        self.__sut.init_domains(self.__csp, current+"/unary.csv")
        # act
        self.__sut.unarify(self.__csp, [specs["C"]])
        D = self.__csp.get_domains()
        expected_pieces = {
            ("1", 100, 2, 0, 19), 
            ("2", 200, 2, 0, 18)
        }
        self.assertEqual(D["P1"], expected_pieces)
        self.assertEqual(D["L1"]["min"], 20)
        self.assertEqual(D["L4"]["min"], 58)
        self.assertEqual(D["L5"]["min"], 77)
        self.assertEqual(D["L6"]["min"], 20)

if __name__ == "__main__":
    unittest.main()