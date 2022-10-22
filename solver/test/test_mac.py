from math import exp
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
    '''Tests the behavior of mac.'''

    def setUp(self):
        self.__csp = CSP()
        self.__catalog = CATALOG()
        self.__catalog.setup(current+"/pieces.csv")
        self.__spec = specs["C"]
        self.__sut = MAC(self.__csp, self.__catalog, self.__spec)
        
    def test_X_propagates_after_unary(self):
        # arrange
        csp = self.__csp
        UNARY.unarify(csp, self.__catalog, self.__spec)
        # act
        X = csp.get_variables()
        res = self.__sut.propagate(X)
        # assess
        self.assertEqual(res[0], PROPAGATION_PROCEEDED)
        expected = csp.get_constraints().keys()
        self.assertEqual(res[2], expected)

    def test_R1_gets_established(self):
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
        expected_examined = {'R2','R3','R4','R5','R6','R7','T1','D1','L1'}
        self.assertEqual(res[1], expected_examined)
        self.assertEqual(res[3], {"stock1", "sameround"})