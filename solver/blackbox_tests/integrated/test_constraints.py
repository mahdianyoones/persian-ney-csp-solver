import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
grandparent = op.dirname(op.dirname(current))
sp.append(grandparent)

from csp import CSP
from stock import STOCK
from constants import *
from catalog import CATALOG
from unary import UNARY
from testspec import specs

class test_CONSTRAINTS(unittest.TestCase):

    def test_D_reduces(self):
        '''Asserts a case that D1 is reduced.
        
        Assigning R1 and T1 limits the choices for D1.'''
        # arrange
        self.__csp = CSP()
        current = op.dirname(__file__)
        self.__catalog = CATALOG(current+"/stock_test.csv")
        self.__sut = STOCK(self.__catalog)
        csp = self.__csp
        UNARY.unarify(csp, self.__catalog, specs["C"])
        D = csp.get_domains()
        csp.assign("T1", 1)
        csp.assign("R1", 0.5)
        # act
        out = self.__sut.establish(csp, "R1", 0.5)
        # assess
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"D1", "L1"})
        self.assertEqual(out[2], {"D1", "L1"})
        D = csp.get_domains()
        self.assertEqual(D["D1"], {18})