import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
grandparent = op.dirname(op.dirname(current))
sp.append(grandparent)

from csp import CSP
from samethick import SAMETHICK
from constants import *

class test_SAMETHICK(unittest.TestCase):
    '''Tests the behavior of SAMETHICK constraint.'''

    def setUp(self):
        self.__csp = CSP()
        self.__sut = SAMETHICK()
    
    def test_establishes_and_reduces(self):
        # arrange
        csp = self.__csp
        domains = {
            "T1": {2.5, 2},
            "T2": {2.5, 5, 4},
            "T3": {0, 2.5},
            "T4": {0, 2.5},
            "T5": {0, 2.5},
            "T6": {0, 2.5},
            "T7": {0, 2.5}
        }
        for var, vals in domains.items():
            csp.update_domain(var, vals)
        # act
        output = self.__sut.establish(csp, "T2", 2.5)
        # assess
        self.assertEqual(output[0], DOMAINS_REDUCED)
        self.assertEqual(output[1], {"T1", "T3", "T4", "T5", "T6", "T7"})
        self.assertEqual(output[2], {"T1", "T3", "T4", "T5", "T6", "T7"})
        D = csp.get_domains()
        self.assertEqual(D["T2"], {2.5, 5, 4})
        for var in {"T1", "T3", "T4", "T5", "T6", "T7"}:
            self.assertEqual(D[var], {2.5})

    def test_contradiction_occurs(self):
        # arrange
        csp = self.__csp
        domains = {
            "T1": {0},
            "T2": {2.5},
            "T3": {0, 2.5},
            "T4": {0, 2.5},
            "T5": {0, 2.5},
            "T6": {0, 2.5},
            "T7": {0, 2.5}
        }
        for var, vals in domains.items():
            csp.update_domain(var, vals)
        # act
        output = self.__sut.establish(csp, "T1", 0)
        # assess
        self.assertEqual(output[0], CONTRADICTION)
    
    def test_establishes_once_only(self):
        '''Enforces the case that the algorithm simply does nothing!
        
        The algorithm only checks domains if THE FIRST T variable is being
        established. Otherwise, we are sure that domains are consistent AND further
        reduction is impossible.
        
        The domains remain intact in this case, and they are NOT examined.'''
        csp = self.__csp
        csp.assign("T1", 2.5)
        output = self.__sut.establish(csp, "T2", 2.5)
        self.assertEqual(output, (DOMAINS_INTACT, set([])))

    def test_all_contain_the_same_value(self):
        '''Enforces a case that domains are checked but no value is removed.
        
        i.e. the domains happend to be just consistent.
        
        The domains remain intact in this case, but they are all examined.'''
        # arrange
        csp = self.__csp
        domains = {
            "T1": {2.5},
            "T2": {2.5},
            "T3": {2.5},
            "T4": {2.5},
            "T5": {2.5},
            "T6": {2.5},
            "T7": {2.5}
        }
        for var, vals in domains.items():
            csp.update_domain(var, vals)
        # act
        output = self.__sut.establish(csp, "T1", 2.5)
        # assess
        self.assertEqual(output[0], DOMAINS_INTACT)
        self.assertEqual(output[1], {"T2", "T3", "T4", "T5", "T6", "T7"})

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_SAMETHICK)
    runner.run(suite)        