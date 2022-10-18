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
        spec = specs["C"]
        UNARY.unarify(self.__csp, self.__catalog, spec)
        self.__sut = MAC(self.__csp, self.__catalog, spec)

    def test_L1_propagation_after_unary(self):
        # arrange
        csp = self.__csp
        # act
        res = self.__sut.propagate({"L1"})
        # assess
        print(res)