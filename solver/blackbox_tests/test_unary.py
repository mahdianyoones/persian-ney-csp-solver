import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
sp.append(parent)

from constants import *
from catalog import CATALOG
from csp import CSP
from unary import UNARY
from testspec import specs

class test_UNARY(unittest.TestCase):
    '''Tests the behavior of unary.
    
    Assumes the catalog is well-tested.'''

    def setUp(self):
        self.__csp = CSP()
        self.__catalog = CATALOG(current+"/unary.csv")
        self.__sut = UNARY

    def test_inits_domains_correctly(self):
        # act
        self.__sut.init_domains(self.__csp, self.__catalog)
        # assess
        expected_pieces = {
            ("1", 100), 
            ("2", 200), 
            ("3", 80),
            ("4", 70), 
            ("5", 150), 
            ("6", 130), 
            ("7", 60), 
            ("8", 170), 
            ("9", 220), 
            ("10", 300), 
            ("11", 120)
        }
        D = self.__csp.get_domains()
        for p in {"P1", "P2", "P3", "P4", "P5", "P6", "P7"}:
            self.assertEqual(D[p], expected_pieces)
        expected_diameters = {12.4, 13, 14, 15, 16, 17, 18, 19}
        for d in {"D1", "D2", "D3", "D4", "D5", "D6", "D7"}:
            self.assertEqual(D[d], expected_diameters)
        expected_thicknesses = {2, 2.5}
        for t in {"T1", "T2", "T3", "T4", "T5", "T6", "T7"}:
            self.assertEqual(D[t], expected_thicknesses)
        expected_roundnesses = {0, 1}
        for r in {"R1", "R2", "R3", "R4", "R5", "R6", "R7"}:
            self.assertEqual(D[r], expected_roundnesses)
        
    def test_establishes_unary_consistency_correctly(self):
        # arrange
        self.__sut.init_domains(self.__csp, self.__catalog)
        # act
        self.__sut.unarify(self.__csp, specs["C"])
        D = self.__csp.get_domains()
        self.assertEqual(D["D1"], {18, 19})
        self.assertEqual(D["L1"]["min"], 20)
        self.assertEqual(D["L4"]["min"], 58)
        self.assertEqual(D["L5"]["min"], 77)
        self.assertEqual(D["L6"]["min"], 20)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_UNARY)
    runner.run(suite)            