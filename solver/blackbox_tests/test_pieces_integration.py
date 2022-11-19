import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
grandparent = op.dirname(op.dirname(current))
sp.append(parent)
sp.append(grandparent)

from csp import CSP
from catalog import CATALOG
from mac import MAC
from unary import UNARY
from testspec import specs
from constants import *

class test_PIECES_INTEGRATION(unittest.TestCase):
    '''Tests the integrated behavior of constraints that deal with pieces.
    
    These constraints are pstock, dstock, rstock, tstock, piecemin, 
    and nodemax.'''

    def setUp(self):
        self.__X = {"T1", "R1", "D1", "P1", "L1"}
        self.__C = {
            "pstock1":   {"T1", "R1", "D1", "P1"},
            "dstock1":   {"T1", "R1", "D1"},
            "rstock1":   {"T1", "R1", "D1"},
            "tstock1":   {"T1", "R1", "D1"},
            "piecemin1": {"L1", "P1"},
            "nodemax1":  {"L1", "P1"}
        }
        self.__csp = CSP(self.__X, self.__C)
        current = op.dirname(__file__)
        self.__catalog = CATALOG()
        self.__catalog.setup(current+"/stock.csv")
        UNARY.init_domains(self.__csp, self.__catalog)
        UNARY.unarify(self.__csp, specs["C"])
        self.__mac = MAC(self.__csp, self.__catalog, specs["C"])
        
    def test_L1_reduction_propagates(self):
        # act
        D = self.__csp.get_domains()
        csp = self.__csp
        csp.update_domain("L1", {"min": 200, "max": 400})
        res = self.__mac.propagate({"L1"})
        self.assertEqual(res[0], MADE_CONSISTENT)
        self.assertEqual(D["L1"]["max"], 300)
        self.assertEqual(D["T1"], {2, 2.5})
        self.assertEqual(D["R1"], {0})
        self.assertEqual(D["D1"], {18})
        self.assertEqual(D["P1"], {("2", 200), ("9", 220), ("10", 300)})

    def test_D1_assignment_gets_established(self):
        # act
        D = self.__csp.get_domains()
        csp = self.__csp
        csp.assign("D1", 19)
        res = self.__mac.establish("D1", 19)
        self.assertEqual(res[0], MADE_CONSISTENT)
        self.assertEqual(D["L1"]["max"], 100)
        self.assertEqual(D["T1"], {2})
        self.assertEqual(D["R1"], {0})
        self.assertEqual(D["P1"], {("1", 100)})

    def test_P1_assignment_propagates(self):
        D = self.__csp.get_domains()
        csp = self.__csp
        csp.assign("P1", ("1", 100))
        res = self.__mac.establish("P1", ("1", 100))
        self.assertEqual(res[0], MADE_CONSISTENT)
        self.assertEqual(D["L1"]["max"], 100)
        self.assertEqual(D["T1"], {2})
        self.assertEqual(D["R1"], {0})
        self.assertEqual(D["D1"], {19})


if __name__ == "__main__":
    unittest.main()