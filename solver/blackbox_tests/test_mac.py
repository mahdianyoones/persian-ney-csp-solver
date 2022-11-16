import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
grandparent = op.dirname(op.dirname(current))
sp.append(parent)
sp.append(grandparent)

import copy
from csp import CSP
from catalog import CATALOG
from mac import MAC
from unary import UNARY
from testspec import specs
from constants import *

class test_MAC(unittest.TestCase):
    '''Tests the behavior of MAC.
    '''

    def setUp(self):
        self.__csp = CSP()
        self.__catalog = CATALOG()
        current = op.dirname(__file__)
        self.__catalog.setup(current+"/contains_solutions.csv")
        self.__spec = specs["C"]
        self.__sut = MAC(self.__csp, self.__catalog, self.__spec)
        
    def test_propagate_makes_consistent(self):
        # arrange
        csp = self.__csp
        spec = self.__spec
        catalog = self.__catalog
        UNARY.init_domains(csp, catalog)
        UNARY.unarify(csp, spec)
        D_backup = copy.deepcopy(csp.get_domains())
        # act
        X = csp.get_variables()
        res = self.__sut.propagate(copy.deepcopy(X))
        # assess
        self.assertEqual(res[0], MADE_CONSISTENT)
        not_expected = {"T1", "T2", "T3", "T4", "T5", "T6", "T7"}
        not_expected.update({"R1", "R2", "R3", "R4", "R5", "R6", "R7"})
        not_expected.add("D1")
        expected = X.difference(not_expected)
        self.assertEqual(res[1], expected)
        D = csp.get_domains()
        for v in expected:
            self.assertNotEqual(D_backup[v], D[v])

if __name__ == "__main__":
    unittest.main()