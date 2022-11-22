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

@unittest.skip("")
class test_LEN_INTEGRATION(unittest.TestCase):
    '''Tests the behavior of MAC.

    len:	 	    (L1, L2, L3, L4, L5, L6, L7)
    hole6:		    (L1, L2, L3, L4, L5)
    hole3:		    (L1, L2, L3, L4)
    hole1:		    (L1, L2, L3)
    half:           (L1, L2)'''

    def setUp(self):
        self.__X = {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}
        self.__C = {
            "len":    {"L1", "L2", "L3", "L4", "L5", "L6", "L7"},
            "hole6":  {"L1", "L2", "L3", "L4", "L5"},
            "hole3":  {"L1", "L2", "L3", "L4"},
            "hole1":  {"L1", "L2", "L3"},
            "half":   {"L1", "L2"} 
        }
        self.__csp = CSP(self.__X, self.__C)
        current = op.dirname(__file__)
        catalog = CATALOG()
        catalog.setup(current+"/real_pieces.csv")
        self.__mac = MAC(self.__csp, catalog, specs["C"])
        UNARY.init_domains(self.__csp, catalog)
        UNARY.unarify(self.__csp, specs["C"])

if __name__ == "__main__":
    unittest.main()