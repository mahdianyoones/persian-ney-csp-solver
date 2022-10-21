import unittest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from csp import CSP
from catalog import CATALOG
from mac import MAC
from unary import UNARY
from spec import specs
from constants import *

class test_MAC(unittest.TestCase):
    '''Tests the behavior of mac.
    
    The behaviors:

    
    '''

    def setUp(self):
        self.__csp = CSP()
        self.__catalog = CATALOG()
        self.__catalog.setup(current+"/pieces.csv")
        self.__spec = specs["C"]
        self.__sut = MAC(self.__csp, self.__catalog, self.__spec)

    def test_L1_propagation_after_unary(self):
        # arrange
        csp = self.__csp
        UNARY.unarify(csp, self.__catalog, self.__spec)
        # act
        res = self.__sut.propagate({"L1"})
        # assess
        D = csp.get_domains()
        self.assertEqual(res, PROPAGATION_PROCEEDED)
        self.assertEqual(D["L1"], {'min': 45, 'max': 69})
        self.assertEqual(D["L2"], {'min': 90, 'max': 138})
        self.assertEqual(D["L3"], {'min': 89, 'max': 137})
        self.assertEqual(D["L4"], {'min': 88, 'max': 136})
        self.assertEqual(D["L5"], {'min': 87, 'max': 135})
        self.assertEqual(D["L6"], {'min': 58, 'max': 134})
        self.assertEqual(D["L7"], {'min': 20, 'max': 133})
        
    def test_T1_is_established(self):
        # arrange
        csp = self.__csp
        X = csp.get_variables()
        UNARY.unarify(csp, self.__catalog, self.__spec)
        self.__sut.propagate(X)
        # act
        csp.assign("T1", 1.0)
        res = self.__sut.establish("T1", 1.0)
        # assess
        D = csp.get_domains()
        self.assertEqual(res[0], DOMAINS_REDUCED)
        examined = {'T6', 'R1', 'T7', 'D1', 'L1', 'T5', 'T3', 'T4', 'T2'}
        self.assertEqual(res[1], examined)
        for v in {"T2", "T3", "T4", "T5", "T6", "T7"}:
            self.assertEqual(D[v], {1.0})

    def test_R1_is_established(self):
        # arrange
        csp = self.__csp
        X = csp.get_variables()
        UNARY.unarify(csp, self.__catalog, self.__spec)
        self.__sut.propagate(X)
        # act
        csp.assign("R1", 0.0)
        res = self.__sut.establish("R1", 0.0)
        # assess
        D = csp.get_domains()
        self.assertEqual(res[0], DOMAINS_REDUCED)
        expected_examined = {'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'T1', 'D1', 'L1'}
        expected_reduced = {"R2", "R3", "R4", "R5", "R6", "R7", "T1"}
        self.assertEqual(res[1], expected_examined)
        self.assertEqual(res[2], expected_reduced)
        for v in {"R2", "R3", "R4", "R5", "R6", "R7"}:
            self.assertEqual(D[v], {0.0})